
major_lower_bound = {
    1:5745.292787,
    2:5919.850775,
    3:6003.567644,
    4:5764.42141,
    5:5668.266131,
    6:5658.208876,
    7:5481.762589,
    8:5479.99643,
    9:5531.767956,
    101:5380.491784,
    102:5506.627158,
    103:5302.818362,
    104:5299.70587,
    105:5129.993458,
    106:5163.661248,
    201:5289.423683,
    202:5455.963321,
    203:5290.543237,
}

major_accept_num = {
    1:350,
    2:50,
    3:80,
    4:100,
    5:50,
    6:90,
    7:100,
    8:110,
    9:90,
    101:290,
    102:43,
    103:60,
    104:50,
    105:78,
    106:110,
    201:150,
    202:50,
    203:70,
}

score_filename = '../data/round-fin/regis-scores.csv'
pref_filename = '../data/round-fin/major-pref-w-mchoice.csv'

results = {}

def read_scores():
    s = {}
    for l in open(score_filename).readlines():
        i = l.split(',')
        if len(i)==2:
            s[i[0]] = float(i[1])
    return s

def read_pref():
    p = {}
    for l in open(pref_filename).readlines():
        i = l.split(',')
        if len(i)>=2:
            if int(i[2])>0:
                p[i[1]] = [int(x) for x in i[3:]]
            else:
                p[i[1]] = []
    return p

def main():
    scores = read_scores()
    pref = read_pref()

    results = dict([(mid,[]) for mid in major_accept_num.keys()])
    min_scores = dict([(mid,10000) for mid in major_accept_num.keys()])
    cur_num = dict([(mid,0) for mid in major_accept_num.keys()])

    for msc,nat in sorted([(-v,k) for k,v in scores.items()]):
        sc = -msc
        p = pref[nat]
        for r in p:
            if (cur_num[r] < major_accept_num[r] and
                sc > major_lower_bound[r]):

                cur_num[r] += 1
                results[r].append(nat)
                min_scores[r] = sc
                break
    
    for m in sorted(min_scores.keys()):
        #print m, cur_num[m], min_scores[m]
        for nat in results[m]:
            print "%s,%f,%d" % (nat,scores[nat],m)

    

if __name__=='__main__':
    main()
