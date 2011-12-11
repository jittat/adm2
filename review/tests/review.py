# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase, TransactionTestCase

from django.conf import settings

from commons import email
from application.models import Applicant

SOMCHAI_EMAIL = "somchai@thailand.com"
SOMCHAI_PASSWORD = "coykx"

SOMYING_EMAIL = "somying@ku.ac.th"
SOMYING_PASSWORD = "bgchp"

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'testadmin'

BASE_REVIEW_FORM_DATA = {
    'abroad_edu_certificate-applicant_note':'',
    'abroad_edu_certificate-internal_note':'',
    'app_fee_doc-applicant_note':'',
    'app_fee_doc-internal_note':'',
    'app_fee_doc-is_passed':'on',
    'edu_certificate-applicant_note':'',
    'edu_certificate-internal_note':'',
    'edu_certificate-is_passed':'on',
    'nat_id-applicant_note':'',
    'nat_id-internal_note':'',
    'nat_id-is_passed':'on',
    'picture-applicant_note':'',
    'picture-internal_note':'',
    'picture-is_passed':'on',
    'submit':'เก็บข้อมูล',
    }

ALL_PASSED_REVIEW_FORM_DATA_ANET = dict(BASE_REVIEW_FORM_DATA)
ALL_PASSED_REVIEW_FORM_DATA_ANET.update({
        'anet_score-applicant_note':'',
        'anet_score-internal_note':'',
        'anet_score-is_passed':'on',
        })

ALL_PASSED_REVIEW_FORM_DATA_GATPAT = dict(BASE_REVIEW_FORM_DATA)
ALL_PASSED_REVIEW_FORM_DATA_GATPAT.update({
        'gat_score-applicant_note':'',
        'gat_score-internal_note':'',
        'gat_score-is_passed':'on',
        'pat1_score-applicant_note':'',
        'pat1_score-internal_note':'',
        'pat1_score-is_passed':'on',
        'pat3_score-applicant_note':'',
        'pat3_score-internal_note':'',
        'pat3_score-is_passed':'on',
        })

DEPOSITE_MISSING_REVIEW_FORM_DATA_GATPAT = dict(ALL_PASSED_REVIEW_FORM_DATA_GATPAT)
DEPOSITE_MISSING_REVIEW_FORM_DATA_ANET = dict(ALL_PASSED_REVIEW_FORM_DATA_GATPAT)

for form_data in [DEPOSITE_MISSING_REVIEW_FORM_DATA_ANET, DEPOSITE_MISSING_REVIEW_FORM_DATA_GATPAT]:
    del form_data['app_fee_doc-is_passed']
    form_data.update({
            'app_fee_doc-applicant_note':'หมายเลขไม่มี',
            'app_fee_doc-internal_note':'',
            })


class ReviewTestCaseBase(TransactionTestCase):

    fixtures = ['submissions', 'admin_user', 'review_field']

    def _login_required(self,email, password):
        response = self.client.post('/apply/login/',
                                    {'email': email,
                                     'password': password })
        
        self.assertRedirects(response,'/apply/status/')
        return response

    def _admin_login_required(self):
        response = self.client.post('/accounts/login/',
                                    {'username': ADMIN_USERNAME,
                                     'password': ADMIN_PASSWORD,
                                     'next': '/review/'})
        self.assertRedirects(response, '/review/')



