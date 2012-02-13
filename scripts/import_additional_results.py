import codecs
import sys
import os

if len(sys.argv)!=2:
    print "Usage: import_additional_results [file.csv]"
    quit()

result_filename = sys.argv[1]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant
from result.models import AdditionalResult

def main():
    f = codecs.open(result_filename,encoding='utf8')
    lines = f.readlines()
    c = 0
    c1 = 0
    for l in lines:
        items = l.strip().split(',')
        if len(items)==7:
            nat_id, title, first_name, last_name, email, password, major = items
            try:
                a = Applicant.objects.get(national_id=nat_id)
            except:
                a = Applicant(national_id=nat_id,
                              title=title,
                              first_name=first_name,
                              last_name=last_name,
                              email=email)
                a.random_password()
                print 'created applicant for', nat_id
                c1 += 1


            a.has_additional_result = True
            a.additional_hashed_password = password
            a.save()

            additional_result = AdditionalResult(applicant=a,
                                                 name=major)
            additional_result.save()
            c += 1

    print "Imported %d applicants (%d created)" % (c,c1)

if __name__=='__main__':
    main()
