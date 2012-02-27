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

SCHOOL_NAME_PATCHES = {
    u'สาธิตมศวปทุมวัน---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยศรีนครินทรวิโรฒ ปทุมวัน',
    u'สาธิตมหาวิทยาลัยศรีนครินทร์วิโรฒปทุมวัน---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยศรีนครินทรวิโรฒ ปทุมวัน',
    u'สาธิตมศว.ประสานมิตรฝ่ายมัธยม---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยศรีนครินทรวิโรฒ ปทุมวัน',
    u'สาธิตมศวประสานมิตรฝ่ายมัธยม---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยศรีนครินทรวิโรฒ ปทุมวัน',
    u'สาธิตมศวประสานมิตรมัธยม---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยศรีนครินทรวิโรฒ ปทุมวัน',
    u'สาธิตมศวประสานมิตร---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยศรีนครินทรวิโรฒ ปทุมวัน',
    u'สาธิตมศว.ปทุมวัน---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยศรีนครินทรวิโรฒ ปทุมวัน',
    u'สาธิตมศว.ประสานมิตร---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยศรีนครินทรวิโรฒ ปทุมวัน',
    u'สาธิตปทุมวัน---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยศรีนครินทรวิโรฒ ปทุมวัน',

    u'สาธิตจุฬาฯ---กรุงเทพมหานคร':u'สาธิตจุฬาลงกรณ์มหาวิทยาลัย (ฝ่ายมัธยม)',
    u'สาธิตจุฬาลงกรณ์มหาวิทยาลัย---กรุงเทพมหานคร':u'สาธิตจุฬาลงกรณ์มหาวิทยาลัย (ฝ่ายมัธยม)',
    u'สาธิตจุฬาลงกรณ์มหาวิทยาลัยมัธยม---กรุงเทพมหานคร':u'สาธิตจุฬาลงกรณ์มหาวิทยาลัย (ฝ่ายมัธยม)',
    u'สาธิตจุฬาฝ่ายมัธยม---กรุงเทพมหานคร':u'สาธิตจุฬาลงกรณ์มหาวิทยาลัย (ฝ่ายมัธยม)',
    u'สาธิตจุฬาฯฝ่ายมัธยม---กรุงเทพมหานคร':u'สาธิตจุฬาลงกรณ์มหาวิทยาลัย (ฝ่ายมัธยม)',
    u'สาธิตจุฬา---กรุงเทพมหานคร':u'สาธิตจุฬาลงกรณ์มหาวิทยาลัย (ฝ่ายมัธยม)',

    u'สาธิตเกษตร---กรุงเทพมหานคร':u'สาธิตแห่งมหาวิทยาลัยเกษตรศาสตร์ ศูนย์วิจัยและพัฒนาการศึกษา',
    u'สาธิตแห่งมหาวิทยาลัยเกษตรศาสตร์---กรุงเทพมหานคร':u'สาธิตแห่งมหาวิทยาลัยเกษตรศาสตร์ ศูนย์วิจัยและพัฒนาการศึกษา',

    u'สาธิตมหาวิทยาลัยขอนแก่นศึกษาศาสตร์---ขอนแก่น':u'สาธิตมหาวิทยาลัยขอนแก่น (ศึกษาศาสตร์) ระดับมัธยม',

    u'สาธิตมหาวิทยาลัยรามคำแหง---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยรามคำแหง (ฝ่ายมัธยม)',
    
    u'บดินทรเดชาสิงห์สิงหเสนี๒---กรุงเทพมหานคร':u'บดินทรเดชา (สิงห์ สิงหเสนี) 2',
    u'บดิทรเดชาสิงห์สิงหเสนี๒---กรุงเทพมหานคร':u'บดินทรเดชา (สิงห์ สิงหเสนี) 2',
    u'บดินทรเดชาสิงห์สิงห์เสนี2---กรุงเทพมหานคร':u'บดินทรเดชา (สิงห์ สิงหเสนี) 2',
    u'บดินเดชาสิงห์สิงหเสนี2---กรุงเทพมหานคร':u'บดินทรเดชา (สิงห์ สิงหเสนี) 2',
    u'บดินทรเดชา2---กรุงเทพมหานคร':u'บดินทรเดชา (สิงห์ สิงหเสนี) 2',
    u'บดินทร2---กรุงเทพมหานคร':u'บดินทรเดชา (สิงห์ สิงหเสนี) 2',

    u'มงฟอร์ตวิทยาลัย---เชียงใหม่':u'มงฟอร์ตวิทยาลัย แผนกมัธยม',
    u'มงฟอร์ต---เชียงใหม่':u'มงฟอร์ตวิทยาลัย แผนกมัธยม',

    u'ยุพราชวิทยาลัยเชียงใหม่---เชียงใหม่':u'ยุพราชวิทยาลัย',

    u'สตรีวิทยา2---กรุงเทพมหานคร':u'สตรีวิทยา ๒',
    u'สตรีวิิทยา2---กรุงเทพมหานคร':u'สตรีวิทยา ๒',

    u'กาญจนาภิเษกวิทยาลัยนครปฐม---นครปฐม':u'กาญจนาภิเษกวิทยาลัย นครปฐม (พระตำหนักสวนกุหลาบมัธยม)',
    u'กาญจนาภิเ๋ษกวิทยาลัยนครปฐม---นครปฐม':u'กาญจนาภิเษกวิทยาลัย นครปฐม (พระตำหนักสวนกุหลาบมัธยม)',

    u'มหาวชิราวุธ---สงขลา':u'มหาวชิราวุธ จังหวัดสงขลา',
    u'มหาวิชราวุธ---สงขลา':u'มหาวชิราวุธ จังหวัดสงขลา',

    u'จุฬาภรณราชวิทยาลัย---พิษณุโลก':u'จุฬาภรณราชวิทยาลัย พิษณุโลก',

    u'สวนกุหลาบ---กรุงเทพมหานคร':u'สวนกุหลาบวิทยาลัย',

    u'เตรียมอุดมศึษา---กรุงเทพมหานคร':u'เตรียมอุดมศึกษา',
    u'สารสาสน์วิเทศบาบอน---สมุทรสงคราม':(u'สารสาสน์วิเทศบางบอน',u'กรุงเทพมหานคร'),

    u'ภ.ป.ร.ราชวิทยาลัยฯ---นครปฐม':u'ภ.ป.ร.ราชวิทยาลัย ในพระบรมราชูปถัมภ์',

    u'พรหมานุสรณ์---เพชรบุรี':u'พรหมานุสรณ์จังหวัดเพชรบุรี',

    u'เบญจมราชูทิศ---ราชบุรี':u'เบญจมราชูทิศ ราชบุรี',
    u'เบญจมราชูทิศ---จันทบุรี':u'เบญจมราชูทิศ จังหวัดจันทบุรี',
    u'เบญจมราชูทิศจ.จันทุบรี---จันทบุรี':u'เบญจมราชูทิศ จังหวัดจันทบุรี',
    u'เบญจมราชูทิศจันทบุรี---จันทบุรี':u'เบญจมราชูทิศ จังหวัดจันทบุรี',

    u'ราชวินิตบางแก้ว---สมุทรปราการ':u'ราชวินิตบางแก้ว ในพระบรมราชูปถัมภ์',

    u'สาธิตมหาวิทยาลัยราชภัฎนครปฐม---นครปฐม':u'สาธิตมหาวิทยาลัยราชภัฏนครปฐม',

    u'มัธยมสาธิตมหาวิทยาลัยราชภัฏบ้านสมเด็จเจ้าพระยา---กรุงเทพมหานคร':u'สาธิตมหาวิทยาลัยราชภัฏบ้านสมเด็จเจ้าพระยา',
}

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

