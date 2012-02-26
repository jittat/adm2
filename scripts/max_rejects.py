from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

import time
import sys

from application.models import Applicant, MajorPreference
from result.models import AdmissionResult

score_filename = '../data/round1/round1-scores-nat.csv'

def read_scores():
    scores = {}
    for l in open(score_filename).readlines():
        items = l.strip().split(',')
        scores[items[0]] = float(items[1])
    return scores

def main():
    max_sc = {}
    scores = read_scores()
    for nat,s in scores.items():
        applicant = Applicant.objects.get(national_id=nat)
        if applicant.admission_results.count()==0:
            for m in applicant.preference.majors:
                mnum = m
                if mnum not in max_sc:
                    max_sc[mnum] = s
                else:
                    if s > max_sc[mnum]:
                        max_sc[mnum] = s

    for mnum in sorted(max_sc.keys()):
        print mnum, max_sc[mnum]
                    

if __name__ == '__main__':
    main()
