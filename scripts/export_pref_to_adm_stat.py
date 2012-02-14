import codecs
import sys
import os

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import NIETSScores
from application.models import Applicant

def main():
    uses_nat_id = ('--nat' in sys.argv)
    all_submitted_applicants = ('--all' in sys.argv)

    applicants = Applicant.objects.all()
    c = 0
    for a in applicants:
        if not a.is_submitted:
            continue

        if not all_submitted_applicants and not a.is_eligible():
            continue

        k = a.id
        if uses_nat_id:
            k = a.national_id
        l = [c,k,len(a.preference.majors)] + a.preference.majors

        print ','.join([str(i) for i in l])

        c += 1

if __name__=='__main__':
    main()

