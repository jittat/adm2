import codecs
import sys
from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant
from result.models import NIETSScores

fname = sys.argv[1]

f = codecs.open(fname,"w",encoding="utf8")

for a in Applicant.objects.all():
    s = None
    try:
        s = a.NIETS_scores
    except:
        s = None

    if s==None or not s.is_request_successful:
        continue

    slist = []
    for sx in s.as_list():
        if sx==-1:
            slist.append("")
        else:
            slist.append(str(sx))

    print >> f,u"\"%s\",\"%s\",%s,%f" % (
        a.national_id,
        a.full_name(),
        ",".join(slist),
        s.get_score())
