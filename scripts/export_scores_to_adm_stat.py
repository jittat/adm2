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
        try:
            niets_scores = a.NIETS_scores
        except:
            niets_scores = None

        if not all_submitted_applicants and not a.is_eligible():
            continue

        if niets_scores and niets_scores.is_request_successful:
            k = a.id
            if uses_nat_id:
                k = a.national_id
            print "%s,%f" % (k,niets_scores.get_score())
            c += 1

if __name__=='__main__':
    main()

