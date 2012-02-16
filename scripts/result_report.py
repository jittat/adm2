import codecs
import sys
from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, MajorPreference
from result.models import NIETSScores, AdmissionResult

file_name = sys.argv[1]

round_number = 1

f = codecs.open(file_name,"w",encoding="utf8")
for r in AdmissionResult.objects.filter(round_number=round_number).all():
    a = r.applicant
    print >> f, u"%s,%s,%.3f,%d,%s,%s" % (
        a.national_id,
        a.full_name(),
        a.NIETS_scores.get_score(),
        int(r.admitted_major.number),
        r.admitted_major.name,
        ','.join([str(m) for m in a.preference.majors]))
f.close()
