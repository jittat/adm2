import codecs
import sys
from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, Major, MajorPreference

MAX_RANK = 3

fname = sys.argv[1]


stat = {}
for l in open(fname).readlines()[1:]:
    items = l.strip().split(',')
    nat_id = items[0]
    maj = int(items[2])

    a = Applicant.objects.get(national_id=nat_id)
    m = a.preference.majors
    #print "%s,%d,%d" % (a.national_id,maj,m.index(maj)+1)
    
    if maj not in stat:
        stat[maj] = [0,0,0]

    stat[maj][m.index(maj)] += 1

for m in sorted(stat.keys()):
    print m, stat[m]
