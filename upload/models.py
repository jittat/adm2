# -*-  coding: utf-8 -*-
import os
from datetime import datetime, date

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from application.models import Applicant, Education
from review.models import CompletedReviewField

uploaded_storage = FileSystemStorage(location=settings.UPLOADED_DOC_PATH)

def get_doc_path(applicant, filename):
    return ('doc/%d/%s' % (applicant.id, filename))

def get_doc_fullpath(applicant, filename):
    return os.path.join(settings.UPLOADED_DOC_PATH,
                        get_doc_path(applicant, filename))

def get_field_filename(org_filename, field_name):
    first, ext = os.path.splitext(org_filename)    
    return field_name + ext

def get_field_thumbnail_filename(field_name):
    return field_name + '.thumbnail.png'

def get_field_preview_filename(field_name):
    return field_name + '.preview.png'

def get_doc_path_function(field_name):
    "returns a function for modifying uploaded filename"
    def f(instance, filename):
        field_filename = get_field_filename(filename, field_name)
        return get_doc_path(instance.applicant, field_filename)
    return f


class AppDocs(models.Model):
    applicant = models.OneToOneField(Applicant)
    picture = models.ImageField(
        upload_to=get_doc_path_function('picture'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='รูปถ่าย')
    edu_certificate = models.ImageField(
        upload_to=get_doc_path_function('edu_certificate'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='ใบรับรองการศึกษา')

    abroad_edu_certificate = models.ImageField(
        upload_to=get_doc_path_function('abroad_edu_certificate'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='หลักฐานการศึกษาต่างประเทศ')

    gat_score = models.ImageField(
        upload_to=get_doc_path_function('gat_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน GAT')

    pat1_score = models.ImageField(
        upload_to=get_doc_path_function('pat1_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน PAT1')

    pat3_score = models.ImageField(
        upload_to=get_doc_path_function('pat3_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน PAT3')

    anet_score = models.ImageField(
        upload_to=get_doc_path_function('anet_score'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='คะแนน A-NET ความถนัดทางวิศวกรรม')

    nat_id = models.ImageField(
        upload_to=get_doc_path_function('nat_id'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='สำเนาบัตรประจำตัวประชาชน หรือสำเนาบัตรนักเรียน')

    app_fee_doc = models.ImageField(
        upload_to=get_doc_path_function('app_fee_doc'),
        storage=uploaded_storage,
        blank=True,
        verbose_name='หลักฐานใบนำฝากเงินค่าสมัคร')

    # taken from application.models.PasswordRequestLog
    # TODO: an application for controlling quota
    last_uploaded_at = models.DateTimeField(auto_now=True)
    num_uploaded_today = models.IntegerField(default=0)


    def thumbnail_path(self, field_name):
        return get_doc_fullpath(self.applicant, 
                                get_field_thumbnail_filename(field_name))

    def preview_path(self, field_name):
        return get_doc_fullpath(self.applicant, 
                                get_field_preview_filename(field_name))

    def fulldoc_path(self, field_name):
        image = self.__getattribute__(field_name)
        return image.path

    def get_upload_fields(self, excluded=[]):
        applicant = self.applicant
        field_list = list(AppDocs.FormMeta.upload_fields)
        try:
            uses_gat_score = self.applicant.education.uses_gat_score
        except Education.DoesNotExist:
            uses_gat_score = True

        if uses_gat_score:
            field_list.remove('anet_score')
        else:
            field_list.remove('gat_score')
            field_list.remove('pat1_score')
            field_list.remove('pat3_score')

        # remove some fields
        for review_field in excluded:
            fname = review_field.short_name
            try:
                field_list.remove(fname)
            except ValueError:
                pass

        return field_list

    def get_required_fields(self, excluded=[]):
        fields = self.get_upload_fields(excluded)
        for f in AppDocs.FormMeta.optional_fields:
            if f in fields:
                fields.remove(f)        
        return fields

    def get_missing_fields(self, find_one=False):
        reviewed_fields = CompletedReviewField.get_for_applicant(self.applicant)
        required_fields = self.get_required_fields(excluded=reviewed_fields)
        missing = []
        for f in required_fields:
            if self.__getattribute__(f).name == '':
                missing.append(f)
        return missing

    def is_complete(self):
        missing_fields = self.get_missing_fields(find_one=True)
        return len(missing_fields)==0

    def has_uploaded_today(self):
        if not self.last_uploaded_at:
            return False
        today = date.today()
        today_datetime = datetime(today.year, today.month, today.day)
        #print self.last_uploaded_at, "today:", today_datetime
        return self.last_uploaded_at >= today_datetime

    def can_upload_more_files(self):
        """
        checks if a user can upload more documents. The criteria are:
        - the user hasn't uploaded the new files more than
        settings.MAX_DOC_UPLOAD_PER_DAY (set in settings.py) times.
        """
        if (self.has_uploaded_today() and
            self.num_uploaded_today >=
            settings.MAX_DOC_UPLOAD_PER_DAY):
            return False
        return True

    def update_upload_counter(self):
        #print "Today?", self.has_uploaded_today()
        if self.has_uploaded_today():
            self.num_uploaded_today += 1
        else:
            self.num_uploaded_today = 1


    @staticmethod
    def valid_field_name(field_name):
        return field_name in AppDocs.FormMeta.upload_fields    


    @staticmethod
    def get_verbose_name_from_field_name(field_name):
        field = AppDocs._meta.get_field_by_name(field_name)
        if field==None:
            return ''
        else:
            return field[0].verbose_name

    class FormMeta:
        """
        lists fields to be uploaded, and also lists optional fields.
        """
        upload_fields = [
            'gat_score',
            'pat1_score',
            'pat3_score',
            'anet_score',
            'nat_id',
            'app_fee_doc']

        optional_fields = [
            'picture', 
            'edu_certificate',
            'abroad_edu_certificate',
            'abroad_edu_certificate'
            ]
