import codecs
import sys
import os

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import NIETSScores
from application.models import Applicant

def main():
    uses_nat_id = False
    if len(sys.argv) > 1 and sys.argv[1]=='--nat':
        uses_nat_id = True

    applicants = Applicant.objects.all()
    c = 0
    for a in applicants:
        if not a.is_submitted:
            continue

        k = a.id
        if uses_nat_id:
            k = a.national_id
        l = [c,k,len(a.preference.majors)] + a.preference.majors

        print ','.join([str(i) for i in l])

        c += 1

if __name__=='__main__':
    main()

