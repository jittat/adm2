# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date

from django.db import models
from django.conf import settings

from commons.utils import random_string
from commons.local import PROVINCE_CHOICES, APP_TITLE_CHOICES
from application.fields import IntegerListField

class Applicant(models.Model):

    # core applicant information
    title = models.CharField(max_length=10,
                             choices=APP_TITLE_CHOICES,
                             verbose_name="คำนำหน้า")
    first_name = models.CharField(max_length=200,
                                  verbose_name="ชื่อ")
    last_name = models.CharField(max_length=300,
                                 verbose_name="นามสกุล")
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=20,
                                   verbose_name="เลขประจำตัวประชาชน",
                                   unique=True)

    hashed_password = models.CharField(max_length=100)

    has_logged_in = models.BooleanField(default=False)
    activation_required = models.BooleanField(default=False)

    # application data

    is_submitted = models.BooleanField(default=False)

    # for related model cache

    RELATED_MODELS = {
        'personal_info': 0,
        'address': 1,
        'educational_info': 2,
        'major_preference': 3,
        'appdocs': 4
        }

    has_related_model = IntegerListField(default=None)

    def check_related_model(self, model_name):
        model_id = Applicant.RELATED_MODELS[model_name]
        if model_id < len(self.has_related_model):
            return (self.has_related_model[model_id] == 1)
        else:
            return None

    def initialize_related_model(self):
        self.has_related_model = [0 
                                  for i in 
                                  range(len(Applicant.RELATED_MODELS))]

    def add_related_model(self, model_name, save=False, smart=False):
        if len(self.has_related_model)==0:
            self.initialize_related_model()
        model_id = Applicant.RELATED_MODELS[model_name]
        old = self.has_related_model[model_id]
        self.has_related_model[model_id] = 1
        if save:
            if (not smart) or (old != 1):
                self.save()


    def refresh_has_related_model(self):
        self.has_related_model = []
        new_related_model = [0 for i in range(len(Applicant.RELATED_MODELS))]
        if self.has_personal_info():
            new_related_model[Applicant.RELATED_MODELS['personal_info']] = 1
        if self.has_address():
            new_related_model[Applicant.RELATED_MODELS['address']] = 1
        if self.has_educational_info():
            new_related_model[Applicant.RELATED_MODELS['educational_info']] = 1
        if self.has_major_preference():
            new_related_model[Applicant.RELATED_MODELS['major_preference']] = 1
        if self.get_applicant_docs_or_none()!=None:
            new_related_model[Applicant.RELATED_MODELS['appdocs']] = 1
        self.has_related_model = new_related_model
        self.save()

    class DuplicateSubmissionError(Exception):
        pass

    class ResubmissionError(Exception):
        pass

    ###################
    # class accessor methods

    @staticmethod
    def get_applicant_by_email(email):
        applicants = Applicant.objects.filter(email=email).all()
        if len(applicants)==0:
            return None
        else:
            return applicants[0]

    @staticmethod
    def get_applicant_by_national_id(nat_id):
        applicants = Applicant.objects.filter(national_id=nat_id).all()
        if len(applicants)==0:
            return None
        else:
            return applicants[0]

    @staticmethod
    def get_active_offline_applicants():
        return Applicant.objects.filter(is_offline=True).filter(is_submitted=False)

    @staticmethod
    def get_submitted_offline_applicants():
        return Applicant.objects.filter(is_offline=True).filter(is_submitted=True)

    # accessor methods

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return "%s %s %s" % (self.title, self.first_name, self.last_name)

    def get_email(self):
        return self.email

    def has_personal_info(self):
        result = self.check_related_model('personal_info')
        if result!=None:
            return result
        else:
            try:
                return self.personal_info != None
            except PersonalInfo.DoesNotExist:
                return False

    def get_personal_info_or_none(self):
        if self.has_personal_info():
            return self.personal_info
        else:
            return None

    def has_address(self):
        result = self.check_related_model('address')
        if result!=None:
            return result
        else:
            try:
                return self.address != None
            except ApplicantAddress.DoesNotExist:
                return False            

    def has_educational_info(self):
        result = self.check_related_model('educational_info')
        if result!=None:
            return result
        else:
            try:
                return self.education != None
            except Education.DoesNotExist:
                return False            

    def get_educational_info_or_none(self):
        if self.has_educational_info():
            edu = self.education
            edu.fix_boolean_fields()
            return edu
        else:
            return None

    def get_additional_education_or_none(self):
        from quota.models import AdditionalEducation
        try:
            return self.additional_education
        except AdditionalEducation.DoesNotExist:
            return None

    def has_major_preference(self):
        result = self.check_related_model('major_preference')
        if result!=None:
            return result
        else:
            try:
                return self.preference != None
            except MajorPreference.DoesNotExist:
                return False

    def has_admission_results(self):
        return self.admission_results.count() != 0

    def get_latest_admission_result(self):
        from result.models import AdmissionRound
        adm_round = AdmissionRound.get_recent()
        if adm_round:
            results = list(
                self.admission_results.filter(
                    round_number=adm_round.number))
            if len(results)>0:
                return results[0]
            else:
                return None
        else:
            return None

    def is_admitted(self):
        admission_result = self.get_latest_admission_result()
        return (admission_result) and (admission_result.is_admitted)
    
    def get_admission_major_preference(self,round_number):
        prefs = self.admission_major_preferences.filter(round_number=round_number)
        if len(prefs)!=0:
            return prefs[0]
        else:
            return None
    
    def get_student_registration(self):
        from confirmation.models import StudentRegistration
        try:
            reg = self.student_registration
            return reg
        except StudentRegistration.DoesNotExist:
            return None
            

    def get_applicant_docs_or_none(self):
        result = self.check_related_model('appdocs')
        if (result!=None) and (result==0):
            return None
        try:
            docs = self.appdocs
        except Exception:
            docs = None
        return docs

    def has_online_docs(self):
        return self.get_applicant_docs_or_none()!=None

    def has_supplements(self):
        supplements = self.supplements.all()
        return len(supplements)!=0

    def can_choose_major(self):
        return True

    def online_doc_submission(self):
        return True

    def is_eligible(self):
        return self.is_submitted and self.submission_info.is_paid

    ######################
    # methods for authentication

    def set_password(self, passwd):
        import random
        import hashlib

        salt = hashlib.sha1(str(random.random())[2:4]).hexdigest()

        full_password = (salt + '$' +
                         hashlib.sha1(salt + passwd).hexdigest())
        
        self.hashed_password = full_password


    def random_password(self, length=5):
        import random
        password = random_string(5)
        self.set_password(password)
        return password

    def check_password(self, password):
        import hashlib

        salt, enc_passwd = self.hashed_password.split('$')

        try:
            return enc_passwd == (hashlib.sha1(salt + password).hexdigest())
        except UnicodeEncodeError:
            return False


    def can_request_password(self):
        """
        checks if a user can request a new password, and saves the
        request log.  The criteria are:

        - the user hasn't requested the new password within 5 minutes,
        - the user hasn't requested the new password more than
        settings.MAX_PASSWORD_REQUST_PER_DAY (set in settings.py)
        times.
        """
        # get the log
        try:
            request_log = self.password_request_log
        except PasswordRequestLog.DoesNotExist:
            request_log = None
        
        if request_log==None:
            # request for the first time
            request_log = PasswordRequestLog.create_for(self)
            request_log.save()
            return True

        result = True
        if (request_log.last_request_at >= 
            datetime.now() - timedelta(minutes=5)):
            result = False

        if (request_log.requested_today() and
            request_log.num_requested_today >=
            settings.MAX_PASSWORD_REQUST_PER_DAY):
            result = False

        request_log.update()
        request_log.save()
        return result

    def verify_activation_key(self, key):
        for reg in self.registrations.all():
            if key==reg.activation_key:
                return True
        return False

    ######################
    # tickets

    def generate_submission_ticket(self):
        pass

    def ticket_number(self):
        try:
            application_id = self.submission_info.applicantion_id
            return ("%(year)d%(id)05d" % 
                    { 'year': settings.ADMISSION_YEAR,
                      'id': application_id })
        except SubmissionInfo.DoesNotExist:
            return None

    def verification_number(self,additional_salt=''):
        try:
            key = u"%s%s-%s-%s-%s-%s%s" % (
                settings.TICKET_SYSTEM_SALT,
                self.submission_info.salt,
                self.national_id,
                self.email,
                self.first_name,
                self.last_name,
                additional_salt)
            import hashlib
            h = hashlib.md5()
            h.update(key.encode('utf-8'))
            return str(int(float.fromhex(h.hexdigest()[:8])))
        except SubmissionInfo.DoesNotExist:
            return None


    #######################
    # submission
    
    def submit(self, submitted_at=None):
        if self.is_submitted:
            raise Applicant.DuplicateSubmissionError()
        try:
            submission_info = SubmissionInfo(applicant=self)
            submission_info.random_salt()
            submission_info.save()
            if submitted_at!=None:
                # to reassign submitted_at, we have to do it after the
                # object has been saved, otherwise the auto_now_add in
                # submitted_at would override our value.  this is why
                # we need to call submission_info.save() twice.
                submission_info.submitted_at = submitted_at
                submission_info.save()
        except:
            raise Applicant.DuplicateSubmissionError()

        self.is_submitted = True
        self.save()


    def resubmit(self):
        if not self.is_submitted:
            raise Applicant.ResubmissionError('Resubmission on applicant who is not submitted')
        submission_info = self.submission_info
        submission_info.is_resubmitted = True
        submission_info.resubmitted_at = datetime.now()
        submission_info.save()


