# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db import models

from application.fields import IntegerListField
from application.models import Applicant, Major

class ReportCategory(models.Model):
    result_set_id = models.IntegerField(null=True)
    name = models.CharField(max_length=5)
    order = models.IntegerField()

    _categories = None

    @staticmethod
    def is_cons(c):
        u"""
        >>> ReportCategory.is_cons(u'ก')
        True
        >>> ReportCategory.is_cons(u'ฮ')
        True
        >>> ReportCategory.is_cons(u'เ')
        False
        >>> ReportCategory.is_cons(u'แ')
        False
        """
        return (c >= u'ก') and (c <= u'ฮ')

    @staticmethod
    def get_category_name_from_first_name(first_name):
        u"""
        >>> ReportCategory.get_category_name_from_first_name('John')
        'J'
        >>> ReportCategory.get_category_name_from_first_name('john')
        'J'

        >>> print ReportCategory.get_category_name_from_first_name(u'สมชาย')
        ส
        >>> print ReportCategory.get_category_name_from_first_name(u'เกียรติ')
        ก
        >>> print ReportCategory.get_category_name_from_first_name(u'ใจดี')
        จ
        """
        if (((first_name[0] >= u'a') and (first_name[0] <= u'z')) or
            ((first_name[0] >= u'A') and (first_name[0] <= u'Z'))): # roman?
            return first_name[0].upper()
        
        for c in first_name:
            if ReportCategory.is_cons(c):
                return c
        
        return ''

    @staticmethod
    def get_category_by_name(result_set_id, name):
        if ReportCategory._categories==None:
            cat = {}
            for category in ReportCategory.objects.all():
                cat[(category.result_set_id, category.name)] = category
            ReportCategory._categories = cat
        return ReportCategory._categories[(result_set_id, name)]

    @staticmethod
    def get_category_by_app_first_name(result_set_id, first_name):
        return ReportCategory.get_category_by_name(
            result_set_id,
            ReportCategory.get_category_name_from_first_name(
                first_name))

    class Meta:
        ordering = ['order']


class QualifiedApplicant(models.Model):
    ticket_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=300)

    order = models.IntegerField()

    category = models.ForeignKey(ReportCategory)

    applicant = models.ForeignKey(Applicant)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u'%s %s %s' % (
            self.ticket_number,
            self.first_name,
            self.last_name)


class AdmissionRound(models.Model):
    number = models.IntegerField(unique=True)
    start_date = models.DateField()
    last_date = models.DateField()
    is_available = models.BooleanField(default=False)

    _recent_round = None
    _cache_timestamp = None

    class Meta:
        ordering = ['-number']

    @staticmethod
    def get_recent():
        from datetime import datetime, timedelta

        now = datetime.now()
        if ((not AdmissionRound._cache_timestamp) or
            (AdmissionRound._cache_timestamp + timedelta(minutes=1) < now)):
            rounds = AdmissionRound.objects.filter(is_available=True)

            if len(rounds)!=0:
                AdmissionRound._recent_round = rounds[0]
            else:
                AdmissionRound._recent_round = None

            AdmissionRound._cache_timestamp = now

        return AdmissionRound._recent_round


    @staticmethod
    def time_to_recent_round_deadline(now=None):
        adm_round = AdmissionRound.get_recent()
        if adm_round:
            if now==None:
                now = datetime.now()
            last = adm_round.last_date
            deadline = datetime(last.year, last.month, last.day)
            return deadline - now + timedelta(1)
        else:
            return timedelta.max

    def __unicode__(self):
        return "Round %d" % self.number

class AdmissionResult(models.Model):
    applicant = models.ForeignKey(Applicant, 
                                  related_name='admission_results')

    round_number = models.IntegerField(default=0)
    is_admitted = models.BooleanField()
    is_waitlist = models.BooleanField()
    
    admitted_major = models.ForeignKey(Major, null=True)

    additional_info = models.TextField(null=True)

    class Meta:
        ordering = ['round_number']

    @staticmethod
    def new_for_applicant(applicant):
        res = AdmissionResult(applicant=applicant,
                              is_admitted=False,
                              is_waitlist=False)
        return res



class ScoreStat:

    SUPER_ZMAX = 13

    def __init__(self, mean, sd, max_score):
        self.mean = mean
        self.sd = sd
        self.max_score = max_score

    def cal_score(self, x):
        if x==-1:
            return 0
        z = (x - self.mean) / self.sd
        return 0.5 + 0.5 * z / ScoreStat.SUPER_ZMAX

