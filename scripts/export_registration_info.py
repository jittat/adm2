# -*- coding: utf-8 -*-
import sys
import codecs
import re

if len(sys.argv)!=3:
    print "Usage: export_registration_info.py [nat_id_list] [output_filename]"
    quit()

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from confirmation.models import StudentRegistration
from application.models import Applicant, Major

school_data = {}

def normalize_school_name(school_name, school_province):
    if school_name.startswith(u'โรงเรียน'):
        school_name = school_name[8:]
    nname = re.sub(r'[ ()"]','',school_name)
    return u"%s---%s" % (nname,school_province)

def read_school_data(data_filename):
    f = codecs.open(data_filename,'r',encoding='utf-8')
    for l in f.readlines():
        items = l.strip().split(',')
        if len(items)==3:
            school_data[normalize_school_name(items[1],items[2])]=items[0]

def find_school_code(school_name, school_province):
    nn = normalize_school_name(school_name, school_province)
    if nn in school_data:
        return school_data[nn]
    else:
        print nn
        return ""

def build_row(applicant, registration, personal_info, major_number):
    if registration==None:
        registration = StudentRegistration()

    if applicant.title==u'นาย':
        gender = 'M'
        eng_title = 'Mr.'
    else:
        gender = 'F'
        eng_title = 'Miss'

    bd_year = personal_info.birth_date.year + 543
    birth_date_str = personal_info.birth_date.strftime("%d/%m") + "/" + str(bd_year)
    address = applicant.address.home_address
    education = applicant.education
    major_number_str = '0'*(3-len(str(major_number))) + str(major_number)
    major = Major.objects.get(number=major_number_str)

    if major_number<100:
        status = u'ปกติ'
    elif major_number<200:
        status = u'พิเศษ'
    else:
        status = u'นานาชาติ'

    return u','.join([u'"%s"' % s for s in
                      [ applicant.national_id,
                        registration.passport_number,
                        gender,
                        applicant.title,
                        applicant.first_name,
                        applicant.last_name,
                        eng_title,
                        registration.english_first_name.capitalize(),
                        registration.english_last_name.capitalize(),
                        personal_info.nationality,
                        personal_info.ethnicity,
                        registration.religion,
                        registration.birth_place,
                        birth_date_str,
                        address.number,
                        address.village_number,
                        "",
                        address.road,
                        address.district,
                        address.city,
                        address.province,
                        address.postal_code,
                        registration.home_phone_number,
                        registration.cell_phone_number,
                        education.school_name,
                        education.school_province,
                        find_school_code(education.school_name,
                                         education.school_province),
                        u'วิศวกรรมศาสตร์',
                        major.name,
                        u'รับตรง คณะวิศวกรรมศาสตร์',
                        status,
                        u'บางเขน',
                        u'มก.',
                        registration.father_title,
                        registration.father_first_name,
                        registration.father_last_name,
                        registration.father_national_id,
                        registration.mother_title,
                        registration.mother_first_name,
                        registration.mother_last_name,
                        registration.mother_national_id,
                        ]])

def main():
    read_school_data('../data/school-codes.csv')
    filename = sys.argv[1]
    fout = codecs.open(sys.argv[2],"w",encoding="utf-8")
    for line in open(filename).readlines():
        items = line.strip().split(",")
        if len(items)!=2:
            continue

        national_id = items[0]
        major_number = items[1]

        applicant = Applicant.objects.get(national_id=national_id)
        personal_info = applicant.personal_info

        try:
            registration = applicant.student_registration
        except:
            registration = None

        print >> fout, build_row(applicant, registration, personal_info, major_number)

if __name__ == '__main__':
    main()

