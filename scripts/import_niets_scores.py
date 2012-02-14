import codecs
import sys
import os

if len(sys.argv)!=2:
    print "Usage: import_niets_scores [timestamp]"
    quit()

timestamp = sys.argv[1]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from result.models import NIETSScores
from application.models import Applicant, PersonalInfo
from commons.email import send_score_import_success_by_email

REQUEST_PREFIX = 'req'
RESULT_PREFIX = 'results-'

EXAMS = ['mar53','jul53','oct53','mar54','dec54']

EXAM_COUNT = len(EXAMS)

req_filename = "%s%s.csv" % (REQUEST_PREFIX, timestamp)
result_filenames = ["%s%s-%s.csv" % (RESULT_PREFIX,timestamp,e) for e in EXAMS]

REQUIRED_FIELDS = ['citizen_id','GAT','PAT1','PAT3']
RESULT_KEY = 'citizen_id'

def check_input_files():
    for f in result_filenames + [req_filename]:
        if not os.path.exists(f):
            print "Abort: input not found:", f
            quit()

def read_result(fname):
    lines = open(fname).readlines()
    header = lines[0]
    lines = lines[1:]
    fields = header.strip().split(',')
    field_indices = [(f,fields.index(f)) for f in REQUIRED_FIELDS]
    key_index = fields.index(RESULT_KEY)

    results = {}

    for ln in lines:
        items = ln.strip().split(',')
        k = items[key_index]
        data = dict([(f,items[i]) for f,i in field_indices])

        results[k] = data

    return results


def read_national_ids(fname):
    nats = []
    for l in open(fname).readlines()[1:]:
        items = l.split(",")
        nats.append(items[1][1:-1])  # throw away quotes
    return nats

def result_exists(results,nat):
    for r in results:
        if nat in r:
            return True
    return False

def convert_data_field(x):
    if x=='-' or x=='':
        return 0
    else:
        if float(x)==0:
            print 'zero'
        return float(x)

def convert_scores(result):
    return [convert_data_field(result['GAT']),
            convert_data_field(result['PAT1']),
            convert_data_field(result['PAT3'])]
            
def combine_rounds(results,nat):
    scores = []
    for i in range(EXAM_COUNT):
        if nat in results[i]:
            scores += convert_scores(results[i][nat])
        else:
            scores += [0,0,0]
    return scores

def main():
    check_input_files()

    nat_ids = read_national_ids(req_filename)
    results = [read_result(fname) for fname in result_filenames]
    
    counter = 0

    for nat in nat_ids:
        apps = Applicant.objects.filter(national_id=nat)
        if len(apps)!=1:
            print 'Error applicant:', nat
            continue

        app = apps[0]

        try:
            niets_scores = app.NIETS_scores
            scores_exists = True
        except:
            niets_scores = NIETSScores()
            scores_exists = False

        if not result_exists(results, nat):
            print (u"Error,%s,%s,%s,%s" % 
                   (nat, 
                    app.full_name(), 
                    app.personal_info.phone_number,
                    app.email))
            niets_scores.applicant = app
            niets_scores.is_request_successful = False
            niets_scores.save()
            continue

        scores =  combine_rounds(results, nat)

        niets_scores.score_list = ','.join([str(s) for s in scores])
        niets_scores.applicant = app
        niets_scores.is_request_successful = True
        niets_scores.save()
        #send_score_import_success_by_email(app, True)
        counter += 1

    print "Successfully imported", counter, "applicants."

if __name__=='__main__':
    main()

