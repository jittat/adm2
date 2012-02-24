import codecs
import sys
from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, MajorPreference
from result.models import NIETSScores, AdmissionResult
from confirmation.models import AdmissionMajorPreference, AdmissionWaiver


file_name = sys.argv[1]

round_number = 2

f = codecs.open(file_name,"w",encoding="utf8")
for r in AdmissionResult.objects.filter(round_number=round_number).all():
    a = r.applicant

    if AdmissionWaiver.is_waived(a):
        majors = []
    else:
        admission_major_prefs = AdmissionMajorPreference.objects.filter(applicant=a).all()
        if len(admission_major_prefs)!=0:
            a_mj_pref = admission_major_prefs[0]
            majors = [int(m.number) for m in a_mj_pref.get_accepted_majors(check_admitted=False)]
        else:
            majors = a.preference.majors

    majors_str = ",".join([str(m) for m in majors])

    print >> f, u"%s,%s,%.3f,%d,%s,%s" % (
        a.national_id,
        a.full_name(),
        a.NIETS_scores.get_score(),
        int(r.admitted_major.number),
        r.admitted_major.name,
        majors_str)
f.close()
