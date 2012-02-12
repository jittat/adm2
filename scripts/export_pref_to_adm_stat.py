import codecs
import sys
import os

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import NIETSScores
from application.models import Applicant

def main():
    applicants = Applicant.objects.all()
    c = 0
    for a in applicants:
        if not a.is_submitted:
            continue

        l = [c,a.id,len(a.preference.majors)] + a.preference.majors

        print ','.join([str(i) for i in l])

        c += 1

if __name__=='__main__':
    main()

