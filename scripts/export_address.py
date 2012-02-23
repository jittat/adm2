# -*- coding: utf-8 -*-
import sys
import codecs

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from confirmation.models import AdmissionMajorPreference, AdmissionConfirmation
from application.models import Applicant
from result.models import AdmissionResult

def prefix_if(st,pref):
    if st.strip()!='':
        return pref + st
    else:
        return ''

def expand_address(address):
    if address.village_number!=0 and address.village_number!=None:
        vnum = str(address.village_number)
    else:
        vnum = ''
    if address.village_name=='-':
        address.village_name=''
    if address.province!=u'กรุงเทพมหานคร':
        return (u"%s %s %s %s %s %s %s %s" % 
                (address.number,
                 prefix_if(vnum,u'หมู่ '),
                 prefix_if(address.village_name,u'หมู่บ้าน'),
                 prefix_if(address.road,u'ถ.'),
                 prefix_if(address.district,u'ต.'),
                 prefix_if(address.city,u'อ.'),
                 prefix_if(address.province,u'จ.'),
                 address.postal_code))
    else:
        return (u"%s %s %s %s %s %s %s %s" % 
                (address.number,
                 prefix_if(vnum,u'หมู่ '),
                 prefix_if(address.village_name,u'หมู่บ้าน'),
                 prefix_if(address.road,u'ถ.'),
                 prefix_if(address.district,u'แขวง'),
                 prefix_if(address.city,u'เขต'),
                 prefix_if(address.province,''),
                 address.postal_code))


def main():
    f = codecs.open(sys.argv[1],"w",encoding="utf8")
    for c in AdmissionConfirmation.objects.all():
        a = c.applicant
        ps = a.admission_major_preferences.all()
        if len(ps)>0:
            pp = ps[0]
            if (pp.ptype == 3) or (pp.ptype==4):
                continue

        print >>f, "%s,%s,\"%s\"" % (a.national_id, a.full_name(), expand_address(a.address.contact_address))


if __name__=='__main__':
    main()