class SubmissionInfo(models.Model):
    """
    associates Applicant who have submitted the applicaiton with a
    unique application_id.
    """
    applicantion_id = models.AutoField(unique=True, primary_key=True)
    applicant = models.OneToOneField(Applicant, 
                                     related_name="submission_info")
    salt = models.CharField(max_length=30)

    submitted_at = models.DateTimeField(auto_now_add=True)

    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    ######################################################
    
    last_updated_at = models.DateTimeField(blank=True, null=True,
                                           default=None)

    @staticmethod
    def find_by_ticket_number(ticket):
        if len(ticket)>8:
            return None
        sub_id = ticket[-5:]
        try:
            sub_id = int(sub_id)
            sub = SubmissionInfo.objects.get(pk=sub_id)
            return sub
        except:
            return None

    def random_salt(self):
        self.salt = random_string(10)

    def can_update_info(self):
        return True

    def update_last_updated_timestamp_to_now(self):
        from django.db import connection, transaction
        cursor = connection.cursor()

        sql = ("UPDATE application_submissioninfo SET `last_updated_at`=NOW() WHERE applicantion_id = %s")
        cursor.execute(sql, [str(self.applicantion_id)])
        transaction.commit_unless_managed()

    class Meta:
        ordering = ['applicantion_id']


