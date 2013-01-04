import codecs
import sys
import os

if len(sys.argv) < 2:
    print "Usage: import_clearing_results [fname] [--force]"
    quit()


from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import ClearingHouseResult
from application.models import Applicant, Major

def main():
    if ClearingHouseResult.objects.count()!=0:
        if "--force" not in sys.argv:
            print 'old results exist; use --force, to replace'
            quit()
        else:
            ClearingHouseResult.objects.delete()

    majors = Major.get_all_majors()
    mdict = dict([(int(m.number),m) for m in majors])

    lines = open(sys.argv[1]).readlines()
    for l in lines:
        items = l.strip().split(',')

        if len(items)!=3:
            print 'BAD LINE:', l
            continue
        
        nat,maj,pwd = items

        a = Applicant.objects.get(national_id=nat)

        ch = ClearingHouseResult(applicant=a,
                                 password=pwd)
        
        if maj!='0':
            m = mdict[int(maj)]
            ch.admitted_major = m
            ch.is_additional_result = False
        else:
            ch.is_additional_result = True

        ch.save()
        print a.national_id, ch.password

    
if __name__=='__main__':
    main()

