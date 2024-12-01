
import string
from collections import deque,defaultdict,Counter
from functools import reduce
from itertools import batched, starmap, accumulate, pairwise
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall(r'-?\d+',s))

f = "input19.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')


workflows = {name:[(f,goal) for rule in rest[:-1].split(',') for [f,goal] in [rule.split(':') if ':' in rule else (None,rule)]]
        for line in lgroups[0].split('\n') for [name,rest] in [(line.split('{'))]}

parts = [ints(line) for line in lgroups[1].split('\n')]

def matches(rule, part):
    if rule is None: return True
    i = "xmas".find(rule[0])
    return eval("part[i]"+rule[1:])

total = 0
for part in parts:
    wf = 'in'
    while wf not in ["R","A"]:
        for rule in workflows[wf]:
            if matches(rule[0],part):
                wf = rule[1]
                break
    if wf=="A":
        total += sum(part)

print(total)

def apply_rule(constraint, rg):
    if constraint is None: # all pass
        return [rg,None]
    i = "xmas".find(constraint[0])
    n = int(constraint[2:])
    yes = [t for t in rg]
    no = [t for t in rg]
    # incorrect (can expand the range), but the input is nice to us
    if constraint[1]=='<':  # set top of range to n
        yes[i] = (rg[i][0], n)
        no[i] = (n, rg[i][1])
    else:#set bottom of range  # >
        yes[i] = (n+1, rg[i][1])
        no[i] = (rg[i][0], n+1)
    return [new_rg if new_rg[i][0]<new_rg[i][1] else None for new_rg in [yes,no]]

start_range = [(1,4001) for _ in range(4)]
q = [('in', start_range)]
#assume DAG / no cycles so BFS should be fine
#handle overlapping ranges at the end

all_a = []

while q:
    nq = []
    for p in q:
        wf,rg = p
        for rule in workflows[wf]:
            yes,no = apply_rule(rule[0],rg)
            if yes:
                if rule[1]=="R":
                    pass  #delete/ignore (reject or empty)
                elif rule[1]=="A":
                    all_a.append(yes)  # store
                else:
                    nq.append((rule[1],yes))  # continue working
            rg = no
    q = nq

#assume non-overlapping: correct
total = 0
for rg in all_a:
    total+=reduce(lambda a,b:a*b, [c[1]-c[0] for c in rg])
#print(len(all_a))  # all_a ranges can be used to directly check if any part is accepted in O(579)
print(total)
