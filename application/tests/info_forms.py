# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.core import mail
from django.test import TestCase, TransactionTestCase

from django.conf import settings

from application.models import Applicant, Registration
from commons import email

from helpers import ApplicantPreparation


class FormsTestCaseBase(TransactionTestCase):

    fixtures = ['major', 'gatpat-dates']

    def setUp(self):
        self.app_prep = ApplicantPreparation()
        self.applicant, self.password = self.app_prep.create_applicant()
        self.email = self.applicant.email

        from django.core.mail import send_mail

        email.send_mail = send_mail 

        self.org_email_setting = settings.FAKE_SENDING_EMAIL
        settings.FAKE_SENDING_EMAIL = False

        # remove submission dealine
        settings.SUBMISSION_DEADLINE = None

    PERSONAL_FORM_DATA = {
        'national_id': '1234567890123',
        'birth_date_day': '1',
        'birth_date_month': '1',
        'birth_date_year': '1990',
        'ethnicity': u'ไทย',
        'nationality': u'ไทย',
        'phone_number': u'081-111-2222 ต่อ 1234'
        }

    ADDRESS_FORM_DATA = {
        'contact-city':'ลำลูกกา',
        'contact-district':'คูคต',
        'contact-number':'74/13',
        'contact-phone_number':'029948402',
        'contact-postal_code':'12130',
        'contact-province':'ปทุมธานี',
        'contact-road':'พหลโยธิน',
        'contact-village_name':'',
        'contact-village_number':'10',
        'home-city':'ลำลูกกา',
        'home-district':'คูคต',
        'home-number':'74/13',
        'home-phone_number':'029948402',
        'home-postal_code':'12130',
        'home-province':'ปทุมธานี',
        'home-road':'พหลโยธิน',
        'home-village_name':'',
        'home-village_number':'10',
        'submit':'เก็บข้อมูล',
        }

    EDU_FORM_DATA_GATPAT = {
        'anet':'10',
        'gat':'100',
        'gat_date':'1',
        'gpax':'3.45',
        'has_graduated':'True',
        'pat1':'200',
        'pat1_date':'2',
        'pat3':'300',
        'pat3_date':'3',
        'school_city':'เมือง',
        'school_name':'สาธิต',
        'school_province':'จันทบุรี',
        'submit':'เก็บข้อมูล',
        'uses_gat_score':'True',
        }

    EDU_FORM_DATA_GATPAT_UPDATED = {
        'anet':'10',
        'gat':'100',
        'gat_date':'1',
        'gpax':'3.45',
        'has_graduated':'True',
        'pat1':'123',
        'pat1_date':'2',
        'pat3':'237',
        'pat3_date':'3',
        'school_city':'เมือง',
        'school_name':'สาธิต',
        'school_province':'นครปฐม',
        'submit':'เก็บข้อมูล',
        'uses_gat_score':'True',
        }

    EDU_FORM_DATA_ANET_PASSED = {
        'anet':'35',
        'gat':'',
        'gat_date':'',
        'gpax':'3.45',
        'has_graduated':'True',
        'pat1':'',
        'pat1_date':'',
        'pat3':'',
        'pat3_date':'',
        'school_city':'เมือง',
        'school_name':'สาธิต',
        'school_province':'นครปฐม',
        'submit':'เก็บข้อมูล',
        'uses_gat_score':'False',
        }

    
    EDU_FORM_DATA_ANET_FAILED_WITHOUT_TOTAL_SCORE = {
        'anet':'10',
        'anet_total_score':'',
        'gat':'',
        'gat_date':'',
        'gpax':'3.45',
        'has_graduated':'True',
        'pat1':'',
        'pat1_date':'',
        'pat3':'',
        'pat3_date':'',
        'school_city':'เมือง',
        'school_name':'สาธิต',
        'school_province':'นครปฐม',
        'submit':'เก็บข้อมูล',
        'uses_gat_score':'False',
        }

    
    EDU_FORM_DATA_ANET_FAILED_WITH_TOTAL_SCORE_PASSED = {
        'anet':'10',
        'anet_total_score':'5000',
        'gat':'100',
        'gat_date':'1',
        'gpax':'3.45',
        'has_graduated':'True',
        'pat1':'200',
        'pat1_date':'2',
        'pat3':'300',
        'pat3_date':'3',
        'school_city':'เมือง',
        'school_name':'สาธิต',
        'school_province':'จันทบุรี',
        'submit':'เก็บข้อมูล',
        'uses_gat_score':'False',
        }

    
    EDU_FORM_DATA_ANET_FAILED_WITH_TOTAL_SCORE_FAILED = {
        'anet':'10',
        'anet_total_score':'4999',
        'gat':'100',
        'gat_date':'1',
        'gpax':'3.45',
        'has_graduated':'True',
        'pat1':'200',
        'pat1_date':'2',
        'pat3':'300',
        'pat3_date':'3',
        'school_city':'เมือง',
        'school_name':'สาธิต',
        'school_province':'จันทบุรี',
        'submit':'เก็บข้อมูล',
        'uses_gat_score':'False',
        }

    
    MAJOR_RANK_FORM_DATA_ROUND1 = {
        'major_1':'3',
        'major_10':'--',
        'major_11':'--',
        'major_12':'--',
        'major_13':'--',
        'major_2':'4',
        'major_3':'--',
        'major_4':'--',
        'major_5':'6',
        'major_6':'5',
        'major_7':'2',
        'major_8':'--',
        'major_9':'1',
        'submit':'เก็บข้อมูล',
        }

    # UPDATED FOR ROUND 2
    MAJOR_RANK_FORM_DATA = {
        'major_1':'--',
        'major_10':'--',
        'major_11':'--',
        'major_12':'--',
        'major_13':'--',
        'major_2':'--',
        'major_3':'--',
        'major_4':'--',
        'major_5':'--',
        'major_6':'--',
        'major_7':'--',
        'major_8':'1',
        'major_9':'3',
        'submit':'เก็บข้อมูล',
        }

    # helpers method

    def _login_required(self, check=True):
        response = self.client.post('/apply/login/',
                                    {'email': self.email,
                                     'password': self.password})
        if check:
            self.assertRedirects(response,'/apply/personal/')
        return response

    def _personal_info_required(self):
        response = self.client.post('/apply/personal/',
                                    InfoFormsTestCase.PERSONAL_FORM_DATA)
        self.assertRedirects(response,'/apply/address/')
                
    def _address_info_required(self):
        response = self.client.post('/apply/address/',
                                    InfoFormsTestCase.ADDRESS_FORM_DATA)
        self.assertRedirects(response,'/apply/education/')
        
    def _edu_info_required(self):
        response = self.client.post('/apply/education/',
                                    InfoFormsTestCase.EDU_FORM_DATA_GATPAT)
        self.assertRedirects(response,'/apply/majors/')

    def _major_ranks_info_required(self):
        response = self.client.post('/apply/majors/',
                                    InfoFormsTestCase.MAJOR_RANK_FORM_DATA,
                                    follow=True)
        if not settings.FORCE_UPLOAD_DOC:
            self.assertRedirects(response,'/apply/doc_menu/')
        else:
            self.assertRedirects(response,'/doc/')

    def _submit_postal_doc_confirm_required(self):
        response = self.client.get('/apply/confirm/')
        self.assertEqual(response.status_code, 200)

    def _online_doc_upload_form_required(self):
        response = self.client.get('/doc/')
        self.assertEqual(response.status_code, 200)
        return response

    def _submit_postal_confirm_required(self):
        response = self.client.post('/apply/confirm/',
                                    {'submit': 'ยืนยัน'})
        self.assertRedirects(response,'/apply/ticket/')
        self.assertEquals(len(mail.outbox),1)       

    def _fill_forms_upto_online_doc_upload_form(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()
        self._major_ranks_info_required()
        return self._online_doc_upload_form_required()



class InfoFormsTestCase(FormsTestCaseBase):

    def test_user_can_login(self):
        self._login_required()
        settings.FAKE_SENDING_EMAIL = self.org_email_setting

    def _test_personal_form(self):
        self._login_required()
        self._personal_info_required()

    def _test_address_form(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()

    def _test_edu_form(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()

    def _test_majors_form(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()
        self._major_ranks_info_required()

    def test_edu_form_with_anet(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        response = self.client.post('/apply/education/',
                                    InfoFormsTestCase.EDU_FORM_DATA_ANET_PASSED)
        self.assertRedirects(response,'/apply/majors/')

    def test_edu_form_with_anet_invalid_when_score_too_low_with_no_total_score(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        response = self.client.post('/apply/education/',
                                    InfoFormsTestCase.EDU_FORM_DATA_ANET_FAILED_WITHOUT_TOTAL_SCORE)
        self.assertTemplateUsed(response,'application/education.html')

    def test_edu_form_with_anet_invalid_when_score_too_low_with_total_score_passed(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        response = self.client.post('/apply/education/',
                                    InfoFormsTestCase.EDU_FORM_DATA_ANET_FAILED_WITH_TOTAL_SCORE_PASSED)
        self.assertRedirects(response,'/apply/majors/')

    def test_edu_form_with_anet_invalid_when_score_too_low_with_total_score_failed(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        response = self.client.post('/apply/education/',
                                    InfoFormsTestCase.EDU_FORM_DATA_ANET_FAILED_WITH_TOTAL_SCORE_FAILED)
        self.assertTemplateUsed(response,'application/education.html')

    def test_postal_submission_confirm(self):
        old_upload_doc_setting = settings.FORCE_UPLOAD_DOC
        settings.FORCE_UPLOAD_DOC = False

        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()
        self._major_ranks_info_required()
        self._submit_postal_doc_confirm_required()

        settings.FORCE_UPLOAD_DOC = old_upload_doc_setting


    def test_postal_submission(self):
        old_upload_doc_setting = settings.FORCE_UPLOAD_DOC
        settings.FORCE_UPLOAD_DOC = False

        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()
        self._major_ranks_info_required()
        self._submit_postal_doc_confirm_required()
        self._submit_postal_confirm_required()

        settings.FORCE_UPLOAD_DOC = old_upload_doc_setting

    def test_edu_info_update_postal_submission(self):
        old_grace_period_end = settings.SUBMISSION_CHANGE_GRACE_PERIOD_END
        settings.SUBMISSION_CHANGE_GRACE_PERIOD_END = (
            datetime.now() + timedelta(1))

        old_upload_doc_setting = settings.FORCE_UPLOAD_DOC
        settings.FORCE_UPLOAD_DOC = False

        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()
        self._major_ranks_info_required()
        self._submit_postal_doc_confirm_required()
        self._submit_postal_confirm_required()
        self._edu_update_required()

        settings.FORCE_UPLOAD_DOC = old_upload_doc_setting
        settings.SUBMISSION_CHANGE_GRACE_PERIOD_END = old_grace_period_end

    def test_online_submission_form(self):
        self._login_required()
        self._personal_info_required()
        self._address_info_required()
        self._edu_info_required()
        self._major_ranks_info_required()
        self._online_doc_upload_form_required()

    def test_wrong_jump_to_online_submission_form(self):
        self._login_required()
        self._personal_info_required()
        response = self.client.get('/doc/')
        self.assertNotEqual(response.status_code, 200)

    # helper methods
    def _edu_update_required(self):
        response = self.client.post('/apply/update/education/',
                                    InfoFormsTestCase.EDU_FORM_DATA_GATPAT_UPDATED)
        self.assertRedirects(response,'/apply/status/')

        response = self.client.get('/apply/update/education/')
        self.assertContains(response,'237')
        self.assertContains(response,'123')
        self.assertContains(response,'นครปฐม')

