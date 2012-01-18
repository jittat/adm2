# -*- coding: utf-8 -*-

from django.conf import settings

from application.models import Major, MajorPreference, Education
from application.models import Address, ApplicantAddress
from application.forms import EducationForm, PersonalInfoForm
from application.forms import AddressForm
from quota.models import AdditionalEducation
from quota.forms import QuotaForm

def extract_ranks(post_data, major_list):
    """
    extracts a list of majors from post data.  Each select list has an
    id of the form 'major_ID'.
    """
    
    rank_dict = {}
    for m in major_list:
        sel_id = m.select_id()
        if sel_id in post_data:
            r = post_data[sel_id]
            try:
                rnum = int(r)
            except:
                rnum = -1
            if (rnum >= 1) and (rnum <= settings.MAX_MAJOR_RANK):
                rank_dict[rnum] = int(m.number)

    ranks = []
    for r in sorted(rank_dict.keys()):
        ranks.append(rank_dict[r])
    return ranks

def assign_major_pref_to_applicant(applicant, pref_list):
    if applicant.has_major_preference():
        preference = applicant.preference
    else:
        preference = MajorPreference()
            
    preference.majors = [int(m.number) for m in pref_list]

    preference.applicant = applicant
    preference.save()
    applicant.add_related_model('major_preference',
                                save=True,
                                smart=True)

def handle_major_form(request, max_major_rank, applicant=None):
    if applicant==None:
        applicant = request.applicant

    majors = Major.get_all_majors()
    mdict = dict([(int(m.number),m) for m in majors])

    errors = None

    pref_list = []
    used = set()
    is_dupplicate = False
    for r in range(1, max_major_rank+1):
        name = "major-%d" % r
        try:
            major_num = int(request.POST[name])
            if major_num!=0:
                if major_num not in used:
                    pref_list.append(mdict[major_num])
                    used.add(major_num)
                else:
                    is_dupplicate = True
        except:
            pass

    if len(pref_list)==0:
        # chooses no majors
        errors = ['ต้องเลือกอย่างน้อยหนึ่งอันดับ']
    elif is_dupplicate:
        errors = ['เลือกสาขาซ้ำกันในสองอันดับ กรุณาเลือกใหม่ ระบบได้ตัดสาขาที่ซ้ำกันทิ้งให้แล้ว']
    else:
        assign_major_pref_to_applicant(applicant, pref_list)
        return (True, pref_list, None)

    return (False, pref_list, errors)


def handle_basic_form_save(form_class, field_name, request, old_data, 
                           applicant=None):
    if applicant==None:
        applicant = request.applicant
    if (request.method == 'POST') and ('cancel' not in request.POST):
        form = form_class(request.POST, 
                          instance=old_data)
        if form.is_valid():
            data = form.save(commit=False)
            data.applicant = applicant
            data.save()
            applicant.add_related_model(field_name,
                                        save=True,
                                        smart=True)
            return (True, form)
    else:
        form = form_class(instance=old_data)
    return (False, form)


def handle_personal_info_form(request, old_info, applicant=None):
    return handle_basic_form_save(PersonalInfoForm,
                                  'personal_info',
                                  request,
                                  old_info,
                                  applicant)

def handle_education_forms(request, 
                           old_education, 
                           old_additional_eduction=None,
                           applicant=None):
    if settings.ACCEPT_ONLY_GRADUATED:
        if old_education==None:
            old_education = Education(has_graduated=True)
        else:
            old_education.has_graduated = True;

    if applicant==None:
        applicant = request.applicant

    if (request.method == 'POST') and ('cancel' not in request.POST):
        form = EducationForm(request.POST, 
                             instance=old_education)
        fvalid = form.is_valid()

        quota_form = QuotaForm(request.POST,
                               prefix='quota',
                               instance=old_additional_eduction)
        qvalid = quota_form.is_valid()

        forms = (form,quota_form)

        if fvalid and qvalid:
            education = form.save(commit=False)
            education.applicant = applicant
            education.save()
            applicant.add_related_model('educational_info',
                                        save=True,
                                        smart=True)
            additional_eduction = quota_form.save(commit=False)
            additional_eduction.applicant = applicant
            additional_eduction.save()
            return (True, forms)
    else:
        form = EducationForm(instance=old_education)
        quota_form = QuotaForm(instance=old_additional_eduction,
                               prefix='quota')
        forms = (form,quota_form)
    return (False, forms)


def handle_address_form(request, applicant=None):
    if applicant==None:
        applicant = request.applicant

    have_old_address = applicant.has_address()

    if have_old_address:
        old_applicant_address = applicant.address
        old_home_address = applicant.address.home_address
        old_contact_address = applicant.address.contact_address
    else:
        # still need this for form instances
        old_home_address, old_contact_address = None, None

    if (request.method == 'POST') and ('cancel' not in request.POST):

        home_address_form = AddressForm(request.POST, 
                                        prefix="home",
                                        instance=old_home_address)
        contact_address_form = AddressForm(request.POST, 
                                           prefix="contact",
                                           instance=old_contact_address)

        if (home_address_form.is_valid() and
            contact_address_form.is_valid()):
            home_address = home_address_form.save()
            contact_address = contact_address_form.save()

            applicant_address = ApplicantAddress(
                applicant=applicant,
                home_address=home_address,
                contact_address=contact_address)

            if have_old_address:
                applicant_address.id = old_applicant_address.id

            applicant_address.save()
            applicant.add_related_model('address',
                                        save=True,
                                        smart=True)

            return (True, home_address_form, contact_address_form)
    else:
        home_address_form = AddressForm(prefix="home",
                                        instance=old_home_address)
        contact_address_form = AddressForm(prefix="contact",
                                           instance=old_contact_address)

    return (False, home_address_form, contact_address_form)

