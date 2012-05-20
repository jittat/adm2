# -*- coding: utf-8 -*-
from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

import time

from application.models import Applicant, PersonalInfo
from commons.email import adm_send_mail

def main():
    print 'Sending mails...'

    while True:
        try:
            nat_id = raw_input().strip()
        except:
            break

        print nat_id
        app = Applicant.objects.get(national_id=nat_id)
        subject = u"กรุณานำบัตรประชาชนมาในงานบัณฑิตยุคใหม่วันที่ 21 พ.ค."
        message = u"งานบัณฑิตยุคใหม่พรุ่งนี้สำหรับนิสิตใหม่ทุกคน อย่าลืมพกบัตรประชาชนไปด้วยนะครับ"
        adm_send_mail(app.get_email(), subject, message, False)

if __name__ == '__main__':
    main()
