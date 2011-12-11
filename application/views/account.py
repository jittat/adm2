# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from django import forms

from MySQLdb import IntegrityError

from commons.utils import redirect_to_index, submission_deadline_passed
from application.views import redirect_to_first_form
from application.views import redirect_to_applicant_first_page

from application.models import Applicant
from application.models import SubmissionInfo
from application.models import Registration
from application.forms import LoginForm, ForgetPasswordForm
from application.forms import RegistrationForm, ActivationNameForm
from commons.email import send_password_by_email, send_activation_by_email
from commons.models import Announcement
from commons.decorators import within_submission_deadline

ALLOWED_LOGOUT_REDIRECTION = ['http://admission.eng.ku.ac.th']

def login(request):
    announcements = Announcement.get_all_enabled_annoucements()
    if not settings.LOGIN_ENABLED:
        # login disabled
        if request.method == 'POST':
            return HttpResponseForbidden()
        else:
            return render_to_response('application/wait.html',
                                      { 'announcements': announcements })     

    error_messages = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            passwd = form.cleaned_data['password']

            national_id = form.cleaned_data['national_id']
            applicants = list(Applicant.objects.filter(national_id=national_id).all())
            if len(applicants)!=0:
                applicant = applicants[0]
            else:
                applicant = None

            if applicant!=None:
                if applicant.activation_required:
                    email = applicant.email
                    return render_to_response(
                        'application/registration/activation-required.html',
                        { 'email': email })
                elif applicant.check_password(passwd):
                    # authenticated

                    if not applicant.has_logged_in:
                        applicant.has_logged_in = True
                        applicant.save()

                    request.session['applicant_id'] = applicant.id
                    
                    return redirect_to_applicant_first_page(applicant)
            
            from django.forms.util import ErrorList

            form._errors['password'] = ErrorList(['รหัสผ่านผิดพลาด'])
            error_messages.append('รหัสผ่านผิดพลาด')
    else:
        form = LoginForm()

    return render_to_response('application/start.html',
                              { 'form': form,
                                'submission_deadline_passed':
                                    submission_deadline_passed(),
                                'errors': error_messages,
                                'announcements': announcements })

def logout(request):
    next_url = None
    if 'url' in request.GET:
        next_url = request.GET['url']
        if next_url[0]!='/':
            next_url = 'http://' + next_url
    request.session.flush()
    if next_url and (next_url in ALLOWED_LOGOUT_REDIRECTION):
        return HttpResponseRedirect(next_url)
    else:
        return redirect_to_index(request)


def duplicate_email_error(applicant, email, first_name, last_name):
    # query set is lazy, so we have to force it, using list().
    old_registrations = list(applicant.registrations.all())  

    new_registration = Registration(applicant=applicant,
                                    first_name=first_name,
                                    last_name=last_name)
    new_registration.random_and_save()
    send_activation_by_email(applicant, new_registration.activation_key)
    applicant.activation_required = True
    applicant.save()
    return render_to_response('application/registration/duplicate.html',
                              { 'applicant': applicant,
                                'email': email,
                                'old_registrations': old_registrations,
                                'new_registration': new_registration,
                                'step_name': "อีเมล์นี้มีการลงทะเบียนไว้แล้ว ต้องมีการยืนยันอีเมล์" })


def validate_email_and_national_id(email, national_id):
    applicant = Applicant.get_applicant_by_national_id(national_id)
    if applicant!=None:
        return (False, 'national_id', applicant)
    else:
        applicant = Applicant.get_applicant_by_email(email)
        if applicant!=None:
            return (False, 'email', applicant)
        else:
            return (True, None, None)
    

def registration_error(error_field,
                       applicant, email, national_id, first_name, last_name):
    if error_field == 'email':
        return duplicate_email_error(applicant,
                                     email,
                                     first_name,
                                     last_name)
    else:
        return render_to_response(
            'application/registration/duplicate-nat-id-error.html',
            { 'national_id': national_id,
              'step_name': u'เกิดปัญหาในการลงทะเบียน เนื่องจากมีการใช้รหัสประจำตัวประชาชนซ้ำ'})


