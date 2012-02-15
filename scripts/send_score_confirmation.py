from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

import time
import sys

from application.models import Applicant, SubmissionInfo
from result.models import  NIETSScores
from commons.email import send_score_confirmation_by_email
import commons

def main():
    for s in NIETSScores.objects.filter(is_request_successful=True).all():
        send_score_confirmation_by_email(s.applicant)

if __name__=='__main__':
    main()

    
