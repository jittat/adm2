from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

import time
import sys

from application.models import Applicant, SubmissionInfo
from result.models import  NIETSScores
from commons.email import send_clearing_house_result_confirmation_email
import commons

filename = '../data/clearing/clearing.csv'

def main():
    lines = open(filename).readlines()
    for l in lines:
        items = l.strip().split(',')
        if len(items)!=3:
            continue

        a = Applicant.objects.get(national_id=items[2])
        send_clearing_house_result_confirmation_email(a)
        print a.national_id

if __name__=='__main__':
    main()

    
