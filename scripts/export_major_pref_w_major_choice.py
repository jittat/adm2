import codecs

import sys
if len(sys.argv)<3:
    print "Usage: export_major_pref_w_major_choice [round_number] [output.csv]"
    quit()
round_number = int(sys.argv[1])
file_name = sys.argv[2]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import SubmissionInfo, Applicant, Major, MajorPreference, PersonalInfo
from confirmation.models import AdmissionMajorPreference, AdmissionWaiver

from utils import get_submitted_applicant_dict

applicants = get_submitted_applicant_dict({
        'preference': MajorPreference,
        'personal_info': PersonalInfo,
        'submission_info': SubmissionInfo,
        })

f = codecs.open(file_name, encoding="utf-8", mode="w")

pref = {}

uses_nat_id =  '--nat' in sys.argv

SUBMISSION_RANK = {1: 2, # doc by mail
                   2: 1, # online
                   3: 3} # all by mail

for applicantion_id in sorted(applicants.keys()):
    applicant = applicants[applicantion_id]
    #if not applicant.submission_info.doc_reviewed_complete:
    #    continue

    if AdmissionWaiver.is_waived(applicant):
        majors = []
    else:
        admission_major_prefs = AdmissionMajorPreference.objects.filter(applicant=applicant).all()
        if len(admission_major_prefs)!=0:
            a_mj_pref = admission_major_prefs[0]
            majors = [int(m.number) for m in a_mj_pref.get_accepted_majors(check_admitted=False)]
        else:
            majors = applicant.preference.majors

    majors_str = ",".join([str(m) for m in majors])
    nat_id = applicant.personal_info.national_id
    submission_method = None
    k = applicant.id
    if uses_nat_id:
        k = applicant.national_id
    output_str = "%s,%s,%d,%s" % (
        applicant.ticket_number(),
        k,
        len(majors),
        majors_str)

    pref[nat_id] = (output_str,
                    submission_method)

for output, method in pref.itervalues():
    print >> f, output