class PersonalInfo(models.Model):
    applicant = models.OneToOneField(Applicant, related_name="personal_info")
    birth_date = models.DateField(verbose_name="วันเกิด")
    nationality = models.CharField(max_length=50,
                                   verbose_name="สัญชาติ")
    ethnicity = models.CharField(max_length=50,
                                 verbose_name="เชื้อชาติ")
    phone_number = models.CharField(max_length=35,
                                    verbose_name="หมายเลขโทรศัพท์")

    def __getattr__(self,name):
        if name=='national_id':
            if self.applicant:
                return self.applicant.national_id
        raise AttributeError()

class Address(models.Model):
    number = models.CharField(max_length=20,
                              verbose_name="บ้านเลขที่")
    village_number = models.IntegerField(blank=True, 
                                         null=True,
                                         verbose_name="หมู่ที่")
    village_name = models.CharField(blank=True,
                                    max_length=100,
                                    verbose_name="หมู่บ้าน")
    road = models.CharField(blank=True, null=True, 
                            max_length=50,
                            verbose_name="ถนน")
    district = models.CharField(max_length=50,
                                verbose_name="ตำบล/แขวง")
    city = models.CharField(max_length=50,
                            verbose_name="อำเภอ/เขต")
    province = models.CharField(max_length=25,
                                choices=PROVINCE_CHOICES,
                                verbose_name="จังหวัด")
    postal_code = models.CharField(max_length=10,
                                   verbose_name="รหัสไปรษณีย์")
    phone_number = models.CharField(max_length=35,
                                    verbose_name="หมายเลขโทรศัพท์")

    def __unicode__(self):
        return ("%s %s %s %s %s %s" % 
                (self.number,
                 self.road,
                 self.district,
                 self.city,
                 self.province,
                 self.postal_code))



class ApplicantAddress(models.Model):
    applicant = models.OneToOneField(Applicant,
                                     related_name="address")
    home_address = models.OneToOneField(Address, 
                                        related_name="home_owner")
    contact_address = models.OneToOneField(Address, 
                                           related_name="contact_owner")

    def __unicode__(self):
        return unicode(self.contact_address)


class GPExamDate(models.Model):
    month_year = models.CharField(max_length=20,
                                  verbose_name="เดือนและปีของการสอบ")
    rank = models.IntegerField(unique=True)

    class Meta:
        ordering = ['rank']

    dates = None

    @staticmethod
    def cache_dates():
        if not GPExamDate.dates:
            GPExamDate.dates = dict([(d.id, d) for d in GPExamDate.objects.all()])

    @staticmethod
    def get_by_id(id):
        GPExamDate.cache_dates()
        try:
            return GPExamDate.dates[id]
        except:
            return None

    def __unicode__(self):
        return self.month_year