class ReviewTestCase(ReviewTestCaseBase):

    def setUp(self):
        # make sure the when testing, the app is using django's email
        # system.
        from django.core.mail import send_mail

        email.send_mail = send_mail 

        self.org_email_setting = settings.FAKE_SENDING_EMAIL
        settings.FAKE_SENDING_EMAIL = False


    def tearDown(self):
        settings.FAKE_SENDING_EMAIL = self.org_email_setting


    def test_doc_received_status_display_changed_after_admin_update(self):
        self._login_required(SOMYING_EMAIL,SOMYING_PASSWORD)
        response = self.client.get('/apply/status/')
        self.assertContains(response,"ยังไม่ได้รับ")

        self._admin_login_required()

        self.client.get('/review/received/toggle/2/')
        self.client.get('/accounts/logout/')

        self._login_required(SOMYING_EMAIL,SOMYING_PASSWORD)
        response = self.client.get('/apply/status/')
        self.assertNotContains(response,"ยังไม่ได้รับ")   


    def test_link_edu_info_update_removed_after_app_gets_reviewed(self):
        self._admin_login_required()

        self.client.post('/review/show/2/',
                         ALL_PASSED_REVIEW_FORM_DATA_ANET)

        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/status/')
        self.assertNotContains(response, "id_edu-update-button")


    def test_app_cannot_edit_edu_info_after_getting_reviewed(self):
        self._admin_login_required()

        self.client.post('/review/show/2/',
                         ALL_PASSED_REVIEW_FORM_DATA_ANET)

        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/update/education')
        self.assertTemplateNotUsed(response, 
                                   "application/update/education.html")


    def test_review_status_update_successful(self):
        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/status/')
        self.assertNotContains(response, "ตรวจสอบเรียบร้อย")

        self._admin_login_required()

        self.client.get('/review/received/toggle/2/')
        response = self.client.post('/review/show/2/',
                         ALL_PASSED_REVIEW_FORM_DATA_ANET)


        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/status/')

        self.assertContains(response, "ตรวจสอบเรียบร้อย")

    def test_review_status_update_failed(self):
        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/status/')
        self.assertNotContains(response, "ตรวจสอบเรียบร้อย")

        self._admin_login_required()

        response = self.client.post('/review/show/2/',
                                    DEPOSITE_MISSING_REVIEW_FORM_DATA_ANET)

        self._login_required(SOMYING_EMAIL, SOMYING_PASSWORD)

        response = self.client.get('/apply/status/')

        self.assertNotContains(response, "ตรวจสอบเรียบร้อย")
        self.assertContains(response, "หลักฐานใบนำฝาก")
        self.assertContains(response, "หมายเลขไม่มี")

class ReviewForApplicantsWithCompletedReviewFieldsTestCase(ReviewTestCaseBase):

    fixtures = ['application_completed_review_field', 
                'submissions_completed_review_field',
                'admin_user', 
                'review_field',
                'major']

    def setUp(self):
        # make sure the when testing, the app is using django's email
        # system.
        from django.core.mail import send_mail

        email.send_mail = send_mail 

        self.org_email_setting = settings.FAKE_SENDING_EMAIL
        settings.FAKE_SENDING_EMAIL = False


    def tearDown(self):
        settings.FAKE_SENDING_EMAIL = self.org_email_setting


    def test_completed_review_field_not_show_in_review_page(self):
        self._admin_login_required()

        response = self.client.get('/review/show/2/')

        self.assertNotContains(response, 'id_app_fee_doc-is_passed')
 
    def test_review_status_failed(self):
        self._admin_login_required()

        # this applicant uses GAT/PAT score, so by submiting ANET data
        # the review should fail.

        REVIEW_FORM_DATA_WITHOUT_GATPAT = dict(ALL_PASSED_REVIEW_FORM_DATA_ANET)
        response = self.client.post('/review/show/2/',
                                    REVIEW_FORM_DATA_WITHOUT_GATPAT,
                                    follow=True)

        self.assertContains(response,
                            'จัดเก็บและแจ้งผลการตรวจว่าหลักฐานไม่ผ่านกับผู้สมัครแล้ว')

    def test_review_status_successful(self):
        self._admin_login_required()

        # update review, using data without app_fee_doc, update should
        # still success because this field is already reviewed.
        response = self.client.post('/review/show/2/',
                                    DEPOSITE_MISSING_REVIEW_FORM_DATA_GATPAT,
                                    follow=True)

        self.assertContains(response,
                            'จัดเก็บและแจ้งผลการตรวจว่าผ่านกับผู้สมัครแล้ว')
