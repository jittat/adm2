# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django import forms

from commons.utils import serve_file

from application.models import Applicant, Education, Major, MajorPreference
from application.models import SubmissionInfo, PersonalInfo
#from upload.models import AppDocs
#from manual.models import AdminEditLog

from commons.email import send_validation_successful_by_email
from commons.email import send_validation_error_by_email
from commons.email import send_resubmission_reminder_by_email

from commons.models import Log

from models import ReviewField, ReviewFieldResult, CompletedReviewField
#from supplement.models import Supplement
from confirmation.models import AdmissionConfirmation
from result.models import NIETSScores

def find_basic_statistics():
    total_submitted_app_count = SubmissionInfo.objects.count()
    paid_app_count = SubmissionInfo.objects.filter(is_paid=True).count()
    imported_app_count = NIETSScores.objects.filter(is_request_successful=True).count()
    imported_problem_app_count = NIETSScores.objects.filter(is_request_successful=False).count()
    ready_app_count = Applicant.get_ready_applicants().count()
    stat = {
        'online_app_registered': Applicant.objects.count(),
        'app_ready': ready_app_count,
        'app_submitted': total_submitted_app_count,
        'app_paid':  paid_app_count,
        'app_imported': imported_app_count,
        'app_imported_problem': imported_problem_app_count,
        }
    return stat

@login_required
def index(request):
    stat = find_basic_statistics()
    return render_to_response("review/index.html",
                              { 'stat': stat })

class ApplicantSearchByIDForm(forms.Form):
    national_id = forms.IntegerField(required=False,
                                     widget=forms.TextInput(attrs={'size':10}))
    full_name = forms.CharField(required=False)
    verification_number = forms.CharField(required=False)

def find_applicants(form):
    national_id = form.cleaned_data['national_id']
    if national_id:
        national_id = str(national_id)
    full_name = form.cleaned_data['full_name']
    applicants = Applicant.objects.all()
    if national_id:
        if len(national_id)==13:
            applicants = applicants.filter(national_id=national_id)
        else:
            applicants = applicants.filter(national_id__startswith=national_id)

    if full_name:
        items = full_name.strip().split(' ')
        if items[0]!='':
            applicants = applicants.filter(first_name__contains=items[0])
            if len(items)>1 and items[1]!='':
                applicants = applicants.filter(last_name__contains=items[1])
        return applicants[:200]
    else:
        return applicants[:200]

def put_minimal_info_to_applicants(applicants):

    def ticket_number(self):
        return '-'
    def verification_number(self):
        return '-'

    import new

    for applicant in applicants:
        applicant.ticket_number = new.instancemethod(ticket_number,applicant)
        applicant.verification_number = new.instancemethod(verification_number,applicant)
        applicant.is_submitted = False

@login_required
def verify_ticket(request):

    if 'notice' in request.session:
        notice = request.session['notice']
        del request.session['notice']
    else:
        notice = ''
    
    applicants = []
    results = []

    if request.method=='POST':
        form = ApplicantSearchByIDForm(request.POST)
        if form.is_valid():
            verinum = form.cleaned_data['verification_number']

            applicants = find_applicants(form)

            # when there are too many results, put empty stub to
            # prevent huge database load.
            if (not type(applicants)==list) and (applicants.count()>20):
                put_minimal_info_to_applicants(applicants)

            if applicants != None and len(applicants) > 0:
                if (('search-and-show' in request.POST) 
                    and (len(applicants)==1) and (applicants[0].is_submitted)):
                    return HttpResponseRedirect(reverse('review-show-app',
                                                        args=[applicants[0].id]))

                for applicant in applicants:
                    match_verinum = (applicant.is_submitted and
                        applicant.verification_number().startswith(verinum))
                    results.append({ 'verinum': match_verinum })
    else:
        form = ApplicantSearchByIDForm()

    return render_to_response("review/ticket_search.html",
                              { 'form': form,
                                'notice': notice,
                                'applicants_results': zip(applicants,results),
                                'user': request.user })


class ApplicantSearchForm(forms.Form):
    school_name = forms.CharField(label="โรงเรียน", required=False)

