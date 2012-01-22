# -*- coding: utf-8 -*-
from application.models import GPExamDate, Applicant
from result.models import NIETSScores

def extract_round(round_data):
    return (int(round_data[0]),int(round_data[1][-1]))

def convert_data_field(x):
    if x=='-' or x=='':
        return 0
    else:
        return float(x)

def extract_data(f):
    NUM_SKIP = 14
    ROUND_FIELDS = (12,13)
    ROW_FIELDS = (
        ('pat1',14),
        ('pat3',28),
        ('gat',48),
        )
    GROUPING_FIELD = 'nat_id'
    DATA_FIELDS = (
        ('nat_id', 4), 
        ('first_name', 6),
        ('last_name', 9),
        )

    source = f.read()
    lines = source.split("\n")[NUM_SKIP:]

    scores = []
    old_key = ''
    for l in lines:
        items = l.split(",")
        if len(items) < 30:
            continue
        
        round_key = extract_round(tuple([items[i] for i in ROUND_FIELDS]))
        row = dict([(f[0],convert_data_field(items[f[1]])) for f in ROW_FIELDS])
        data = dict([(f[0],items[f[1]]) for f in DATA_FIELDS])
        
        k = data[GROUPING_FIELD]

        if k!=old_key:
            app_data = data
            app_data['scores'] = []
            scores.append(app_data)
            #print k
        old_key = k

        app_data = scores[-1]

        if GPExamDate.get_by_year_and_number(round_key[0],round_key[1])!=None:
            app_data['scores'].append((round_key,row))

    return scores

def test_score_import(f):
    scores = extract_data(f)
    return scores[:3] + scores[-2:]

def initialialize_empty_score_list():
    excount = len(GPExamDate.get_all())
    return [0] * excount * 3

def score_import(f):

    from datetime import datetime

    count = 0
    scores = extract_data(f)
    for s in scores:
        try:
            a = Applicant.objects.get(national_id=s['nat_id'])
        except Applicant.DoesNotExist:
            a = None
        if a==None:
            continue

        try:
            niets_scores = a.NIETS_scores
        except:
            niets_scores = NIETSScores(applicant=a)
            
        
        niets_scores.is_request_successful = True
        niets_scores.requested_at = datetime.now()

        score_list = initialialize_empty_score_list()

        for scr in s['scores']:
            y = scr[0][0]
            num = scr[0][1]
            d = GPExamDate.get_by_year_and_number(y,num)
            i = d.rank - 1

            score_list[i*3] = scr[1]['gat']
            score_list[i*3 + 1] = scr[1]['pat1']
            score_list[i*3 + 2] = scr[1]['pat3']

        niets_scores.score_list = ','.join([str(x) for x in score_list])
        niets_scores.save()
        count += 1

    return u'นำเข้าข้อมูลทั้งสิ้น %d คน' % count