@within_submission_deadline
def register(request):
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect_to_index(request)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            national_id=form.cleaned_data['national_id']

            result, error_field, applicant = (
                validate_email_and_national_id(email,
                                               national_id))

            if result:
                try:
                    applicant = form.get_applicant()
                    passwd = applicant.random_password()
                    applicant.save()
                except IntegrityError:
                    # somehow, it gets error

                    result, error_field, applicant = (
                        validate_email_and_national_id(email,
                                                       national_id))
                    return registration_error(error_field,
                                              applicant,
                                              email,
                                              national_id,
                                              first_name,
                                              last_name)
                
                registration = Registration(
                    applicant=applicant,
                    first_name=first_name,
                    last_name=last_name)
                registration.random_and_save()
                send_password_by_email(applicant, passwd)
                return render_to_response(
                    'application/registration/success.html',
                    {'email': form.cleaned_data['email'],
                     'step_name': "การลงทะเบียนเรียบร้อย" })
            else:
                if not applicant.has_logged_in:
                    return registration_error(error_field,
                                              applicant,
                                              email,
                                              national_id,
                                              first_name,
                                              last_name)

                # e-mail or national id has been registered and logged in
                from django.forms.util import ErrorList
                from commons.utils import admin_email

                if error_field == 'email':
                    dup_obj = u'อีเมล์'
                else:
                    dup_obj = u'รหัสประจำตัวประชาชน'

                form._errors['__all__'] = ErrorList([
u"""%(dup_obj)sนี้ถูกลงทะเบียนและถูกใช้แล้ว ถ้าอีเมล์นี้เป็นของคุณจริงและยังไม่เคยลงทะเบียน
กรุณาติดต่อผู้ดูแลระบบทางอีเมล์ <a href="mailto:%(email)s">%(email)s</a> หรือทางเว็บบอร์ด
อาจมีผู้ไม่ประสงค์ดีนำอีเมล์คุณไปใช้""" % {'dup_obj': dup_obj,
                                 'email': admin_email()}])
                
    else:
        form = RegistrationForm()
    return render_to_response('application/registration/register.html',
                              { 'form': form })


@within_submission_deadline
def activate(request, activation_key):
    try:
        registration = Registration.objects.get(activation_key=activation_key)
    except Registration.DoesNotExist:
        return render_to_response(
            'application/registration/activation-not-required.html',
            {'step_name': "ไม่จำเป็นต้องมีการยืนยันอีเมล์"})

    applicant = registration.applicant

    if not applicant.activation_required:
        return render_to_response(
            'application/registration/activation-not-required.html',
            {'step_name': "ไม่จำเป็นต้องมีการยืนยันอีเมล์"})

    if not applicant.verify_activation_key(activation_key):
        return render_to_response(
            'application/registration/incorrect-activation-key.html',
            {'applicant': applicant,
             'step_name': "รหัสยืนยันผิดพลาด" })

    if request.method == 'GET':
        # get a click from e-mail
        name_form = ActivationNameForm(initial={
                'title': applicant.title,
                'first_name': applicant.first_name,
                'last_name': applicant.last_name})
    else:
        name_form = ActivationNameForm(request.POST)
        if name_form.is_valid():
            applicant.activation_required = False
            applicant.title = name_form.cleaned_data['title']
            applicant.first_name = name_form.cleaned_data['first_name']
            applicant.last_name = name_form.cleaned_data['last_name']
            passwd = applicant.random_password()
            applicant.save()
            registration = Registration(
                applicant=applicant,
                first_name=applicant.first_name,
                last_name=applicant.last_name)
            registration.random_and_save()
            send_password_by_email(applicant, passwd)           
            return render_to_response(
                'application/registration/activation-successful.html',
                {'applicant': applicant})

    return render_to_response(
        'application/registration/activation-name-confirmation.html',
        {'applicant': applicant,
         'form': name_form,
         'activation_key': activation_key,
         'no_first_page_link': True,
         'step_name': "การยืนยันอีเมล์ - รหัสสำหรับยืนยันถูกต้อง" })


def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']['email']
            applicant = form.cleaned_data['email']['applicant']

            if applicant.can_request_password():

                if applicant.activation_required:
                    return duplicate_email_error(applicant,
                                                 email,
                                                 applicant.first_name,
                                                 applicant.last_name)

                new_pwd = applicant.random_password()
                applicant.save()
                send_password_by_email(applicant, new_pwd)
            
                return render_to_response(
                    'application/registration/password-sent.html',
                    {'email': email,
                     'step_name': "ส่งรหัสผ่านให้แล้ว"})
            else:
                return render_to_response(
                    'application/registration/too-many-requests.html',
                    {'email': email,
                     'step_name': "ขอรหัสผ่านบ่อยครั้งเกินไป"})                
    else:
        form = ForgetPasswordForm()

    return render_to_response('application/forget.html', 
                              { 'form': form })
    