@login_required
def search(request):
    applicants = []
    display = {}
    applicant_count = 0
    if request.method=='POST':
        form = ApplicantSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['school_name']!='':
                educations = (Education.objects.filter(
                        school_name__contains=form.cleaned_data['school_name'])
                              .select_related(depth=1))
                applicant_count = educations.count()

                # only show the first 100
                educations = educations.all()[:200]

                for e in educations:
                    app = e.applicant
                    app.education = e
                    applicants.append(app)
                display['edu'] = True
    else:
        form = ApplicantSearchForm()

    return render_to_response("review/search.html",
                              { 'form': form,
                                'applicant_count': applicant_count,
                                'applicants': applicants,
                                'display': display,
                                'force_review_link': True })


@login_required
def toggle_received_status(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    submission_info = applicant.submission_info
    
    if not applicant.online_doc_submission():
        submission_info.toggle_doc_received_at()

        return render_to_response("review/include/doc_received_status_block.html",
                                  {'has_received_doc':
                                       submission_info.has_received_doc()})

    return HttpResponseForbidden()


@login_required
def generate_password(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    if not (applicant.can_password_be_generated() and request.user.is_staff):
        return HttpResponseForbidden()

    new_password = applicant.random_password()
    applicant.save()
    submission_info = applicant.submission_info

    log = Log.create("Generated password: %s" % (applicant_id,),
                     request.user.username,
                     applicant_id=int(applicant_id),
                     applicantion_id=submission_info.applicantion_id)
    
    return render_to_response("review/password_generated.html",
                              { 'applicant': applicant,
                                'password': new_password })

def get_applicant_doc_name_list(applicant):
    names = []
    #names.append('picture')
    names.append('nat_id')
    #names.append('edu_certificate')
    if applicant.education.uses_gat_score:
        names.append('gat_score')
        names.append('pat1_score')
        names.append('pat3_score')
    else:
        names.append('anet_score')
    names.append('app_fee_doc')
    #names.append('abroad_edu_certificate')
    return names


def prepare_applicant_review_results(applicant, names):
    submitted_review_results = (ReviewFieldResult.
                                get_applicant_review_results(applicant))
    result_dict = {}
    for result in submitted_review_results:
        field_id = result.review_field_id
        field = ReviewField.get_field_by_id(field_id)
        result_dict[field.short_name] = result

    # reorganize the results, add None result when needed
    review_results = []
    for n in names:
        if n in result_dict:
            review_results.append(result_dict[n])
        else:
            review_results.append(None)
    return review_results

def prepare_applicant_review_fields(names):
    return [ReviewField.get_field_by_short_name(n)
            for n in names]

class ReviewResultForm(forms.Form):
    is_passed = forms.BooleanField(required=False)
    applicant_note = forms.CharField(required=False)
    internal_note = forms.CharField(required=False)
    is_submitted = forms.BooleanField(required=False)

def prepare_applicant_forms(applicant, names, results, post_data=None):
    forms = []
    for n, res in zip(names, results):
        if res!=None:
            initial={'is_passed': res.is_passed,
                     'applicant_note': res.applicant_note,
                     'internal_note': res.internal_note,
                     'is_submitted': True }
        else:
            initial=None
        forms.append(ReviewResultForm(post_data,
                                      prefix=n,
                                      initial=initial))
    return forms

def build_review_data(fields, results, forms, completed_review_fields):
    completed_names = [f.short_name for f in completed_review_fields]
    data = [ { 'field': field,
               'result': result,
               'form': form,
               'completed': field.short_name in completed_names } 
             for field, result, form 
             in zip(fields, results, forms) ]

    return data

def prepare_applicant_review_data(applicant):
    field_names = get_applicant_doc_name_list(applicant)
    completed_review_fields = CompletedReviewField.get_for_applicant(applicant)
    fields = prepare_applicant_review_fields(field_names)
    results = prepare_applicant_review_results(applicant, field_names)
    forms = prepare_applicant_forms(applicant, field_names, results)
    return build_review_data(fields, results, forms, completed_review_fields)

@login_required
def review_document(request, applicant_id, return_to_manual=False):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    submission_info = applicant.submission_info

    if not submission_info.can_be_reviewed():
        request.session['notice'] = 'ยังไม่สามารถตรวจสอบเอกสารได้เนื่องจากยังไม่พ้นช่วงเวลาสำหรับการแก้ไข'
        return HttpResponseRedirect(reverse('review-ticket'))

    if (request.method=='POST') and ('submit' in request.POST):

        if not request.user.has_perm('review.change_reviewfieldresult'):
            request.session['notice'] = 'คุณไม่สามารถแก้ข้อมูลได้ในขณะนี้'
            return HttpResponseRedirect(reverse('review-ticket'))

        # auto set received flag
        submission_info.set_doc_received_at_now_if_not()

        log_messages = []

        field_names = get_applicant_doc_name_list(applicant)
        fields = prepare_applicant_review_fields(field_names)
        results = prepare_applicant_review_results(applicant, field_names)
        forms = prepare_applicant_forms(applicant, field_names, results, request.POST)

        completed_review_fields = CompletedReviewField.get_for_applicant(applicant)
        completed_names = [rf.short_name for rf in completed_review_fields]

        error = False
        for f in forms:
            if not f.is_valid():
                error = True

        if not error:
            failed_fields = []

            for field, result, form in zip(fields, results, forms):
                if field.short_name in completed_names:
                    # skip completed review fields
                    continue

                if not result:
                    old_value = '-'    # for logging
                    result = ReviewFieldResult()
                else:
                    old_value = result.is_passed

                result.applicant_note = form.cleaned_data['applicant_note']
                result.internal_note = form.cleaned_data['internal_note']

                result.review_field = field
                result.applicant = applicant

                if (field.required) or (form.cleaned_data['is_submitted']):
                    result.is_passed = form.cleaned_data['is_passed']
                    new_value = str(int(form.cleaned_data['is_passed']))
                    if result.id!=None:
                        result.save(force_update=True)
                    else:
                        result.save(force_insert=True)

                    if not result.is_passed:
                        failed_fields.append((field,result))
                else:
                    new_value = '-'
                    if result.id!=None:
                        result.delete()

                log_messages.append('%d:%s-%s' %
                                    (field.id, old_value, new_value))

            submission_info.has_been_reviewed = True
            submission_info.doc_reviewed_at = datetime.now()
            submission_info.doc_reviewed_complete = (len(failed_fields)==0)
            submission_info.save()

            # add a log entry
            log = Log.create("Review doc: " + '; '.join(log_messages),
                             request.user.username,
                             applicant_id=int(applicant_id),
                             applicantion_id=submission_info.applicantion_id)

            if submission_info.doc_reviewed_complete:
                send_validation_successful_by_email(applicant)
                request.session['notice'] = 'จัดเก็บและแจ้งผลการตรวจว่าผ่านกับผู้สมัครแล้ว'
            else:
                send_validation_error_by_email(applicant, failed_fields)
                request.session['notice'] = 'จัดเก็บและแจ้งผลการตรวจว่าหลักฐานไม่ผ่านกับผู้สมัครแล้ว'
            if not return_to_manual:
                return HttpResponseRedirect(reverse('review-ticket'))
            else:
                return HttpResponseRedirect(reverse('manual-index'))
    elif 'cancel' in request.POST:
        request.session['notice'] = 'ยกเลิกการตรวจสอบ ผลตรวจทุกอย่างคงเดิม'
        #print return_to_manual
        if not return_to_manual:
            return HttpResponseRedirect(reverse('review-ticket'))
        else:
            return HttpResponseRedirect(reverse('manual-index'))
    else:
        data = prepare_applicant_review_data(applicant)

    if applicant.online_doc_submission():
        appdocs = applicant.appdocs
    else:
        appdocs = None
        
    can_request_password = request.user.is_staff and applicant.can_password_be_generated()
    return render_to_response("review/show.html",
                              { 'applicant': applicant,
                                'appdocs': appdocs,
                                'submission_info': submission_info,
                                'review_data': data,
                                'can_request_password': can_request_password })


def get_applicants_from_submission_infos(submission_infos):
    applicants = []
    for s in submission_infos:
        app = s.applicant
        app.submission_info = s
        applicants.append(app)
    return applicants


@login_required
def auto_review_all_apps(request):
    submission_infos = SubmissionInfo.objects.filter(doc_received_at__isnull=False).filter(has_been_reviewed=False).select_related(depth=1)
    applicants = get_applicants_from_submission_infos(submission_infos)

    passed_count = 0

    for applicant in applicants:
        doc_name_list = get_applicant_doc_name_list(applicant)
        completed_review_fields = CompletedReviewField.get_for_applicant(applicant)
        completed_names = set([rf.short_name for rf in completed_review_fields])
        failed = False
        for field in doc_name_list:
            if field not in completed_names:
                failed = True
                break
        if failed:
            continue

        # have already submitted all doc from round 1
        passed_count += 1

        submission_info = applicant.submission_info
        submission_info.has_been_reviewed = True
        submission_info.doc_reviewed_at = datetime.now()
        submission_info.doc_reviewed_complete = True
        submission_info.save()

        # add a log entry
        log = Log.create("Auto review doc",
                         request.user.username,
                         applicant_id=int(applicant.id),
                         applicantion_id=submission_info.applicantion_id)
        send_validation_successful_by_email(applicant)

    request.session['notice'] = 'ตรวจผ่านทั้งสิ้น %d คน' % (passed_count,)
    return HttpResponseRedirect(reverse('review-ticket'))


def get_applicants_using_update_review_time_diff(time_diff, review_status=None):
    where_condition = ("ADDTIME(`last_updated_at`,'%s') >= `doc_reviewed_at`" 
                       % time_diff)
    submission_infos = (SubmissionInfo
                        .objects
                        .extra(where=[where_condition])
                        .select_related(depth=1))
    if review_status!=None:
        submission_infos = (
            submission_infos.filter(doc_reviewed_complete=review_status))
    return get_applicants_from_submission_infos(submission_infos)


def build_search_title(paid, score_imported):
    t = u'รายการผู้สมัครที่ส่งใบสมัครแล้ว'
    if paid!=None:
        if paid:
            t += u' ที่ชำระเงินแล้ว'
        else:
            t += u' ที่ยังไม่ได้ชำระเงิน'
    if score_imported!=None:
        if score_imported:
            t += u' ที่นำเข้าคะแนนสอบแล้ว'
        else:
            t += u' ที่การนำเข้าคะแนนสอบมีปัญหา'
    return t


APPLICANTS_PER_PAGE = 200

@login_required
def list_applicant(request, paid=None, score_imported=None, pagination=True):
    applicants = []
    display = {}
    submission_infos = SubmissionInfo.objects.order_by('-submitted_at').select_related(depth=1)

    if paid!=None:
        submission_infos = submission_infos.filter(is_paid=paid)
    if score_imported!=None:
        submission_infos = submission_infos.filter(applicant__NIETS_scores__is_request_successful=score_imported)

    title = build_search_title(paid, score_imported)

    applicant_count = submission_infos.count()

    if pagination:
        max_page = (applicant_count + APPLICANTS_PER_PAGE -1) / APPLICANTS_PER_PAGE
        page = 1
        if 'page' in request.GET:
            try:
                page = int(request.GET['page'])
            except:
                page = 1
        if page < 1 or page > max_page:
            page = 1
    else:
        max_page = 1
        page = 1

    display_start = APPLICANTS_PER_PAGE * (page - 1) + 1
    display_end = APPLICANTS_PER_PAGE * page
    submission_infos = submission_infos.all()[display_start-1:display_end]
    display_count = len(submission_infos)

    applicants = get_applicants_from_submission_infos(submission_infos)

    display['ticket_number']=True
    display['payment_status']=True
    if score_imported!=None:
        display['score_import_status']=True

    return render_to_response("review/search.html",
                              { 'form': None,
                                'applicant_count': applicant_count,
                                'applicants': applicants,
                                'force_review_link': True,
                                'pagination': pagination,
                                'display_start': display_start,
                                'display_end': display_end,
                                'display_count': display_count,
                                'page': page,
                                'max_page': max_page,
                                'display': display,
                                'title': title })

@login_required
def list_applicants_with_supplements(request, time_diff=None, review_status=False):
    if time_diff == None:
        time_diff = '00:01:00'

    applicants = get_applicants_using_update_review_time_diff('00:01:00',
                                                              review_status)
    applicant_count = len(applicants)

    if review_status == None: 
        title = "รายชื่อผู้สมัครที่ยื่นหลักฐานเพิ่มหลังจากตรวจสอบแล้ว"
    elif review_status == False:
        title = "รายชื่อผู้สมัครที่หลักฐานไม่ผ่านที่ยื่นหลักฐานเพิ่มหลังจากตรวจสอบแล้ว"

    return render_to_response("review/list_applicants_with_supplements.html",
                              { 'form': None,
                                'list_title': title,
                                'applicant_count': applicant_count,
                                'applicants': applicants,
                                'force_review_link': True,
                                'display': 
                                { 'ticket_number': True,
                                  'doc_reviewed_at': True,
                                  'doc_reviewed_complete': True }})


@login_required
def list_incomplete_applicants(request, submission_method=None):
    submission_infos = (SubmissionInfo
                        .get_incomplete_submissions()
                        .select_related(depth=1))

    applicants = get_applicants_from_submission_infos(submission_infos)

    submission_method_name = ''
    if submission_method=='postal':
        submission_method_name = 'ที่สมัครออนไลน์แต่ส่งหลักฐานทางไปรษณีย์'
        applicants = [a for a in applicants 
                      if a.doc_submission_method==Applicant.SUBMITTED_BY_MAIL]
    elif submission_method=='offline':
        submission_method_name = 'ที่สมัครและส่งหลักฐานทางไปรษณีย์ (offline)'
        applicants = [a for a in applicants 
                      if a.doc_submission_method==Applicant.SUBMITTED_OFFLINE]
    elif submission_method=='online':
        submission_method_name = 'ที่สมัครและส่งหลักฐานออนไลน์ทั้งหมด'
        applicants = [a for a in applicants 
                      if a.doc_submission_method==Applicant.SUBMITTED_ONLINE]
        

    applicant_count = len(applicants)

    notice = ''

    can_send_reminder_emails = (request.user.is_superuser and 
                                submission_method != 'offline')

    if (request.method=='POST') and (can_send_reminder_emails):
        # form submission, now send e-mail
        for app in applicants:
            send_resubmission_reminder_by_email(app)
        notice = ("ส่งอีเมล์เตือน %d ฉบับแล้ว" % (applicant_count,))

    return render_to_response("review/list_incomplete_for_email.html",
                              { 'form': None,
                                'notice': notice,
                                'submission_method_name':
                                    submission_method_name,
                                'can_send_reminder_emails':
                                    can_send_reminder_emails,
                                'applicant_count': applicant_count,
                                'applicants': applicants,
                                'force_review_link': True,
                                'display':
                                    { 'ticket_number': True,
                                      'doc_reviewed_at': True,
                                      'doc_reviewed_complete': True }})

@login_required
def list_applicants_with_potential_edu_update_hazard(request):
    update_timestamps = {}
    review_timestamps = {}

    for education in Education.objects.all():
        update_timestamps[education.applicant_id] = education.updated_at

    for submission_info in SubmissionInfo.objects.all():
        review_timestamps[submission_info.applicant_id] = (
            submission_info.doc_reviewed_at)

    ten_minutes = timedelta(minutes=10)

    potential_list = []

    for app_id, review_timestamp in review_timestamps.iteritems():
        if app_id in update_timestamps:
            update_timestamp = update_timestamps[app_id]
            if ((update_timestamp != None) and (review_timestamp != None)
                and (update_timestamp + ten_minutes > review_timestamp)):
                potential_list.append((app_id, update_timestamp))

    all_applicants = [(Applicant.objects.get(pk=app_id), update_timestamp) 
                      for app_id, update_timestamp in potential_list]

    applicants = []
    for app, update_timestamp in all_applicants:
        if app.doc_submission_method != Applicant.SUBMITTED_OFFLINE:
            admin_log = AdminEditLog.objects.filter(applicant=app)
            is_manual_update = (len(admin_log) != 0)

            app.update_info = {
                'updated_at': update_timestamp,  # HACK: add field to display
                'is_manual_update': is_manual_update,
                }
            applicants.append(app)

    applicant_count = len(applicants)

    return render_to_response(
        "review/list_applicants_with_potential_edu_update_hazard.html",
        { 'form': None,
          'applicant_count': applicant_count,
          'applicants': applicants,
          'force_review_link': True,
          'display': 
          { 'ticket_number': True,
            'update_info': True,
            'doc_reviewed_at': True,
            'doc_reviewed_complete': True }})

def build_model_dict(join_model):
    d = {}
    for data in join_model.objects.all():
        d[data.applicant_id] = data
    return d

def dump_fields(applicant, fields):
    items = []
    for f in fields:
        fdata = applicant.__getattribute__(f)
        if hasattr(fdata,'__call__'):
            items.append(unicode(fdata()))
        else:
            items.append(unicode(fdata))
    return u','.join(items)
            
@login_required
def list_qualified_applicants(request, download=True):
    submission_infos = (SubmissionInfo
                        .get_qualified_submissions()
                        .select_related(depth=1)
                        .all())
    applicants = get_applicants_from_submission_infos(submission_infos)

    personal_infos = build_model_dict(PersonalInfo)
    # added more info to applicants
    for a in applicants:
        if a.id in personal_infos:
            a.national_id = personal_infos[a.id].national_id
    
    FIELD_LIST = [
        'ticket_number', 
        'first_name', 
        'last_name', 
        'get_doc_submission_method_display', 
        'national_id' ]

    output_list = []
    for a in applicants:
        output_list.append(dump_fields(a, FIELD_LIST))
    output = u'\n'.join(output_list)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=applicants.csv'
    response.write(output)

    return response


############################################################
# views for displaying documents and supplements
#

IMG_MAX_HEIGHT = 450
IMG_MAX_WIDTH = 800

def cal_zoom_size(field):
    if field:
        height = field.height
        width = field.width
    else:
        height = 1
        width = 1

    hscale = float(height) / IMG_MAX_HEIGHT
    wscale = float(width) / IMG_MAX_WIDTH

    if (hscale > 1) or (wscale > 1):
        zoomable = True
        if hscale > wscale:
            new_h = IMG_MAX_HEIGHT
            new_w = int(width / hscale)
        else:
            new_h = int(height / wscale)
            new_w = IMG_MAX_WIDTH
    else:
        zoomable = False
        new_h, new_w = height, width

    return new_h, new_w, zoomable


@login_required
def doc_view(request, applicant_id, field_name):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    docs = applicant.get_applicant_docs_or_none()
    if not AppDocs.valid_field_name(field_name):
        return HttpResponseNotFound()

    field = docs.__getattribute__(field_name)

    ext = ''
    if field:
        filename = docs.__getattribute__(field_name).name
        if filename:
            name, ext = os.path.splitext(filename)
    if ext=='':
        ext = '.png'

    new_h, new_w, zoomable = cal_zoom_size(field)

    filename = '%s%s' % (field_name, ext)
    return render_to_response("review/doc_view.html",
                              { 'applicant': applicant,
                                'field_name': field_name,
                                'filename': filename,
                                'height': new_h,
                                'width': new_w,
                                'zoomable': zoomable })

@login_required
def supplement_view(request, supplement_id):
    supplement = get_object_or_404(Supplement, pk=supplement_id)

    name, ext = os.path.splitext(supplement.image.name)
    filename = '%s%s' % (supplement_id, ext)

    new_h, new_w, zoomable = cal_zoom_size(supplement.image)

    return render_to_response("review/supplement_view.html",
                              { 'applicant': supplement.applicant,
                                'supplement': supplement,
                                'filename': filename,
                                'height': new_h,
                                'width': new_w,
                                'zoomable': zoomable })


@login_required
def doc_img_view(request, applicant_id, filename):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    docs = applicant.get_applicant_docs_or_none()

    if docs!=None:
        field_name, ext = os.path.splitext(filename)

        if not AppDocs.valid_field_name(field_name):
            return HttpResponseNotFound()

        try:
            full_path = docs.__getattribute__(field_name).path

            if os.path.exists(full_path):
                return serve_file(full_path)
            else:
                return HttpResponseNotFound()
        except ValueError:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()


@login_required
def supplement_img_view(request, filename):
    fname, ext = os.path.splitext(filename)

    try:
        supplement_id = int(fname)
    except:
        return HttpResponseForbidden()

    supplement = get_object_or_404(Supplement, pk=supplement_id)

    try:
        full_path = supplement.image.path
        
        if os.path.exists(full_path):
            return serve_file(full_path)
        else:
            return HttpResponseNotFound()
    except ValueError:
        return HttpResponseNotFound()

@login_required
def show_applicant(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    try:
        submission_info = applicant.submission_info
    except:
        submission_info = None
    
    from application.views.status import prepare_exam_scores

    exam_scores = prepare_exam_scores(applicant)

    admission_results = applicant.admission_results.all()
    confirmations = AdmissionConfirmation.objects.filter(applicant=applicant).all()

    return render_to_response("review/show_app.html",
                              { 'applicant': applicant,
                                'submission_info': submission_info,
                                'exam_scores': exam_scores,
                                'admission_results': admission_results,
                                'confirmations': confirmations })

@login_required
def export_app_nat_id(request):

    from datetime import datetime

    filename = "req" + datetime.now().strftime("%Y%m%d%H%M") + ".csv"

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    data = ["No,CITIZENID,Name,SurName\n"]
    applicants = Applicant.objects.filter(NIETS_scores=None).all()

    submitted_ids = set([s.applicant_id for s in SubmissionInfo.objects.all()])

    counter = 1
    for a in applicants:
        if a.id in submitted_ids:
            data.append('"%d","%s","%s","%s"\n' %
                        (counter, a.national_id, a.first_name, a.last_name))
            counter += 1

    response.write(''.join(data))

    return response


class ScoreUploadForm(forms.Form):
    file = forms.FileField(label=u'ไฟล์ csv ของคะแนนสอบ')

@login_required
def import_niets_scores(request, testing=True):

    from score_import import score_import, test_score_import

    result = ""
    if request.method == 'POST':
        form = ScoreUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if testing:
                imported_applicants = test_score_import(request.FILES['file'])
                new_form = ScoreUploadForm()
                return render_to_response("review/score_import_test_result.html",
                                          { 'form': new_form,
                                            'applicants': imported_applicants,
                                            'message': "" })
            else:
                result = score_import(request.FILES['file'])
        else:
            if not testing:
                test_result = None
                message = u'เกิดข้อผิดพลาดในการกรอกฟอร์ม (เช่นลืมเลือกแฟ้มข้อมูล) ทำให้ตัวอย่างผลลัพธ์ของการนำเข้าไม่แสดง แต่ถ้าคุณแน่ใจว่าการทดสอบการนำเข้าทำงานได้ถูกต้อง คุณสามารถนำเข้าข้อมูลใหม่ได้'
                return render_to_response("review/score_import_test_result.html",
                                          { 'form': form,
                                            'test_result': test_result,
                                            'message': message })                
    else:
        form = ScoreUploadForm()

    return render_to_response("review/score_import.html",
                              { 'form': form,
                                'result': result })

@login_required
def create_payment(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    try:
        submission_info = applicant.submission_info
    except:
        submission_info = None

    if submission_info and (not submission_info.is_paid):
        submission_info.is_paid = True
        submission_info.paid_at = datetime.now()
        submission_info.save()

        log = Log.create("Manual accept payment: %s (%s)" % 
                         (applicant_id, applicant.national_id),
                         request.user.username,
                         applicant_id=int(applicant_id))

    return redirect('review-show-app',applicant_id)


@login_required
def show_major_pref_stat(request):
    all_submission_infos = SubmissionInfo.objects.all()
    submitted_ids = set([s.applicant_id for s in all_submission_infos])

    from django.conf import settings
    max_rank = settings.MAX_MAJOR_RANK

    majors = Major.get_all_majors()
    major_stat = dict([(int(m.number), {'major': m, 'stat': [0]*max_rank})
                       for m in majors])

    all_major_prefs = MajorPreference.objects.all()
    for mp in all_major_prefs:
        if mp.applicant_id in submitted_ids:
            r = 0
            for m in mp.majors:
                major_stat[m]['stat'][r] += 1
                r += 1

    major_stat_data = [(major_stat[m]['major'], major_stat[m]['stat']) for
                       m in sorted(major_stat.keys())]
    return render_to_response('review/major_pref_stat.html',
                              { 'ranks': range(1,max_rank+1),
                                'major_stat_data': major_stat_data })

