def extract_round(round_data):
    return (int(round_data[0]),int(round_data[1][-1]))

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
        row = dict([(f[0],items[f[1]]) for f in ROW_FIELDS])
        data = dict([(f[0],items[f[1]]) for f in DATA_FIELDS])
        
        k = data[GROUPING_FIELD]

        if k!=old_key:
            app_data = data
            app_data['scores'] = []
            scores.append(app_data)
        old_key = k

        app_data = scores[-1]
        app_data['scores'].append((round_key,row))

    return scores

def test_score_import(f):
    scores = extract_data(f)
    return scores[:3] + scores[-2:]


def score_import(f):
    pass