class Education(models.Model):
    applicant = models.OneToOneField(Applicant,
                                     related_name="education")

    # school information
    has_graduated = models.BooleanField(
        choices=((False,u"กำลังเรียนระดับมัธยมศึกษาปีที่ 6 หรือเทียบเท่า"),
                 (True,u"จบการศึกษาระดับมัธยมศึกษาปีที่ 6 หรือเทียบเท่า")),
        verbose_name=u"ระดับการศึกษา")
    school_name = models.CharField(max_length=100,
                                   verbose_name=u"โรงเรียน")
    school_city = models.CharField(max_length=50,
                                   verbose_name=u"อำเภอ/เขต")
    school_province = models.CharField(max_length=25,
                                       choices=PROVINCE_CHOICES,
                                       verbose_name=u"จังหวัด")
    alt_name = models.CharField(max_length=300,
                                default="",
                                blank=True,
                                null=True,
                                verbose_name="ชื่ออื่น(ที่ใช้เมื่อสอบ)")

    # This is used for post-identifying potential cross review-update
    # condition.  In that case the document must be manually validated
    # again.
    updated_at = models.DateTimeField(auto_now=True)

    def fix_boolean_fields(self):
        self.has_graduated = bool(self.has_graduated)

    def __unicode__(self):
        if self.has_graduated:
            return u"จบการศึกษาจากโรงเรียน" + self.school_name
        else:
            return u"กำลังศึกษาอยู่ที่โรงเรียน" + self.school_name


class Major(models.Model):
    number = models.CharField(max_length=5)
    name = models.CharField(max_length=100)

    confirmation_amount = models.IntegerField(default=0)

    class Meta:
        ordering = ['number']

    def __unicode__(self):
        return "%s: %s" % (self.number, self.name)

    def select_id(self):
        return "major_%d" % (self.id,)

    __major_list = None

    @staticmethod
    def get_all_majors():
        if Major.__major_list==None:
            Major.__major_list = list(Major.objects.all())
        return Major.__major_list

    @staticmethod
    def get_majors_for_training_round(r):
        if r==2:
            return Major.objects.filter(number__startswith=1)
        else:
            return Major.objects.all()
        


class MajorPreference(models.Model):
    applicant = models.OneToOneField(Applicant,
                                     related_name="preference")
    majors = IntegerListField()

    @staticmethod
    def major_list_to_major_rank_list(major_list):
        """
        return a list of preference ranks for each major
        """
        all_majors = Major.get_all_majors()
        major_count = len(all_majors)

        ranks = [None] * major_count

        rev = {}
        for i in range(major_count):
            rev[int(all_majors[i].number)] = i

        r = 1
        for m in major_list:
            ranks[rev[m]] = r
            r += 1

        return ranks
        

    def to_major_rank_list(self):
        return MajorPreference.major_list_to_major_rank_list(self.majors)

    def get_major_list(self):
        """
        return a list of majors ordered by preference
        """
        all_majors = Major.get_all_majors()

        majors_dict = {}
        for m in all_majors:
            majors_dict[int(m.number)] = m

        l = []
        for number in self.majors:
            l.append(majors_dict[number])

        return l


####################################################
# models for registration data
#

class Registration(models.Model):
    applicant = models.ForeignKey(Applicant,related_name="registrations")
    national_id = models.CharField(max_length=20,
                                   verbose_name="เลขประจำตัวประชาชน")
    registered_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=300)
    activation_key = models.CharField(max_length=10, blank=True, unique=True)

    def random_activation_key(self):
        self.activation_key = random_string(10)
        return self.activation_key

    def random_and_save(self):
        success = False
        trials = 0
        while not success:
            try:
                self.random_activation_key()
                self.save()
                success = True
            except:
                trials += 1
                if trials > 10:
                    raise

    class Meta:
        ordering = ['-registered_at']


class PasswordRequestLog(models.Model):
    """
    keeps track of password requests.  It is used when calling to
    Applicant.can_request_password()
    """
    applicant = models.OneToOneField(Applicant,related_name='password_request_log')
    last_request_at = models.DateTimeField()
    num_requested_today = models.IntegerField(default=0)

    @staticmethod
    def create_for(applicant):
        log = PasswordRequestLog(applicant=applicant,
                                 last_request_at=datetime.now(),
                                 num_requested_today=1)
        return log

    def requested_today(self):
        if not self.last_request_at:
            return False
        today = date.today()
        today_datetime = datetime(today.year, today.month, today.day)
        return self.last_request_at >= today_datetime

    def update(self):
        """
        updates the number of requests for today, and the requested
        timestamp.
        """
        self.last_request_at = datetime.now()
        if self.requested_today():
            self.num_requested_today = self.num_requested_today + 1
        else:
            self.num_requested_today = 1


class ApplyingCondition(models.Model):
    number = models.IntegerField(unique=True, 
                             verbose_name=u'หมายเลข')
    body = models.TextField(verbose_name=u'เงื่อนไข')

    class Meta:
        ordering = ['number']

    def __unicode__(self):
        return u'%d %s' % (self.number, self.body[:30])

