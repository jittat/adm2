# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from application.models import Applicant, Major
from application.models import SubmissionInfo
import os

@login_required
def list_by_majors(request):
    applicants = []
    submission_infos = SubmissionInfo.objects.order_by('-submitted_at').select_related(depth=1)

    majors = Major.get_all_majors()

    major_lists = dict([(int(m.number),{'major': m, 'applicants': []})
                        for m in majors])

    for s in submission_infos:
        applicant = s.applicant
        major_num = applicant.preference.majors[0]
        major_lists[major_num]['applicants'].append(applicant)

    return render_to_response("review/list_applicants_by_majors.html",
                              { 'major_lists': major_lists })

def format_address(address):
    o = u'%s %s' % (address.number , address.village_name)
    if address.village_number:
        o += u' หมู่ที่ %d' % (address.village_number,)
    if address.road:
        o += u' ถ. %s' % (address.road)
    o += u' %s %s %s' % (address.district, address.city, address.province)
    return o
        

@login_required
def report_applicants(request):
    from django.conf import settings

    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, Frame
    from reportlab.lib.styles import ParagraphStyle

    font_path = os.path.join(settings.PROJECT_DIR, 'media/fonts/')
    normal_font_file = os.path.join(font_path,'THSarabun.ttf')
    bold_font_file = os.path.join(font_path,'THSarabunBold.ttf')

    pdfmetrics.registerFont(TTFont('THSarabun', normal_font_file))
    pdfmetrics.registerFont(TTFont('THSarabunBold', bold_font_file))
    pdfmetrics.registerFontFamily('THSarabun',
                                  normal='THSarabun',
                                  bold='THSarabunBold')
    style = ParagraphStyle(name='normal', 
                           fontSize=15,
                           fontName='THSarabun',
                           leading=18)

    styleL = ParagraphStyle(name='large', 
                           fontSize=18,
                           fontName='THSarabun',
                           leading=20)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'filename=applicants.pdf'

    pdf = Canvas(response)
    pdf.setFont('THSarabun',14)

    submission_infos = SubmissionInfo.objects.order_by('submitted_at').select_related(depth=1)

    for a in [s.applicant for s in submission_infos]:
        content = []

        tx = u'<b>การสัมภาษณ์ผู้สมัครเข้าศึกษาต่อโควตา สสวท. และสอวน.</b><br/>'
        tx += u'<b>ผู้สมัคร:</b> <u>%s</u>   <b>หมายเลข:</b> <u>%s</u><br/>' % (a.full_name(), a.ticket_number())
        content.append(Paragraph(tx, styleL))


        major = a.preference.get_major_list()[0]
        tx = u'<b>สาขาที่สมัคร:</b> %s<br/>' % major.name

        education = a.education
        aedu = a.additional_education

        tx += u'<br/><b><u>ข้อมูลการศึกษา</u></b><br/>'
        tx += u'<b>สถานศึกษา</b>: ' + education.get_has_graduated_display()
        if education.has_graduated:
            tx += u'จาก'
        else:
            tx += u'ที่'
        tx += u' %s %s %s<br/>' % (education.school_name,
                               education.school_city,
                               education.school_province)
        tx += u'<b>คะแนนเฉลี่ย (5 ภาคการศึกษา):</b> %1.2f<br/>' % (aedu.gpax)

        if aedu.pat3!=None:
            tx += u'<b>คะแนน PAT3:</b> %.1f<br/>' % (aedu.pat3)

        tx += u'<b>ค่ายอบรม:</b> ผ่านการอบรม %s สาขา %s<br/>' % (aedu.get_training_round_display(),
                                               aedu.training_subject)

        tx += u'<br/><b>ที่อยู่:</b> %s<br/>' % format_address(a.address.home_address)
        tx += u'<b>สถานที่ติดต่อ:</b> %s<br/>' % format_address(a.address.contact_address)
        
        tx += u'<br/><b><u>การตรวจหลักฐาน</u></b><br/>'
        tx += u'  ............. ระเบียนแสดงผลการเรียน 5 ภาคการศึกษา (ฉบับจริง) พร้อมสำเนา 1 ชุด<br/>'
        tx += u'  ............. สำเนาทะเบียนบ้าน 1 ชุด<br/>'
        tx += u'  ............. บัตรประจำตัวประชาชน (ฉบับจริง) พร้อมสำเนา 1 ชุด<br/>'
        tx += u'  ............. หลักฐานแสดงการผ่านการอบรมค่ายโอลิมปิกวิชาการ<br/>'
        tx += u'  ............. สำเนาผลสอบ PAT3<br/>'
        if a.submission_info.is_paid:
            tx += u'  .....X....... ยืนยันการชำระเงินแล้ว<br/>'
        else:
            tx += u'  ............. หลักฐานการชำระเงินค่าสมัคร<br/>'

        tx += u'-' * 120 + u'<br/>'
        tx += u'(เนื้อที่สำหรับกรรมการสัมภาษณ์)'

        content.append(Paragraph(tx, style))
        f = Frame(0.9*inch, 0.5*inch, 6.9*inch, 10*inch, showBoundary=0)
        f.addFromList(content,pdf)
        pdf.showPage()

    pdf.save()

    return response
