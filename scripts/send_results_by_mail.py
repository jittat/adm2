from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

import time
import sys

from application.models import Applicant, SubmissionInfo
from commons.email import adm_send_mail
import commons

def main():
    print 'Sending mails...'

    only_paid = '--paid' in sys.argv
    if settings.ADM_RESULT_MAIL_BUILD_BODY != None:
        body_function = getattr(commons.email, 
                                settings.ADM_RESULT_MAIL_BUILD_BODY)

    for s in SubmissionInfo.objects.select_related(depth=1).all():
        if only_paid and (not s.paid):
            continue

        applicant = s.applicant

        if settings.ADM_RESULT_MAIL_BUILD_BODY==None:
            print applicant.national_id, ' (no body function specified)'
            continue

        subject = settings.ADM_RESULT_MAIL_SUBJECT
        body = body_function(applicant)

        adm_send_mail(applicant.get_email(),
                      subject,
                      body,
                      priority='low')

if __name__ == '__main__':
    main()
