import codecs
import sys
from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, MajorPreference
from result.models import NIETSScores, AdmissionResult

file_name = sys.argv[1]

round_number = 2

f = codecs.open(file_name,"w",encoding="utf8")
admitted = set([r.applicant_id for 
                r in AdmissionResult.objects.filter(round_number=round_number).all()])

for a in Applicant.objects.all():
    if not a.is_eligible():
        continue
    if a.id in admitted:
        continue

    sc = None
    try:
        sc = a.NIETS_scores
    except:
        pass

    if sc and sc.is_request_successful:
        print >> f, u"%s,%s,%.3f,%s" % (
            a.national_id,
            a.full_name(),
            a.NIETS_scores.get_score(),
            ','.join([str(m) for m in a.preference.majors]))

f.close()