SCORE_STATS = [
    #{ 'gat': ScoreStat(78.09, 44.32, 290),
    #  'pat1': ScoreStat(88.33, 30.63, 300),
    #  'pat3': ScoreStat(108.66, 26.17, 240) },
    #{ 'gat': ScoreStat(93.10, 51.13, 287.5),
    #  'pat1': ScoreStat(87.11, 31.14, 300),
    #  'pat3': ScoreStat(97.86, 28.56, 260) },
    #{ 'gat': ScoreStat(106.78, 55.59, 292.5),
    #  'pat1': ScoreStat(63.56, 25.90, 270),
    #  'pat3': ScoreStat(86.73, 24.64, 237) },

    # mar53
    { 'gat': ScoreStat(130.78, 58.32, 295),
      'pat1': ScoreStat(64.00, 30.88, 294),
      'pat3': ScoreStat(103.20, 42.47, 276) },

    # jul53
    { 'gat': ScoreStat(128.43, 61.32, 300),
      'pat1': ScoreStat(56.26, 25.92, 300),
      'pat3': ScoreStat(83.54, 35.78, 300) },

    # oct53
    { 'gat': ScoreStat(139.38, 67.85, 300),
      'pat1': ScoreStat(48.34, 23.45, 300),
      'pat3': ScoreStat(121.25, 41.56, 300) },

    # mar54
    { 'gat': ScoreStat(171.89, 48.04, 297.5),
      'pat1': ScoreStat(64.22, 18.08, 274),
      'pat3': ScoreStat(101.95, 40.68, 270) },

    # dec54
    { 'gat': ScoreStat(130.59, 68.04, 300),
      'pat1': ScoreStat(39.64, 20.07, 288),
      'pat3': ScoreStat(83.45, 32.44, 267) },
    ]
EXAM_COUNT = len(SCORE_STATS)

class NIETSScores(models.Model):
    applicant = models.OneToOneField(Applicant,
                                     related_name='NIETS_scores')
    is_request_successful = models.NullBooleanField()
    requested_at = models.DateTimeField(null=True)
    score_list = models.CharField(max_length=200)

    @staticmethod
    def extract_gatpat_scores(score_list):
        scores = {'gat': [-1] * EXAM_COUNT,
                  'pat1': [-1] * EXAM_COUNT,
                  'pat3': [-1] * EXAM_COUNT}

        i = 0
        for e in range(EXAM_COUNT):
            for exam in ['gat','pat1','pat3']:
                scores[exam][e] = score_list[i]
                i += 1

        return scores

    def as_list(self):
        if self.score_list!='':
            return [float(s) for s in self.score_list.split(',')]
        else:
            return None

    def as_list_by_exam_round(self):
        if self.score_list=='':
            return None
        else:
            l = self.as_list()
            out = []
            while len(l)!=0:
                out.append(l[:3])
                l = l[3:]
            return out

    def as_calculated_list_by_exam_round(self):
        all_scores = self.as_list_by_exam_round()
        if not all_scores:
            return []

        exams = ['gat','pat1','pat3']
        scores = []
        best_scores = dict([(ex,(0,None)) for ex in exams])
        for e in range(EXAM_COUNT):
            rscores = {}
            i = 0
            for exam_name in exams:
                x = all_scores[e][i]
                n = SCORE_STATS[e][exam_name].cal_score(x) * 10000
                if x==-1:
                    x = None
                rscores[exam_name] = {
                    'raw': x,
                    'normalized': n,
                    'selected': False
                    }
                
                if n > best_scores[exam_name][0]:
                    best_scores[exam_name] = (n, rscores[exam_name])
                
                i+=1
            scores.append(rscores)

        for ex in exams:
            if best_scores[ex][1]:
                best_scores[ex][1]['selected'] = True
        return scores        

    def get_best_normalized_score(self, test_name):
        all_scores = self.as_list()
        scores = NIETSScores.extract_gatpat_scores(all_scores)
        best_score = 0
        raw_score = 0
        for i in range(EXAM_COUNT):
            x = scores[test_name][i]
            score = SCORE_STATS[i][test_name].cal_score(x)
            if score > best_score:
                best_score = score
                raw_score = x
        return best_score, raw_score

    def get_score(self):
        gat, gs = self.get_best_normalized_score('gat')
        pat1, p1s = self.get_best_normalized_score('pat1')
        pat3, p3s = self.get_best_normalized_score('pat3')

        score = (gat * 0.25 +
                 pat1 * 0.25 + 
                 pat3 * 0.5)
        return 10000.0 * score

    def get_best_test_scores(self):
        gat, gs = self.get_best_normalized_score('gat')
        pat1, p1s = self.get_best_normalized_score('pat1')
        pat3, p3s = self.get_best_normalized_score('pat3')
        return [gs, p1s, p3s]


class AdditionalResult(models.Model):
    applicant = models.OneToOneField(Applicant,
                                     related_name='additional_result')
    name = models.CharField(max_length=200)
    round_number = models.IntegerField()
    is_waived = models.BooleanField(default=False)
    waived_at = models.DateTimeField(blank=True,
                                     null=True,
                                     default=None)

    def __unicode__(self):
        return self.name
