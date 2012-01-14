# -*- coding: utf-8 -*-
from django.db import models

from application.models import Applicant

class AdditionalEducation(models.Model):

    SUBJECT_CHOICES = (
        (u'คณิตศาสตร์',u'คณิตศาสตร์'),
        (u'เคมี',u'เคมี'),
        (u'ชีววิทยา',u'ชีววิทยา'),
        (u'ฟิสิกส์',u'ฟิสิกส์'),
        (u'คอมพิวเตอร์',u'คอมพิวเตอร์'),
        (u'ดาราศาสตร์',u'ดาราศาสตร์'))

    TRAINING_ROUND_CHOICES = (
        (2,'ค่าย 2 ของการอบรมสอวน. (อบรมที่ศูนย์แต่ละภูมิภาค)'),
        (3,'ค่ายอบรมระดับประเทศ (อบรมที่สสวท. ช่วงเดือนตุลาคม)'))

    applicant = models.OneToOneField(Applicant,
                                     related_name='additional_education')
    training_round = models.IntegerField(verbose_name=u'รอบการอบรมโอลิมปิกวิชาการ',
                                         choices=TRAINING_ROUND_CHOICES)
    training_subject = models.CharField(max_length=100,
                                        verbose_name= u'สาขาวิชา',
                                        choices=SUBJECT_CHOICES)
    gpax = models.FloatField(verbose_name=u'คะแนนเฉลี่ยรวม (GPAX) 5 ภาคการศึกษา')
    pat3 = models.FloatField(verbose_name=u'คะแนน PAT 3',
                             blank=True,
                             null=True)
