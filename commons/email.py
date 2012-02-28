# -*- coding: utf-8 -*-
from django.conf import settings
from commons.utils import admin_email, submission_deadline_passed
from django.core.urlresolvers import reverse

AUTO_ADD_BR = False

# favour django-mailer but fall back to django.core.mail
try:
    if (("mailer" in settings.INSTALLED_APPS) and 
        settings.SEND_MAILS_THROUGH_DJANGO_MAILER):
        from mailer import send_mail
    else:
        from django.core.mail import send_mail
except:
    from django.core.mail import send_mail
    

def adm_send_mail(to_email, subject, message, force=False, priority='medium'):

    if settings.EMAIL_SENDER=='':
        sender = admin_email()
    else:
        sender = settings.EMAIL_SENDER

    send_real_email = True

    try:
        if settings.FAKE_SENDING_EMAIL:
            send_real_email = False
    except:
        pass
    
    if send_real_email:
        send_mail(subject,
                  message,
                  sender,
                  [ to_email ],
                  fail_silently=True,
                  priority=priority)
    else:
        print 'Does not send email'
        print 'Message:'
        print message


def send_password_by_email(applicant, password, force=False):
    """
    sends password to applicant.
    """
    subject = 'รหัสผ่านสำหรับการสมัครเข้าศึกษาแบบทางตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'
    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

ขอบคุณที่ได้ลงทะเบียนเพื่อสมัครเข้าศึกษาต่อที่คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ บางเขน

รหัสผ่านของคุณคือ %(password)s

คุณสามารถเข้าใช้ระบบได้โดยป้อนหมายเลขประจำตัวประชาชน %(national_id)s ที่คุณได้ลงทะเบียนไว้ แล้วป้อนรหัสผ่านด้านบน

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ กรุณาช่วยแจ้งผู้ดูแล้วด้วย

