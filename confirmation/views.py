# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from commons.decorators import submitted_applicant_required, applicant_required
from commons.utils import admission_major_pref_deadline_passed, round2_confirmation_deadline_passed, validate_national_id, validate_phone_number
from commons.models import Log
from commons.email import send_admission_confirmation_by_email, send_admission_waive_by_email, send_admission_unwaive_by_email
from application.models import Applicant, SubmissionInfo, Major, Education, PersonalInfo
from result.models import NIETSScores, AdmissionResult, AdmissionRound

from models import AdmissionMajorPreference, AdmissionConfirmation, Round2ApplicantConfirmation, StudentRegistration, AdmissionWaiver

from django import forms
from django.forms import ModelForm
from django.conf import settings

def get_higher_ranked_majors(majors, current_major):
    result = []
    for m in majors:
        if m.id != current_major.id:
            result.append(m)
        else:
            return result
        

def check_form_submission(post_data, higher_majors):
    if (('pref_type' not in post_data) or
        (post_data['pref_type'] not in ['no_move',
                                        'move_up_inclusive',
                                        'move_up_strict',
                                        'withdrawn'])):
        return False, 'เลือกประเภทการพิจารณาไม่ถูกต้อง, กรุณาเลือก 1 ข้อ'
    if post_data['pref_type'] in ['move_up_strict', 'move_up_inclusive']:
        mcount = len(higher_majors)
        for i in range(mcount):
            if ('major-accepted-' + str(i+1)) in post_data:
                return True, ''
        return False, 'กรุณาเลือกสาขาที่ต้องการให้พิจารณาเลื่อนอันดับอย่างน้อย 1 สาขา'
    return True, ''

def update_admission_major_preference(pref, applicant,
                                      preferred_majors,
                                      higher_majors,
                                      round_number,
                                      post_data):
    if not pref:
        pref = AdmissionMajorPreference()

    pref.applicant = applicant
    pref.round_number = round_number
    
    alist = [0] * len(preferred_majors)
    if post_data['pref_type'] in ['move_up_inclusive', 'move_up_strict']:
        for i in range(len(higher_majors)):
            if ('major-accepted-' + str(i+1)) in post_data:
                alist[i] = 1
    if post_data['pref_type'] in ['no_move', 'move_up_inclusive']:
        alist[len(higher_majors)] = 1    # current admitted major

    pref.is_accepted_list = alist
    return pref

@submitted_applicant_required
def request_nomove(request, is_nomove):
    applicant = request.applicant
    admitted = applicant.is_admitted()

    if not admitted:
        return HttpResponseForbidden()

    first_admission = (applicant.admission_results.count() == 1)
    if first_admission:
        return HttpResponseForbidden()
    
    if request.method != 'POST':
        return HttpResponseForbidden()

    # check for deadline
    if admission_major_pref_deadline_passed():
        return render_to_response('confirmation/pref_deadline_passed.html')

    current_round = AdmissionRound.get_recent()
    round_number = current_round.number
    admission_pref = applicant.get_admission_major_preference(round_number)

    if not admission_pref:
        return HttpResponseForbidden()

    admission_pref.is_nomove_request = is_nomove
    admission_pref.save()

    Log.create("request nomove (%s) - from: %s" %
               (str(is_nomove),
                request.META['REMOTE_ADDR']),
               applicant_id=applicant.id,
               applicantion_id=applicant.submission_info.applicantion_id)

    return redirect('status-index')
    

