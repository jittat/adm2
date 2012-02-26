import sys
import codecs

if len(sys.argv)<2:
    print "Usage: export_results_with_confirmation.py [round_number] (optional-filename)"
    quit()

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import AdmissionResult
from confirmation.models import AdmissionConfirmation, AdmissionWaiver
from application.models import Applicant

from application.views.status import prepare_exam_scores

def main():
    round_number = int(sys.argv[1])
    if len(sys.argv)>2:
        filename = sys.argv[2]
        fp = codecs.open(filename,"w",encoding="utf-8")
    else:
        fp = None

    uses_nat_id = '--nat' in sys.argv

    results = (AdmissionResult.
               objects.
               filter(round_number=round_number).
               select_related(depth=1).
               all())

    c = 0
    for r in results:
        c += 1
        app = r.applicant
        exam_scores = prepare_exam_scores(app)
        confirmed = (app.admission_confirmations.all().count() > 0)

        if AdmissionWaiver.is_waived(app):
            confirmed = False

        if confirmed and app.get_student_registration()==None:
            print 'BAD!'
            quit()

        prefix = app.title
        name = app.first_name + ' ' + app.last_name
        k = app.id
        if uses_nat_id:
            k = app.national_id
        if not fp:
            print "%s,%d,%s,%.5f,%s,%s" % (k, int(r.admitted_major.number), str(confirmed), exam_scores['final_score'], prefix, name)
        else:
            print >>fp, u"%s,%d,%s,%.5f,%s,%s" % (k, int(r.admitted_major.number), str(confirmed), exam_scores['final_score'], prefix, name)


if __name__ == '__main__':
    main()