-โครงการรับสมัครตรง
"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'national_id': applicant.national_id,
    'password': password }
)
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_activation_by_email(applicant, activation_key, force=False):
    """
    sends activation key to an email.
    """

    base_path = settings.HTTP_BASE_PATH
    subject = 'รหัสสำหรับเปิดใช้งานบัญชีผู้ใช้สำหรับการสมัครเข้าศึกษาต่อคณะวิศวกรรมศาสตร์ มก.บางเขน'
    message = (
u"""เรียน คุณ %(firstname)s %(lastname)s

เราขอส่งรหัสสำหรับยืนยันอีเมล์เพื่อสำหรับบัญชีผู้ใช้ของระบบรับสมัครเข้าศึกษาต่อของคณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน

กรุณากดลิงก์ต่อไปนี้ %(link)s เพื่อยืนยันบัญชีที่คุณได้ลงทะเบียนไว้

เมื่อยืนยันเรียบร้อยแล้ว เราจะส่งรหัสผ่านมายังอีเมล์นี้อีกครั้งหนึ่ง

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ กรุณาช่วยแจ้งผู้ดูแลด้วย

-โครงการรับสมัครตรง
"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'link': base_path + reverse('apply-activate', 
                                args=[activation_key]) }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_submission_confirmation_by_email(applicant, force=False):
    """
    sends submission confirmation
    """
    subject = 'ยืนยันการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    greeting = u"จดหมายอิเล็กทรอนิกส์ฉบับนี้ ยืนยันว่าคณะวิศวกรรมศาสตร์ได้รับใบสมัครของคุณแล้ว"

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

%(greeting)s

หมายเลขประจำตัวประชาชนคือ %(national_id)s
รหัสยืนยันคือ %(verification)s
โดยการสมัครได้สมัครโดยใช้อีเมล์ %(email)s

คุณสามารถเข้าสู่ระบบรับสมัครเพื่อตรวจสอบสถานะใบสมัครได้โดยใช้รหัสประจำตัวประชาชนของคุณ

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'greeting': greeting,
    'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'national_id': applicant.national_id,
    'verification': applicant.verification_number(),
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_resubmission_confirmation_by_email(applicant, force=False):
    """
    sends submission confirmation
    """
    subject = 'ยืนยันการยื่นหลักฐานเพิ่มเติม การสมัครตรงคณะวิศวกรรมศาสตร์ (รอบ 2) ม.เกษตรศาสตร์ บางเขน'

    greeting = u"จดหมายอิเล็กทรอนิกส์ฉบับนี้ ยืนยันว่าคณะวิศวกรรมศาสตร์ได้รับการยื่นหลักฐานเพิ่มเติมของคุณแล้ว ใบสมัครของคุณจะเข้าสู่กระบวนการตรวจสอบหลักฐานซ้ำอีกครั้ง เมื่อการตรวจเรียบร้อยแล้วคณะจะส่งอีเมล์ยืนยันให้กับคุณอีกครั้ง"

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

%(greeting)s

เลขประจำตัวผู้สมัครของคุณคือ %(ticket)s
รหัสยืนยันคือ %(verification)s
โดยการสมัครได้สมัครโดยใช้อีเมล์ %(email)s

คุณสามารถเข้าสู่ระบบรับสมัครเพื่อตรวจสอบสถานะใบสมัครได้โดยใช้อีเมล์ %(email)s 

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'greeting': greeting,
    'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'ticket': applicant.ticket_number(),
    'verification': applicant.verification_number(),
    'submission_method': applicant.get_doc_submission_method_display(),
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)



def send_sub_method_change_notice_by_email(applicant, force=False):
    """
    sends doc submission method change notice
    """
    subject = 'แจ้งการเปลี่ยนแปลงวิธีการส่งหลักฐานเพื่อการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์นี้แจ้งให้คุณทราบว่าคุณได้ยกเลิกการส่งหลักฐานทางไปรษณีย์
และเปลี่ยนไปใช้การส่งหลักฐานแบบออนไลน์

กระบวนการดังกล่าวจะทำให้ผู้สมัครเปลี่ยนสถานะกลับไปเป็น<b>ผู้สมัครที่ยังไม่ได้ยื่นใบสมัคร</b>
และทำให้หมายเลขประจำตัวผู้สมัครหมายเลขเดิมที่ผู้สมัครเคยได้รับถูกยกเลิก
ผู้สมัครจะได้รับหมายเลขประจำตัวใหม่อีกครั้งเมื่อยื่นหลักฐานครบและได้ยืนยันหลักฐานอีกครั้ง

อย่าลืมว่าคุณจะต้องกลับไปยืนยันเอกสารและส่งใบสมัครอีกครั้ง

ถ้าคุณได้รับเมล์นี้ โดยไม่ได้เลือกเปลี่ยนการส่งข้อมูล อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ กรุณาช่วยแจ้งผู้ดูแล้วด้วย

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_validation_successful_by_email(applicant, force=False):
    """
    sends validation result
    """
    subject = 'การตรวจหลักฐานเพื่อการสมัครตรงเรียบร้อย'
    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์นี้แจ้งว่าคณะวิศวกรรมศาสตร์ได้ตรวจสอบหลักฐานที่คุณได้ยื่นให้กับคณะ
เพื่อใช้ในการสมัครเข้าศึกษาต่อ ด้วยวิธีรับตรง (รอบ 2) ประจำปีการศึกษา 2553 แล้ว

หลักฐานที่คุณส่งมานั้นครบถ้วนและสมบูรณ์แล้ว ขณะนี้คุณได้เข้าสู่กระบวนการคัดเลือกของคณะต่อไป
คณะจะประกาศรายชื่อผู้ได้รับการคัดเลือกเข้าศึกษาต่อแบบรับตรง (รอบ 2) ในวันที่ 11 พ.ค. 2553

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_validation_error_by_email(applicant, failed_fields, force=False):
    """
    sends validation result
    """

    error_list = []
    for field, result in failed_fields:
        error_list.append('%s - %s' % (field.name, result.applicant_note))
    errors = '\n'.join(error_list)

    if applicant.is_offline:
        extra_msg = u"""คุณจะต้องส่งหลักฐาน ภายในวันที่ 15 ธ.ค. นี้
เนื่องจากคุณสมัครโดยส่งใบสมัครและหลักฐานทุกอย่างทางไปรษณีย์ 
ในการส่งหลักฐานให้ระบุให้ชัดเจนว่าเป็นการส่งหลักฐานเพิ่มเติม
และให้ระบุหมายเลขประจำตัวผู้สมัครว่า %(ticket_number)s ด้วย""" % {'ticket_number': applicant.ticket_number()}
    elif applicant.online_doc_submission():
#        extra_msg = u"""คุณจะต้องส่งหลักฐานเพิ่มเติม ภายในวันที่ 15 ธ.ค. นี้  โดยใช้วิธีส่งแบบออนไลน์เช่นเดิม"""
        extra_msg = u"""คุณจะต้องส่งหลักฐานเพิ่มเติม ภายในวันที่ 9 พ.ค. นี้  โดยใช้วิธีส่งแบบออนไลน์เช่นเดิม"""
    else:
        extra_msg = u"""คุณจะต้องส่งหลักฐานเพิ่มเติม ผ่านทางระบบออนไลน์ ภายในวันที่ 9 พ.ค. 2553 นี้"""
#        extra_msg = u"""คุณจะต้องส่งหลักฐานเพิ่มเติม ภายในวันที่ 15 ธ.ค. นี้  โดยใช้วิธีส่งทางไปรษณีย์เช่นเดิม
#ถ้าคุณใช้การส่งหลักฐานทางไปรษณีย์ อย่าลืมพิมพ์ใบนำส่งแนบมาด้วย (สามารถพิมพ์ได้จากเว็บรับสมัคร)"""

    subject = 'การตรวจหลักฐานเพื่อการสมัครตรงไม่ผ่าน'
    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์นี้แจ้งว่าคณะวิศวกรรมศาสตร์ได้ตรวจสอบหลักฐานที่คุณได้ยื่นให้กับคณะ
เพื่อใช้ในการสมัครเข้าศึกษาต่อ ด้วยวิธีรับตรง ประจำปีการศึกษา 2553 แล้ว

หลักฐานที่คุณส่งมานั้นมีปัญหาดังนี้:
%(errors)s

%(extra_msg)s

ถ้ามีข้อสงสัยประการใด สามารถสอบถามได้ในเว็บบอร์ด หรือส่งเมล์หาผู้ดูแลที่ %(admin_email)s

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'errors': errors,
    'extra_msg': extra_msg,
    'admin_email': admin_email()
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_resubmission_reminder_by_email(applicant, force=False):
    """
    sends resubmission reminder result
    """

    subject = 'การส่งหลักฐานเพิ่มเติมในการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์'
    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายฉบับนี้ส่งมาเพื่อเตือนว่าใบสมัครเข้าศึกษาต่อแบบรับตรง
ที่คุณส่งให้กับทางคณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน
มีหลักฐานบางอย่างที่ไม่ผ่านการตรวจ

ถ้าคุณได้ส่งหลักฐานมาใหม่แล้ว เราต้องขออภัยที่แจ้งซ้ำซ้อน

ถ้าคุณต้องการส่งหลักฐานเพิ่มเติมในขณะนี้ 
ยังสามารถทำได้แต่ต้องส่งหลักฐานเพิ่มแบบออนไลน์เท่านั้น
โดยเข้าไปที่เว็บไซต์รับตรง http://admission.eng.ku.ac.th/adm/
เข้าใช้ระบบแล้วเลือก "ส่งหลักฐานเพิ่มเติม" ปุ่มสีน้ำเงินด้านขวา
ระบบนี้จะเปิดให้ส่งได้ถึงวันที่ 9 พ.ค. นี้เท่านั้น

หลักฐานที่ส่งแบบออนไลน์นั้นสามารถนำเข้าเครื่อง
โดยใช้การสแกนหรือการถ่ายรูปด้วยกล้องดิจิทัลก็ได้ 
(ดูรายละเอียดเกี่ยวกับความละเอียดในจากหน้าเว็บ)

ถ้ามีข้อสงสัยประการใด สามารถสอบถามได้ในเว็บบอร์ด 
หรือส่งเมล์หาผู้ดูแลที่ %(admin_email)s

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'admin_email': admin_email()
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_status_by_email_no_applicant(email, force=False):
    subject = 'สถานะการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'
    message = (
u"""เรียนผู้ใช้อีเมล์ %(email)s

ไม่พบข้อมูลการสมัครเข้าศึกษาแบบรับตรง ประจำปีการศึกษา 2553 
ที่คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตบางเขน

ถ้าคุณได้ส่งสมัครมาที่คณะ อาจเป็นไปได้ที่จดหมายยังไม่ถึง
หรือมีการกรอกข้อมูลอีเมล์ผิดพลาด  ให้รีบติดต่อที่ %(admin_email)s โดยด่วน 
พร้อมทั้งระบุชื่อ นามสกุล และหมายเลขประจำตัวประชาชน 
เพื่อให้ทางทีมงานตรวจสอบ

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'email': email,
    'admin_email': admin_email() }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(email, subject, message, force)


def send_status_by_email_not_submitted(email, applicants, force=False):
    subject = 'สถานะการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    applicant_names = '\n'.join([a.full_name() for a in applicants])

    message = (
u"""เรียนผู้ใช้อีเมล์ %(email)s

จากการตรวจสอบพบผู้ลงทะเบียนด้วยอีเมล์นี้ แต่ไม่มีข้อมูลการยืนยันใบสมัคร

โดยข้อมูลผู้ลงทะเบียนโดยใช้อีเมล์นี้มีรายชื่อดังนี้

%(applicant_names)s

เนื่องจากใบสมัครที่ส่งยังไม่ได้รับการยืนยัน ทางคณะจึงยังไม่ได้ประมวลผลใบสมัครของคุณ
ถ้าคุณต้องการยืนยันการสมัคร ให้รีบติดต่อผู้ดูทางอีเมล์ %(admin_email)s 
เพื่อให้ยืนยันและตรวจสอบหลักฐานโดยด่วน

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'email': email,
    'applicant_names': applicant_names,
    'admin_email': admin_email() }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(email, subject, message, force)


def summarize_applicant_status(applicant):
    if applicant.is_submitted:
        ticket_number = applicant.ticket_number()
        submission_status = u"สถานะใบสมัคร: ยืนยันแล้ว"
        if applicant.submission_info.has_been_reviewed:
            if applicant.submission_info.doc_reviewed_complete:
                review_result = u'ผ่าน'
            else:
                review_result = u'ไม่ผ่าน'                
            submission_status = submission_status + (
u"""
สถานะการตรวจสอบ: ตรวจสอบแล้ว เมื่อ %(doc_review_at)s
ผลการตรวจสอบ: %(doc_review_status)s
""" % { 'doc_review_at': applicant.submission_info.doc_reviewed_at.strftime("%H:%M, %d %b"),
        'doc_review_status': review_result })
            
        else:
            # has not been reviewed
            if applicant.submission_info.doc_received_at != None:
                doc_received_status = u"ได้รับเมื่อ " + applicant.submission_info.doc_received_at.strftime("%H:%M, %d %b")
            else:
                doc_received_status = u"ยังไม่ได้รับ"
            submission_status = submission_status + (
                u"""
สถานะการตรวจสอบ: ยังไม่ได้ตรวจสอบ
สถานะใบสมัคร: %(doc_received_status)s""" % { 'doc_received_status': doc_received_status })
            
    else:
        # not submitted
        ticket_number = u'ไม่มีหมายเลขผู้สมัคร'
        submission_status = u"สถานะใบสมัคร: ยังไม่ได้ยืนยัน"

    if not applicant.has_major_preference():
        pref_status = u"ยังไม่ได้เลือกอันดับของสาขา"
    else:
        pref_status = (u"อันดับของสาขาที่เลือกคือ:\n" + 
                       u'\n'.join([unicode(m) for m in  applicant.preference.get_major_list()]))
    status = (
u"""ชื่อ: %(full_name)s
หมายเลขผู้สมัคร: %(ticket_number)s
วิธีการส่งใบสมัคร: %(doc_submission_method)s

%(submission_status)s
%(pref_status)s
""" % { 
            'full_name': applicant.full_name(),
            'ticket_number': ticket_number,
            'doc_submission_method': applicant.get_doc_submission_method_display(),
            'submission_status': submission_status,
            'pref_status': pref_status
            }
)
    return status


def send_status_by_email(applicant, force=False):
    subject = 'สถานะการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'
    message = (
u"""เรียนคุณ %(first_name)s %(last_name)s

ด้านล่างเป็นข้อมูลการสมัครเข้าศึกษาต่อแบบรับตรงประจำปีการศึกษา 2553
คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน
พร้อมด้วยลำดับการเลือกสาขาของคุณ
โปรดตรวจสอบ และถ้าพบข้อผิดพลาดให้รีบแจ้งกับทางผู้ดูแล
ทางอีเมล์ %(admin_email)s โดยด่วน

%(status)s
ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'first_name': applicant.first_name,
    'last_name': applicant.last_name,
    'status': summarize_applicant_status(applicant), 
    'admin_email': admin_email()
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_status_by_email_many_submitted_apps(applicants, force=False):
    subject = 'สถานะการสมัครตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    statuses = u''
    counter = 1
    for a in applicants:
        statuses = statuses + (u"รายการที่ " + unicode(counter) + u"\n\n" + 
                               summarize_applicant_status(a) + u"\n")
        counter += 1

    message = (
u"""เรียนผู้ใช้อีเมล์ %(email)s

ระบบพบว่ามีข้อมูลของผู้ใช้หลายคนที่ใช้อีเมล์ %(email)s และมีการยื่นใบสมัครหลายครั้ง

ทั้งนี้สาเหตุอาจมาจากการส่งหลักฐานซ้ำซ้อน หรือการที่ทางเจ้าหน้าที่ป้อนข้อมูลซ้ำเข้าในระบบ
ข้อมูลซ้ำซ้อนนี้ไม่เป็นปัญหาต่อผู้สมัครแต่อย่างใด เพราะในการคัดเลือก 
คณะจะใช้ข้อมูลของผู้สมัครที่ผ่านการตรวจสอบเท่านั้น และจะตัดข้อมูลที่ไม่ผ่านทิ้งไป
อย่างไรก็ตาม ถ้ามีข้อมูลผ่านหลายชุดและผู้สมัครต้องการเลือกรายการที่ต้องการ
ให้รีบติดต่อกับทางผู้ดูแลทางอีเมล์ %(admin_email)s โดยด่วน

ด้านล่างเป็นข้อมูลการสมัครเข้าศึกษาต่อแบบรับตรงประจำปีการศึกษา 2553
คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน
พร้อมด้วยลำดับการเลือกสาขาของคุณ
โปรดตรวจสอบ และถ้าพบข้อผิดพลาดให้รีบแจ้งกับทางผู้ดูแล
ทางอีเมล์ %(admin_email)s โดยด่วน

%(statuses)s
ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'email': applicants[0].get_email(),
    'statuses': statuses,
    'admin_email': admin_email()
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicants[0].get_email(), subject, message, force)



def send_admission_status_problem_by_mail(email, force=False):
    subject = 'ผลการสมัครเข้าศึกษาต่อแบบรับตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    message = (
u"""เรียนผู้ใช้อีเมล์ %(email)s

ในการเรียกค้น เราพบว่ามีข้อมูลผู้ใช้หลายคนที่มีหมายเลขประจำตัวประชาชนไม่ตรงกันที่ใช้อีเมล์นี้
ทำให้เราไม่สามารถตรวจสอบผลการรับสมัครให้แบบอัตโนมัติได้

รบกวนผู้สมัครส่งเมล์สอบถามผลการรับสมัครโดยตรงที่ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'email': email,
    'admin_email': admin_email()
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicants[0].get_email(), subject, message, force)


def send_admission_status_by_mail(applicant, force=False):
    subject = u'ผลการสมัครเข้าศึกษาต่อแบบรับตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    if applicant.has_admission_results():
        adm_result = applicant.get_latest_admission_result()
        if adm_result.is_waitlist:
            result = u"""คุณมีชื่ออยู่ในรายชื่อสำรอง ดูข้อมูลเพิ่มเติมได้จาก<a href="http://admission.eng.ku.ac.th/adm/%s">หน้าประกาศผล</a>
สำหรับผู้ที่มีรายชื่ออยู่ในรายชื่อสำรอง คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์จะประกาศรายชื่อผู้มีสิทธิ์เข้าสอบสัมภาษณ์ในวันศุกร์ที่ 5 กุมภาพันธ์ 2553 ทางเว็บไซด์ <a href="http://admission.eng.ku.ac.th">โครงการรับตรง (http://admission.eng.ku.ac.th)</a>""" % (reverse("result-set-index", args=["waitlist"]),)
        else:
            result = u"""คุณผ่านการคัดเลือกให้เข้ารับการสัมภาษณ์เข้าศึกษาต่อแบบรับตรง (ดูข้อมูลเพิ่มเติมได้ที่<a href="http://admission.eng.ku.ac.th/adm/%(url)s">หน้าประกาศผลการรับสมัคร</a>)

สาขาที่ได้รับการคัดเลือก*: %(major)s
ข้อมูลการสัมภาษณ์: %(add_info)s

หมายเหตุ: สาขาที่ได้รับคัดเลือกอาจมีการเปลี่ยนแปลงได้ แต่จะเป็นสาขาที่อยู่ในอันดับที่ดีขึ้นเท่านั้น""" % {
                'url': reverse('result-set-index', args=['admitted']),
                'major':
                    (adm_result.admitted_major.number + ' ' + 
                     adm_result.admitted_major.name),
                'add_info': adm_result.additional_info }
    else:
        result = u"""คุณไม่ผ่านการคัดเลือกให้เข้ารับการสัมภาษณ์รอบที่ 1 อย่างไรก็ตาม ในวันที่ 5 ก.พ. 2553 จะมีการประกาศรายชื่อผู้มีสิทธิ์เพิ่มเติม กรุณาติดตามได้จากเว็บรับตรง 

นอกจากนี้ยังมีช่องทางอื่นในการเข้าศึกษาต่อที่คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตบางเขน กรุณาดูข้อมูลได้ที่เว็บ <a href="http://admission.eng.ku.ac.th/information/2553">http://admission.eng.ku.ac.th</a>"""

    message = (
u"""เรียนคุณ %(first_name)s %(last_name)s

ด้านล่างเป็นผลการสมัครเข้าศึกษาต่อแบบรับตรงประจำปีการศึกษา 2553
คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน

%(result)s

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'first_name': applicant.first_name,
    'last_name': applicant.last_name,
    'result': result,
    'admin_email': admin_email()
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_final_admission_status_by_mail(applicant, force=False):
    subject = u'ผลการสมัครเข้าศึกษาต่อแบบรับตรง คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    if applicant.has_admission_results():
        admission_result = applicant.get_latest_admission_result()
    else:
        from result.models import AdmissionResult

        admission_result = AdmissionResult.new_for_applicant(applicant)

    from django.template.loader import get_template
    from django.template import Context

    result = (get_template('emails/final_admission_status.txt')
              .render(Context({'applicant': applicant,
                               'admission_result': admission_result})))

    message = (
u"""เรียนคุณ %(first_name)s %(last_name)s

ด้านล่างเป็นผลการสมัครเข้าศึกษาต่อแบบรับตรงประจำปีการศึกษา 2553
คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ วิทยาเขตบางเขน

%(result)s

ถ้าคุณได้รับเมล์นี้โดยไม่ได้ลงทะเบียน อาจมีผู้ไม่หวังดีแอบอ้างนำอีเมล์คุณไปใช้ 
กรุณาช่วยแจ้งผู้ดูแลด้วยที่อีเมล์ %(admin_email)s

-โครงการรับสมัครตรง
"""
% { 'first_name': applicant.first_name,
    'last_name': applicant.last_name,
    'result': result,
    'admin_email': admin_email()
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_payment_acceptance_by_email(applicant, force=False):
    """
    sends payment acceptance
    """
    subject = 'แจ้งการรับชำระค่าสมัคร คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    greeting = u"จดหมายอิเล็กทรอนิกส์ฉบับนี้ แจ้งยืนยันว่าคณะวิศวกรรมศาสตร์ได้รับข้อมูลการชำระเงินค่าสมัครจากธนาคารเรียบร้อยแล้ว"

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

%(greeting)s

คุณสมัครโครงการรับตรง โดยใช้หมายเลขประจำตัวประชาชนคือ %(national_id)s
สมัครได้สมัครโดยใช้อีเมล์ %(email)s

คุณสามารถเข้าสู่ระบบรับสมัครเพื่อตรวจสอบสถานะใบสมัครได้โดยใช้รหัสประจำตัวประชาชนของคุณ

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'greeting': greeting,
    'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'national_id': applicant.national_id,
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force, priority='low')


def send_score_import_success_by_email(applicant, force=False):
    """
    sends score import success status
    """
    subject = 'แจ้งการนำเข้าข้อมูลคะแนน คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์ฉบับนี้ แจ้งยืนยันว่าคณะวิศวกรรมศาสตร์
ได้นำเข้าข้อมูลการสอบของผู้สมัครจากทาง สทศ. เรียบร้อยแล้ว

ผู้สมัครสามารถเข้าระบบเพื่อตรวจสอบความถูกต้อง 
และผลการคำนวณคะแนนได้ที่เว็บรับสมัครของโครงการรับตรง

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'email': applicant.get_email(), 
    'national_id': applicant.national_id,
    }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force, priority='low')


def send_admission_confirmation_by_email(applicant, force=False):
    """
    sends admission confirmation
    """
    subject = 'แจ้งการยืนยันสิทธิ์ คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์ฉบับนี้ แจ้งยืนยันว่าคณะวิศวกรรมศาสตร์
รับข้อมูลเพื่อการยืนยันสิทธิ์จากผู้สมัครแล้ว

ถ้าผู้สมัครไม่ได้แจ้งยืนยันสิทธิ์ กรุณารีบติดต่อผู้ดูแลทางอีเมล์ %(admin_email)s โดยด่วน

ขอบคุณ
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'admin_email': admin_email() }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_admission_waive_by_email(applicant, force=False):
    """
    sends admission waive
    """
    subject = 'แจ้งการสละสิทธิ์ คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์ฉบับนี้ แจ้งยืนยันว่าคุณได้ขอสละสิทธิ์การเข้าศึกษาต่อผ่านทางโครงการรับตรงแล้ว

ถ้าผู้สมัครไม่ได้แจ้งขอสละสิทธิ์ กรุณารีบติดต่อผู้ดูแลทางอีเมล์ %(admin_email)s โดยด่วน

ขอบคุณที่สนใจโครงการรับตรง
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'admin_email': admin_email() }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_admission_unwaive_by_email(applicant, force=False):
    """
    sends admission unwaive
    """
    subject = 'แจ้งการยกเลิกการสละสิทธิ์ คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน'

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายอิเล็กทรอนิกส์ฉบับนี้ แจ้งยืนยันว่าคุณได้ขอยกเลิกการสละสิทธิ์การเข้าศึกษาต่อผ่านทางโครงการรับตรงแล้ว
อย่างไรก็ตาม คุณยังไม่ได้กรอกข้อมูลขอยืนยันสิทธิ์ ดังนั้น ถ้าคุณต้องการยืนยันสิทธิ์ คุณต้องเข้าไปกรอกข้อมูลด้วย

ถ้าผู้สมัครไม่ได้แจ้งขอยกเลิกการสละสิทธิ์ กรุณารีบติดต่อผู้ดูแลทางอีเมล์ %(admin_email)s โดยด่วน

ขอบคุณที่สนใจโครงการรับตรง
โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'admin_email': admin_email() }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_payment_reminder_by_email(applicant, force=False):
    """
    sends payment reminder
    """
    subject = 'แจ้งเตือนกำหนดการชำระเงินค่าสมัคร โครงการรับตรง วิศวกรรมศาสตร์ ม.เกษตร'

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายนี้แจ้งเตือนผู้สมัครว่ากำหนดการชำระเงินค่าสมัครโครงการรับตรงคือวันที่ 15 ก.พ. 2555
ผู้สมัครจะต้องชำระเงินภายในวันดังกล่าว จึงจะมีสิทธิ์เข้ารับการคัดเลือกผ่านโครงการนี้

ถ้าผู้สมัครชำระเงินในวันที่ 14 ก.พ. 2555 แล้ว ทางโครงการต้องขออภัยที่ผู้สมัครได้รับอีเมล์นี้ด้วย
สำหรับสถานะการชำระเงินนั้น ทางโครงการจะได้รับข้อมูลจากธนาคารในวันที่ 15 ช่วงเช้า
คาดว่าผู้สมัครจะสามารถเข้ามาตรวจสอบได้ภายหลังเวลา 10:00 น.

ถ้ามีข้อสงสัยสามารถสอบถามได้ทางอีเมล์ %(admin_email)s

-โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'admin_email': admin_email() }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force)


def send_score_confirmation_by_email(applicant, force=False):
    """
    sends score confirmation
    """
    subject = 'แจ้งยืนยันคะแนน โครงการรับตรง วิศวกรรมศาสตร์ ม.เกษตร'

    try:
        sc = applicant.NIETS_scores.get_score()
    except:
        return

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

จดหมายฉบับนี้แจ้งผู้สมัครว่าทางคณะวิศวกรรมศาสตร์ได้ดึงคะแนนจากสทศ. เรียบร้อยแล้ว

คะแนนที่จะใช้ในการคัดเลือกของผู้สมัครคือ %(score).3f

ผู้สมัครสามารถอ่านวิธีการคำนวณคะแนนได้จากลิงก์
http://admission.eng.ku.ac.th/2555/admission/direct/criteria
และทดลองคำนวณคะแนนได้ที่
http://admission.eng.ku.ac.th/2555/admission/direct/score-cal

ถ้ามีข้อสงสัยสามารถสอบถามได้ทางอีเมล์ %(admin_email)s

-โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'score': sc,
    'admin_email': admin_email() }
)
    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force,
                  priority='low')


def admission_result_round1_mail_body(applicant):
    result = applicant.get_latest_admission_result()

    if not applicant.is_eligible():
        return u"""เรียน คุณ %(first_name)s %(last_name)s

คุณไม่มีสิทธิ์เข้ารับการคัดเลือก เนื่องจากไม่ได้ชำระค่าสมัครในเวลาที่กำหนด

อย่างไรก็ตาม ถ้าคุณสนใจเข้าศึกษาต่อที่คณะวิศวกรรมศาสตร์ คุณยังสามารถสมัครผ่านทางแอดมิชชันกลางได้
อ่านรายละเอียดได้ที่ http://admission.eng.ku.ac.th/2555/admission/central

ด้วยความเคารพ
-ทีมงานเว็บรับสมัคร""" % { 'first_name': applicant.first_name,
                       'last_name': applicant.last_name }    

    if not result:
        return u"""เรียน คุณ %(first_name)s %(last_name)s

คุณไม่ผ่านการคัดเลือกเข้าศึกษาต่อโครงการรับตรง ในรอบที่ 1

อย่างไรก็ตาม ในวันที่ 24 ก.พ. 2555 จะมีการประกาศผู้มีสิทธิ์เข้าศึกษาต่อรอบที่ 2 
ทางทีมงานจะแจ้งผลทางอีเมล์และผู้สมัครสามารถตรวจสอบผลรอบสองได้จากเว็บ
http://admission.eng.ku.ac.th/adm/
ในวันดังกล่าว

ด้วยความเคารพ
-ทีมงานเว็บรับสมัคร""" % { 'first_name': applicant.first_name,
                       'last_name': applicant.last_name }

    else:
        return u"""เรียน คุณ %(first_name)s %(last_name)s

ขอแสดงความยินดีด้วย คุณผ่านการคัดเลือกให้เข้าศึกษาต่อโครงการรับตรง รอบที่ 1
สาขาที่ได้รับการคัดเลือก: %(major)s

คุณจะต้องเข้าระบบยืนยันสิทธิ์ออนไลน์ที่
http://admission.eng.ku.ac.th/adm/
เพื่อยืนยันสิทธิ์ในวันที่ 18 - 21 ก.พ. 2555 โดยป้อนข้อมูลเพิ่มเติมสำหรับการเคลียริงเฮาส์
และเลือกทางเลือกในการพิจารณาสาขาในการจัดอันดับรอบต่อไป

อ่านรายละเอียดเกี่ยวกับการยืนยันสิทธิ์ได้ที่ http://admission.eng.ku.ac.th/2555/admission/direct/confirmation

เมื่อผู้สมัครได้ยืนยันสิทธิ์กับทางคณะวิศวกรรมศาสตร์แล้ว ในวันที่ 27 ก.พ. 2555 ผู้สมัครจะได้รหัสยืนยันสิทธิ์ผ่านระบบเคลียริงเฮาส์ของสอท.
ซึ่งผู้สมัครจะต้องเข้าระบบไปยืนยันสิทธิ์อีกครั้งในวันที่ 11 - 17 มีนาคม 2555  จึงจะมีสิทธิ์เข้าศึกษาต่อในโครงการรับตรง

ในวันที่ 28 - 29 ก.พ. 2555 คณะวิศวกรรมศาสตร์จัดกิจกรรมโครงการเลือกแนวทางวางอนาคต Open House ผู้สมัครที่สนใจเยี่ยมชมคณะสามารถเข้าร่วมงานได้

อนึ่ง ในปีการศึกษา 2555 นี้ โครงการรับตรง คณะวิศวกรรมศาสตร์ไม่มีการเก็บเงินค่าประกันสิทธิ์แต่อย่างใด

ด้วยความเคารพ
-ทีมงานเว็บรับสมัคร""" % { 'first_name': applicant.first_name,
                       'last_name': applicant.last_name,
                       'major': result.admitted_major.name }


def admission_result_round2_mail_body(applicant):
    result = applicant.get_latest_admission_result()

    if not applicant.is_eligible():
        return None

    if not result:
        if applicant.get_student_registration()==None:
            return u"""เรียน คุณ %(first_name)s %(last_name)s

คุณไม่ผ่านการคัดเลือกเข้าศึกษาต่อโครงการรับตรง ในรอบที่ 2

อย่างไรก็ตาม คุณยังมีสิทธิ์เข้าศึกษาต่อที่คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน ผ่านทางการแอดมิชชันกลาง

อ่านกำหนดการและจำนวนการรับได้จากลิงก์: 
http://admission.eng.ku.ac.th/2555/admission/central

(หมายเหตุ จำนวนรับของแอดมิชชันกลางอาจมีการปรับได้ กรุณาติดตามข้อมูล)

ด้วยความเคารพ
-ทีมงานเว็บรับสมัคร""" % { 'first_name': applicant.first_name,
                       'last_name': applicant.last_name }
        else:
            return u"""เรียน คุณ %(first_name)s %(last_name)s

คุณไม่ผ่านการคัดเลือกเข้าศึกษาต่อโครงการรับตรง ในรอบที่ 2

อย่างไรก็ตาม เนื่องจากคุณได้ยืนยันสิทธิ์เพื่อขอเลื่อนอันดับไว้ในรอบการคัดเลือกก่อน 
คุณจึงยังมีสิทธิ์เข้ารับการพิจารณาในการจัดอันดับรอบสุดท้ายก่อนส่งชื่อที่ระบบเคลียริงเฮาส์

ดังนั้นกรุณากลับมาตรวจสอบผลในรอบต่อไปในวันที่ 27 เพื่อรักษาสิทธิ์การเข้าศึกษาต่อของคุณ

ด้วยความเคารพ
-ทีมงานเว็บรับสมัคร""" % { 'first_name': applicant.first_name,
                       'last_name': applicant.last_name }

    else:
        if applicant.admission_results.all().count()==1:
            return u"""เรียน คุณ %(first_name)s %(last_name)s

ขอแสดงความยินดีด้วย คุณผ่านการคัดเลือกให้เข้าศึกษาต่อโครงการรับตรง รอบที่ 2
สาขาที่ได้รับการคัดเลือก: %(major)s

คุณจะต้องเข้าระบบยืนยันสิทธิ์ออนไลน์ที่
http://admission.eng.ku.ac.th/adm/
เพื่อยืนยันสิทธิ์ภายในวันที่  26 ก.พ. 2555 โดยป้อนข้อมูลเพิ่มเติมสำหรับการเคลียริงเฮาส์
และเลือกทางเลือกในการพิจารณาสาขาในการจัดอันดับรอบต่อไป

อ่านรายละเอียดเกี่ยวกับการยืนยันสิทธิ์ได้ที่ http://admission.eng.ku.ac.th/2555/admission/direct/confirmation

เมื่อผู้สมัครได้ยืนยันสิทธิ์กับทางคณะวิศวกรรมศาสตร์แล้ว ในวันที่ 27 ก.พ. 2555 ผู้สมัครจะได้รหัสยืนยันสิทธิ์ผ่านระบบเคลียริงเฮาส์ของสอท.
ซึ่งผู้สมัครจะต้องเข้าระบบไปยืนยันสิทธิ์อีกครั้งในวันที่ 11 - 17 มีนาคม 2555  จึงจะมีสิทธิ์เข้าศึกษาต่อในโครงการรับตรง

ในวันที่ 28 - 29 ก.พ. 2555 คณะวิศวกรรมศาสตร์จัดกิจกรรมโครงการเลือกแนวทางวางอนาคต Open House ผู้สมัครที่สนใจเยี่ยมชมคณะสามารถเข้าร่วมงานได้

อนึ่ง ในปีการศึกษา 2555 นี้ โครงการรับตรง คณะวิศวกรรมศาสตร์ไม่มีการเก็บเงินค่าประกันสิทธิ์แต่อย่างใด

ด้วยความเคารพ
-ทีมงานเว็บรับสมัคร""" % { 'first_name': applicant.first_name,
                       'last_name': applicant.last_name,
                       'major': result.admitted_major.name }
        else:
            return u"""เรียน คุณ %(first_name)s %(last_name)s

ขอแสดงความยินดีด้วย คุณผ่านการคัดเลือกให้เข้าศึกษาต่อโครงการรับตรง รอบที่ 2
สาขาที่ได้รับการคัดเลือก: %(major)s

คุณได้ยืนยันสิทธิ์แล้วตั้งแต่รอบแรก ดังนั้นคุณไม่จำเป็นต้องดำเนินการใด ๆ อีก

อย่างไรก็ตาม ถ้าคุณเลือกขอเลื่อนอันดับขึ้นมามากกว่าสาขาที่ได้รับคัดเลือกนี้ตั้งแต่ในรอบก่อน
สำหรับรอบนี้ โครงการยังเปิดโอกาสให้คุณขอคงสาขาที่ได้รับคัดเลือกเป็นสาขา %(major)s ได้
โดยไม่ขอรับการพิจารณาเลื่อนอีก  ถ้าคุณต้องการคงสาขาดังกล่าว คุณสามารถเข้าไปเลือกได้ในระบบ
ได้จนถึงในวันที่  26 ก.พ. 2555 ที่ลิงก์
http://admission.eng.ku.ac.th/adm/

ในวันที่ 27 ก.พ. 2555 ผู้สมัครจะได้รหัสยืนยันสิทธิ์ผ่านระบบเคลียริงเฮาส์ของสอท.
ซึ่งผู้สมัครจะต้องเข้าระบบไปยืนยันสิทธิ์อีกครั้งในวันที่ 11 - 17 มีนาคม 2555  จึงจะมีสิทธิ์เข้าศึกษาต่อในโครงการรับตรง

ในวันที่ 28 - 29 ก.พ. 2555 คณะวิศวกรรมศาสตร์จัดกิจกรรมโครงการเลือกแนวทางวางอนาคต Open House ผู้สมัครที่สนใจเยี่ยมชมคณะสามารถเข้าร่วมงานได้

ด้วยความเคารพ
-ทีมงานเว็บรับสมัคร""" % { 'first_name': applicant.first_name,
                       'last_name': applicant.last_name,
                       'major': result.admitted_major.name }


def read_password(password):
    PASSWORDING = {
        'a':u'เอ',
        'b':u'บี',
        'c':u'ซี',
        'd':u'ดี',
        'e':u'อี',
        'f':u'เอฟ',
        'g':u'จี',
        'h':u'เอช',
        'i':u'ไอ',
        'j':u'เจ',
        'k':u'เค',
        'l':u'แอล',
        'm':u'เอ็ม',
        'n':u'เอ็น',
        'o':u'โอ',
        'p':u'พี',
        'q':u'คิว',
        'r':u'อาร์',
        's':u'เอส',
        't':u'ที',
        'u':u'ยู',
        'v':u'วี',
        'w':u'ดับเบิลยู',
        'x':u'เอ็กซ์',
        'y':u'วาย',
        'z':u'แซด',
        '0':u'ศูนย์',
        '1':u'หนึ่ง',
        '2':u'สอง',
        '3':u'สาม',
        '4':u'สี่',
        '5':u'ห้า',
        '6':u'หก',
        '7':u'เจ็ด',
        '8':u'แปด',
        '9':u'เก้า',
        }

    return ' '.join([PASSWORDING[c] for c in password])
            

def send_clearing_house_info_by_email(applicant, force=False):
    """
    sends clearing house info
    """
    subject = 'ผลการคัดเลือกรับตรง วิศวกรรมศาสตร์ มก. และรหัสผ่านสำหรับเข้าระบบเคลียริงเฮาส์'

    try:
        clearing_result = applicant.clearing_house_result
    except:
        print 'no result', applicant.national_id
        return

    if not clearing_result.is_additional_result:
        message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

ขอแสดงความยินดีด้วย คุณผ่านการคัดเลือกเข้าศึกษาต่อในคณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์
ผ่านทางระบบรับตรง
สาขา %(major)s
และได้ยืนยันสิทธิ์ครบถ้วน

คณะวิศวกรรมศาสตร์จะส่งชื่อคุณเข้าระบบเคลียริงเฮาส์ 
โดยรหัสผ่านที่คุณจะใช้เข้าระบบเคลียริงเฮาส์คือ

%(password)s

คำอ่านของรหัสผ่าน (เพื่อความชัดเจน): %(password_read)s
      
คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์
จะส่งรหัสระบุตัวบุคคลเพื่อใช้ในการยืนยันสิทธิ์การเข้าศึกษาผ่านเว็บไซต์
http://www.cuas.or.th ตั้งแต่ วันที่ 11 -17 มีนาคม 2555
ผู้ผ่านการคัดเลือกที่ต้องการเข้าศึกษาต่อจะต้องไปยืนยันสิทธิ์การเข้าศึกษาต่อผ่านระบบเคลียริงเฮาส์
ภายในวันและเวลาดังกล่าว

หากผู้ผ่านการคัดเลือกมีสิทธิ์เข้าศึกษาไม่ดำเนินการใดๆ
จะถือว่าสละสิทธิ์การเข้าศึกษาในระบบรับตรงของมหาวิทยาลัย/สถาบัน/กลุ่มสถาบัน
ที่เข้าร่วมในระบบเคลียริ่งเฮาส์ของปีการศึกษา 2555

ถ้ามีข้อสงสัยสามารถสอบถามได้ทางอีเมล์ %(admin_email)s

-โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'major': clearing_result.admitted_major.name,
    'password': clearing_result.password,
    'password_read': read_password(clearing_result.password),
    'admin_email': admin_email() }
)
    else:
        subject = 'ผลการคัดเลือกโควตา วิศวกรรมศาสตร์ มก. และรหัสผ่านสำหรับเข้าระบบเคลียริงเฮาส์'
        message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

ขอแสดงความยินดีด้วย คุณผ่านการคัดเลือกเข้าศึกษาต่อในคณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์
ผ่านทางระบบโควตา
สาขา %(major)s
และได้ยืนยันสิทธิ์ครบถ้วน

คณะวิศวกรรมศาสตร์จะส่งชื่อคุณเข้าระบบเคลียริงเฮาส์ 
โดยรหัสผ่านที่คุณจะใช้เข้าระบบเคลียริงเฮาส์คือ

%(password)s

คำอ่านของรหัสผ่าน (เพื่อความชัดเจน): %(password_read)s
      
คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเกษตรศาสตร์
จะส่งรหัสระบุตัวบุคคลเพื่อใช้ในการยืนยันสิทธิ์การเข้าศึกษาผ่านเว็บไซต์
http://www.cuas.or.th ตั้งแต่ วันที่ 11 -17 มีนาคม 2555
ผู้ผ่านการคัดเลือกที่ต้องการเข้าศึกษาต่อจะต้องไปยืนยันสิทธิ์การเข้าศึกษาต่อผ่านระบบเคลียริงเฮาส์
ภายในวันและเวลาดังกล่าว

หากผู้ผ่านการคัดเลือกมีสิทธิ์เข้าศึกษาไม่ดำเนินการใดๆ
จะถือว่าสละสิทธิ์การเข้าศึกษาในระบบรับตรงของมหาวิทยาลัย/สถาบัน/กลุ่มสถาบัน
ที่เข้าร่วมในระบบเคลียริ่งเฮาส์ของปีการศึกษา 2555

ถ้ามีข้อสงสัยสามารถสอบถามได้ทางอีเมล์ %(admin_email)s

-โครงการรับสมัคร คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'major': applicant.additional_result.name,
    'password': clearing_result.password,
    'password_read': read_password(clearing_result.password),
    'admin_email': admin_email() }
)

    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force,
                  priority='low')


def send_sorry_email(applicant, force=False):
    """
    sends sorry email
    """
    subject = 'ผลการคัดเลือกรับตรง วิศวกรรมศาสตร์ มก.'

    message = (
u"""เรียนคุณ %(firstname)s %(lastname)s

เราเสียใจที่ต้องแจ้งกับคุณว่า จากการที่คุณได้เคยยืนยันสิทธิ์กับทางคณะฯ 
เมื่อประกาศผลการคัดเลือกในรอบที่ 1 หรือ 2 และได้ขอพิจารณาเลื่อนอันดับ
และถ้าไม่ได้เลื่อนขอสละสิทธิ์นั้น

จากผลการคัดเลือกในรอบสุดท้ายพบว่า คุณไม่ได้รับการเลื่อนอันดับ 
ดังนั้นคณะจึงพิจารณาว่าคุณได้ขอสละสิทธิ์การเข้าศึกษาต่อ

อย่างไรก็ตาม คุณยังมีสิทธิ์เข้าศึกษาต่อที่คณะวิศวกรรมศาสตร์ ม.เกษตรศาสตร์ บางเขน 
ผ่านทางการแอดมิชชันกลาง

อ่านกำหนดการและจำนวนการรับได้จากลิงก์: 
http://admission.eng.ku.ac.th/2555/admission/central

(หมายเหตุ จำนวนรับของแอดมิชชันกลางอาจมีการปรับได้ กรุณาติดตามข้อมูล)

ด้วยความเคารพ
-โครงการรับตรง คณะวิศวกรรมศาสตร์"""
% { 'firstname': applicant.first_name, 
    'lastname': applicant.last_name,
    'admin_email': admin_email() }
)

    if AUTO_ADD_BR:
        message = message.replace('\n','<br/>\n')
    adm_send_mail(applicant.get_email(), subject, message, force,
                  priority='low')