@submitted_applicant_required
def pref(request):
    if settings.SHOW_ONLY_RESULTS:
        return HttpResponseForbidden()

    applicant = request.applicant
    admitted = applicant.is_admitted()

    if not admitted:
        return HttpResponseForbidden()

    first_admission = (applicant.admission_results.count() == 1)
    if not first_admission:
        return HttpResponseForbidden()

    registration = applicant.get_student_registration()
    if not registration:
        return HttpResponseForbidden()

    # check for deadline
    if admission_major_pref_deadline_passed():
        return render_to_response('confirmation/pref_deadline_passed.html')

    current_round = AdmissionRound.get_recent()
    round_number = current_round.number
    is_last_round = False

    admission_result = applicant.get_latest_admission_result()

    preferred_majors = applicant.preference.get_major_list()
    higher_majors = get_higher_ranked_majors(preferred_majors, 
                                             admission_result.admitted_major)

    admission_pref = applicant.get_admission_major_preference(round_number)

    if admission_pref:
        pref_type = admission_pref.get_pref_type()
        accepted_major_ids = [m.id for m in admission_pref.get_accepted_majors()]
        is_accepted_list = [(m.id in accepted_major_ids)
                            for m in higher_majors]
    else:
        pref_type = AdmissionMajorPreference.PrefType.new_empty()
        try:
            is_accepted_list = [False] * len(higher_majors)
        except:
            Log.create("Error: empty higher majors: %d" % (applicant.id,))
            raise

    form_check_message = ''

    if request.method=='POST':
        if 'submit' in request.POST:
            check_result, form_check_message = check_form_submission(request.POST, higher_majors)
            if check_result:
                admission_pref = update_admission_major_preference(
                    admission_pref,
                    applicant, preferred_majors,
                    higher_majors, 
                    round_number,
                    request.POST)
                admission_pref.set_ptype_cache(save=False)

                if is_last_round and (
                    admission_pref.get_pref_type().is_move_up_inclusive() or
                    admission_pref.get_pref_type().is_move_up_strict()):
                    return HttpResponseForbidden()

                admission_pref.save()
                request.session['notice'] = 'เก็บข้อมูลการยืนยันอันดับการเลือกสาขาวิชาแล้ว'

                Log.create("confirmation - from: %s,type: %d (%s), val: %s" %
                           (request.META['REMOTE_ADDR'],
                            admission_pref.get_pref_type().ptype,
                            request.POST['pref_type'],
                            str(admission_pref.is_accepted_list)),
                           applicant_id=applicant.id,
                           applicantion_id=applicant.submission_info.applicantion_id)

                return HttpResponseRedirect(reverse('status-index'))
        else:
            if admission_pref:
                request.session['notice'] = 'ยกเลิกการแก้ไขอันดับการเลือกสาขาวิชา'
            else:
                request.session['notice'] = 'ยกเลิกการยืนยันอันดับการเลือกสาขาวิชา'

            Log.create("confirmation: cancel",
                       applicant_id=applicant.id,
                       applicantion_id=applicant.submission_info.applicantion_id)

            return HttpResponseRedirect(reverse('status-index'))
    else:
        pass

    return render_to_response('confirmation/pref.html',
                              { 'applicant': applicant,
                                'admission_result': admission_result,
                                'current_round': current_round,
                                'is_last_round': is_last_round,
                                'registration': registration,
                                'higher_majors': higher_majors,
                                'majors_with_is_accepted':
                                    zip(higher_majors, is_accepted_list),
                                'admission_pref': admission_pref,
                                'pref_type': pref_type,
                                'form_check_message': form_check_message })


class StudentRegistrationForm(ModelForm):
    class Meta:
        model = StudentRegistration
        exclude = ('applicant')

        widgets = {
            'father_title': forms.TextInput(attrs={'size': 2}),
            'mother_title': forms.TextInput(attrs={'size': 2}),
            }

    def clean_nat_id_and_remark(self, nat_id, remark, field_name):
        if (nat_id != None) and (remark != None):
            if not validate_national_id(nat_id) and remark=='':
                self._errors[field_name] = self.error_class(['หมายเลขประชาชนไม่ถูกต้อง ถ้าใช้รหัสยืนยันอื่นหรือไม่มีรหัสยืนยันใด ๆ ให้เขียนอธิบายในช่องหมายเหตุ'])
                return False
        return True

    def clean_home_phone_number(self):
        p = self.cleaned_data['home_phone_number']
        if p!='' and not validate_phone_number(p):
            raise forms.ValidationError("หมายเลขโทรศัพท์ไม่ถูกต้อง")
        return p

    def clean_cell_phone_number(self):
        p = self.cleaned_data['cell_phone_number']
        if p!='' and not validate_phone_number(p):
            raise forms.ValidationError("หมายเลขโทรศัพท์ไม่ถูกต้อง")
        return p

    def clean(self):
        cleaned_data = self.cleaned_data
        father_national_id = cleaned_data.get('father_national_id')
        father_national_id_remark = cleaned_data.get('father_national_id_remark')
        
        mother_national_id = cleaned_data.get('mother_national_id')
        mother_national_id_remark = cleaned_data.get('mother_national_id_remark')
        
        if not self.clean_nat_id_and_remark(father_national_id,
                                            father_national_id_remark,
                                            'father_national_id'):
            del cleaned_data['father_national_id']
        
        if not self.clean_nat_id_and_remark(mother_national_id,
                                            mother_national_id_remark,
                                            'mother_national_id'):
            del cleaned_data['mother_national_id']
        
        hpn = cleaned_data.get('home_phone_number')
        cpn = cleaned_data.get('cell_phone_number')

        if hpn=='' and cpn=='':
            self._errors['cell_phone_number'] = self.error_class(['จะต้องระบุเบอร์โทรศัพท์อย่างน้อยหนึ่งเบอร์'])
            del cleaned_data['cell_phone_number']
        
        return cleaned_data

