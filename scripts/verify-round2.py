
result_filename = '../data/round2/round2-assignment.csv'
score_filename = '../data/round1/round1-scores-nat.csv'
pref_filename = '../data/round2/round1-major-pref-w-major-choice.csv'
confirmation_filename = '../data/round2/round1-result-w-confirmation.csv'

def read_scores():
    scores = {}
    for l in open(score_filename).readlines():
        items = l.strip().split(',')
        scores[items[0]] = float(items[1])
    return scores

def read_pref():
    prefs = {}
    for l in open(pref_filename).readlines():
        l = l.strip()
        items = l.strip().split(',')

        if items[2]!='0':
            prefs[items[1]] = [int(x) for x in items[3:]]

    return prefs

def read_confirmation():
    confirmation = {}
    for l in open(confirmation_filename).readlines():
        l = l.strip()
        items = l.split(',')

        confirmation[items[0]] = (items[2]=='True')
    return confirmation


def read_result():
    results = {}
    for l in open(result_filename).readlines()[1:]:
        l = l.strip()
        items = l.split(',')

        results[items[0]] = int(items[2])
    return results

MAJORS = [1,2,3,4,5,6,7,8,9,101,102,103,104,105,106,201,202,203]

results = {}
prefs = {}
scores = {}

def validate(n,maj,confirmation):
    if n in confirmation and (not confirmation[n]):
        return
    if n not in results:
        if n not in prefs:
            #print 'waived: ', n
            pass
        else:
            if maj in prefs[n]:
                print 'BAD1', n
    else:
        r = results[n]
        if r==maj:
            return
        for p in prefs[n]:
            if p==maj:
                print 'BAD2', n
                return
            if p==r:
                return

def check(maj,confirmation):
    min_accepted = 10000
    count = 0
    for n,m in results.items():
        if m==maj:
            if scores[n] < min_accepted:
                min_accepted = scores[n]
            count += 1

    print maj, count, min_accepted

    for n,sc in scores.items():
        if sc >= min_accepted - 0.01:
            validate(n,maj,confirmation)


results = read_result()
prefs = read_pref()
scores = read_scores()
confirmation = read_confirmation()

for m in MAJORS:
    check(m,confirmation)