failed_counter = 0

def find_school_code(school_name, school_province):
    global failed_counter
    nn = normalize_school_name(school_name, school_province)
    if nn in SCHOOL_NAME_PATCHES:
        p = SCHOOL_NAME_PATCHES[nn]
        if type(p)==tuple:
            nn = normalize_school_name(p[0],
                                       p[1])
        else:
            nn = normalize_school_name(p,
                                       school_province)
    if nn in school_data:
        return school_data[nn]
    else:
        print nn
        failed_counter += 1
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

    vnum = ''
    if address.village_number!=0 and address.village_number!=None:
        vnum = address.village_number

    return u','.join([u'"%s"' % s for s in
                      [ unicode(applicant.ticket_number()),
                        applicant.national_id,
                        registration.passport_number,
                        gender,
                        applicant.title,
                        applicant.first_name,
                        applicant.last_name,
                        eng_title,
                        registration.english_first_name,
                        registration.english_last_name.capitalize(),
                        personal_info.nationality,
                        personal_info.ethnicity,
                        registration.religion,
                        registration.birth_place,
                        birth_date_str,
                        address.number,
                        vnum,
                        registration.address_avenue,
                        address.road,
                        address.district,
                        address.city,
                        address.province,
                        address.postal_code,
                        registration.home_phone_number,
                        registration.cell_phone_number,
                        applicant.email,
                        find_school_code(education.school_name,
                                         education.school_province),
                        education.school_name,
                        education.school_province,
                        registration.school_type,
                        u'%1.2f' % (registration.GPA),
                        u'บางเขน',
                        '',
                        u'วิศวกรรมศาสตร์',
                        '',
                        major.name,
                        u'รับตรง คณะวิศวกรรมศาสตร์',
                        status,
                        unicode(applicant.submission_info.submitted_at.strftime('%d/%m/2555')),
                        unicode(applicant.submission_info.submitted_at.strftime('%H/%M/%S')),
                        u'0002',
                        u'เกษตรศาสตร์',
                        '',
                        registration.father_title,
                        registration.father_first_name,
                        registration.father_last_name,
                        registration.father_national_id,
                        registration.mother_title,
                        registration.mother_first_name,
                        registration.mother_last_name,
                        registration.mother_national_id,
                        ]
                      ])

def main():
    read_school_data('../data/school-codes.csv')
    filename = sys.argv[1]
    fout = codecs.open(sys.argv[2],"w",encoding="utf-8")
    for line in open(filename).readlines():
        items = line.strip().split(",")
        if len(items)!=3:
            continue

        national_id = items[0]
        major_number = int(items[2])

        applicant = Applicant.objects.get(national_id=national_id)
        personal_info = applicant.personal_info

        try:
            registration = applicant.student_registration
        except:
            registration = None

        print >> fout, build_row(applicant, registration, personal_info, major_number)

    print failed_counter

if __name__ == '__main__':
    main()