@submitted_applicant_required
def student_registration(request):

    return HttpResponseForbidden()

    applicant = request.applicant
    admitted = applicant.is_admitted()

    if not admitted:
        raise Http404

    registration = applicant.get_student_registration()

    if request.method=='POST':
        form = StudentRegistrationForm(request.POST,
                                       instance=registration)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.applicant = applicant
            registration.save()
            return redirect('status-index')
    else:
        form = StudentRegistrationForm(instance=registration)

    return render_to_response('confirmation/student_registration.html',
                              { 'applicant': applicant,
                                'form': form })


def save_best_admission_major_pref(applicant, 
                                   admission_round, 
                                   admission_result):
    AdmissionMajorPreference.objects.filter(applicant=applicant,
                                            round_number=admission_round.number).delete()
    pref = AdmissionMajorPreference.new_for_applicant(applicant,
                                                      admission_result=admission_result)
    pref.round_number = admission_round.number
    pref.save()


def save_waive_admission_major_pref(applicant, 
                                    admission_round):
    AdmissionMajorPreference.objects.filter(applicant=applicant,
                                            round_number=admission_round.number).delete()
    preferred_majors = applicant.preference.get_major_list()

    pref = AdmissionMajorPreference(applicant=applicant,
                                    round_number=admission_round.number)
    pref.is_accepted_list = [0]*len(preferred_majors)
    pref.set_ptype_cache()


@submitted_applicant_required
def main(request, is_edit_registration=False):
    if settings.SHOW_ONLY_RESULTS:
        return HttpResponseForbidden()

    applicant = request.applicant
    admitted = applicant.is_admitted()

    if not admitted:
        return HttpResponseForbidden()

    first_admission = (applicant.admission_results.count() == 1)
    if not first_admission:
        return HttpResponseForbidden()

    current_round = AdmissionRound.get_recent()
    round_number = current_round.number
    is_last_round = False

    # check for deadline
    if admission_major_pref_deadline_passed():
        return render_to_response('confirmation/pref_deadline_passed.html',
                                  {'admission_round': current_round})

    admission_result = applicant.get_latest_admission_result()

    preferred_majors = applicant.preference.get_major_list()
    higher_majors = get_higher_ranked_majors(preferred_majors, 
                                             admission_result.admitted_major)
    is_best_major = (len(higher_majors)==0)

    if AdmissionWaiver.is_waived(applicant):
        waiver = applicant.admission_waiver
    else:
        waiver = None

    registration = applicant.get_student_registration()
    if request.method=='GET' and registration and not is_edit_registration and not is_best_major:
        return redirect('confirmation-pref')

    if request.method=='POST' and 'confirm' in request.POST:
        form = StudentRegistrationForm(request.POST,
                                       instance=registration)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.applicant = applicant
            registration.save()

            AdmissionConfirmation.create_for(applicant,
                                             current_round.number)

            send_admission_confirmation_by_email(applicant)

            if not is_best_major:
                Log.create("Confirm applicant %s from %s" % 
                           (applicant.id,request.META['REMOTE_ADDR']),
                           applicant_id=applicant.id)

                return redirect('confirmation-pref')
            else:
                Log.create("Confirm applicant %s (for best) from %s" % 
                           (applicant.id,request.META['REMOTE_ADDR']),
                           applicant_id=applicant.id)

                save_best_admission_major_pref(applicant, 
                                               current_round,
                                               admission_result)
                return redirect('status-index')

    elif request.method=='POST' and 'waive' in request.POST:

        AdmissionWaiver.waive_applicant(applicant)
        if registration:
            registration.delete()
        AdmissionConfirmation.delete_for(applicant,
                                         current_round.number)
        save_waive_admission_major_pref(applicant,
                                        current_round)

        Log.create("Waive applicant %s from %s" % 
                   (applicant.id,request.META['REMOTE_ADDR']),
                   applicant_id=applicant.id)

        send_admission_waive_by_email(applicant)

        request.session['notice'] = u'คุณได้สละสิทธิ์การเข้าศึกษาต่อผ่านโครงการรับตรงแล้ว'
        return redirect('status-index')
        
    elif request.method=='POST' and 'unwaive' in request.POST:

        AdmissionWaiver.unwaive_applicant(applicant)
        AdmissionMajorPreference.objects.filter(applicant=applicant,
                                                round_number=current_round.number).delete()

        Log.create("Unwaive applicant %s from %s" % 
                   (applicant.id,request.META['REMOTE_ADDR']),
                   applicant_id=applicant.id)

        send_admission_unwaive_by_email(applicant)

        return redirect('confirmation-app-index')

    elif request.method=='POST' and 'cancel' in request.POST:
        return redirect('status-index')

    else:
        form = StudentRegistrationForm(instance=registration)

    return render_to_response('confirmation/index.html',
                              { 'applicant': applicant,
                                'admission_result': admission_result,
                                'current_round': current_round,
                                'is_last_round': is_last_round,
                                'is_best_major': is_best_major,
                                'registration': registration,
                                'waiver': waiver,
                                'form': form,
                                'can_log_out': True})


