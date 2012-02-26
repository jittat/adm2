import codecs
import sys
import os

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import NIETSScores
from application.models import Applicant
from confirmation.models import StudentRegistration, AdmissionWaiver
def main():
    uses_nat_id = ('--nat' in sys.argv)

    registrations = StudentRegistration.objects.all()
    c = 0
    for reg in registrations:
        a = reg.applicant

        if a.admission_results.count()!=0 and not AdmissionWaiver.is_waived(a):
            niets_scores = a.NIETS_scores
            k = a.id
            if uses_nat_id:
                k = a.national_id
            print "%s,%f" % (k,niets_scores.get_score())
            c += 1

if __name__=='__main__':
    main()