def quota_choice(request, applicant, admission_result):
    current_round = AdmissionRound.get_recent()
    round_number = current_round.number

    additional_result = applicant.additional_result
    is_result_for_current_round = (additional_result.round_number == round_number)
    can_edit = (not admission_major_pref_deadline_passed()) and is_result_for_current_round

    student_registration = applicant.get_student_registration()

    if request.method=='POST' and not can_edit:
        return render_to_response('confirmation/pref_deadline_passed.html',
                                  {'admission_round': current_round})

    if request.method=='POST':
        if request.POST['major_select']=='quota':
            AdmissionWaiver.waive_applicant(applicant)
            Log.create("Waive applicant %s to quota from %s" % 
                       (applicant.id, request.META['REMOTE_ADDR']),
                       applicant_id=applicant.id)
            return redirect('status-index')           

        if request.POST['major_select']=='direct':
            additional_result.is_waived = True
            additional_result.save()
            Log.create("Waive applicant %s to direct from %s" % 
                       (applicant.id, request.META['REMOTE_ADDR']),
                       applicant_id=applicant.id)
            return redirect('status-index')           

    return render_to_response('confirmation/quota/choices.html',
                              { 'applicant': applicant,
                                'admission_result': admission_result,
                                'additional_result': additional_result,
                                'student_registration': student_registration,
                                'can_edit': can_edit,
                                'can_log_out': True })
@applicant_required
def quota_confirm(request):
    """
    confirmation page for quota-only applicants
    """
    applicant = request.applicant

    if not applicant.has_additional_result:
        return HttpResponseForbidden()

    current_round = AdmissionRound.get_recent()
    round_number = current_round.number

    admission_result = applicant.get_latest_admission_result()

    if admission_result and not AdmissionWaiver.is_waived(applicant):
        return quota_choice(request, applicant, admission_result)

    additional_result = applicant.additional_result
    is_result_for_current_round = (additional_result.round_number == round_number)

    can_edit = (not admission_major_pref_deadline_passed()) and is_result_for_current_round

    registration = applicant.get_student_registration()

    if request.method=='POST' and not can_edit:
        return render_to_response('confirmation/pref_deadline_passed.html',
                                  {'admission_round': current_round})

    if request.method=='POST' and 'submit' in request.POST:
        form = StudentRegistrationForm(request.POST,
                                       instance=registration)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.applicant = applicant
            registration.save()
            return redirect('confirmation-quota-index')
    elif request.method=='POST' and 'waive' in request.POST:
        if registration:
            registration.delete()
        return redirect('confirmation-quota-index')
    else:
        form = StudentRegistrationForm(instance=registration)

    return render_to_response('confirmation/quota/student_registration.html',
                              { 'applicant': applicant,
                                'can_edit': can_edit,
                                'form': form,
                                'additional_result': additional_result,
                                'admission_result': admission_result,
                                'registration': registration,
                                'can_log_out': True })

@applicant_required
def quota_reset_choice(request):
    """
    reset choice between quota & direct
    """
    applicant = request.applicant

    if not applicant.has_additional_result:
        return HttpResponseForbidden()
    additional_result = applicant.additional_result

    current_round = AdmissionRound.get_recent()
    round_number = current_round.number

    admission_result = applicant.get_latest_admission_result()

    if not admission_result: 
        return HttpResponseForbidden()
    
    if request.method!='POST':
        return HttpResponseForbidden()

    # remove from quota waived
    AdmissionWaiver.unwaive_applicant(applicant)

    # remove from direct waived
    additional_result.is_waived = False
    additional_result.save()
    AdmissionConfirmation.delete_for(applicant,
                                     current_round.number)
    AdmissionMajorPreference.objects.filter(applicant=applicant,
                                            round_number=current_round.number).delete()

    registration = applicant.get_student_registration()
    if registration:
        registration.delete()

    Log.create("Reset quota/direct waiver applicant %s from %s" % 
               (applicant.id, request.META['REMOTE_ADDR']),
               applicant_id=applicant.id)

    return redirect('status-index')
