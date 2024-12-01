
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

f = "input.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

# i'm feeling a 2D grid problem coming...
#g = defaultdict(int, {x+y*1j: (c) for y,line in enumerate(lines) for x,c in enumerate(line)})

LR = lgroups[0]
rest = [line for line in lgroups[1].split('\n')]
d = {a.strip():(b[1:],c[:-1]) for line in rest for (a,t) in [line.split(" = ")] for (b,c) in [t.split(", ")]}
#print(d)
t = "AAA"
from itertools import cycle
for i, p in enumerate(cycle(LR)):
    if t=="ZZZ":
        print(i)
        break
    ti = "LR".index(p)
    t = d[t][ti]

#LCM
#brain fried

ps = [k for k in d.keys() if k[-1]=="A"]
print(len(ps))
hist = [dict() for pi in ps]  # history
has_z = [[] for pi in ps]
cycle_start = [0 for pi in ps]
cycle_len = [0 for pi in ps]  # multiple of len(LR)?
#while 1
for i, (state_i, c) in enumerate(cycle(enumerate(LR))):
    ti = "LR".index(c)
    for pi, p in enumerate(ps):
        if cycle_start[pi]!=0: continue
        if (state_i, p) in hist[pi]:
            cycle_start[pi] = hist[pi][(state_i, p)]
            cycle_len[pi] = i - cycle_start[pi]
            print((state_i, p), cycle_start[pi], i)
            continue
        # add this state to history
        hist[pi][(state_i, p)] = i  # steps to reach this state
        has_z[pi].append(p[-1]=="Z")
    if all(cycle_start): break
    # next state
    for pi in range(len(ps)):  # move all
        ps[pi] = d[ps[pi]][ti]

z_idx = [l.index(True) for l in has_z]
print(z_idx)
print(cycle_start)
print(cycle_len)
from math import lcm
total_len = lcm(*cycle_len)
print(total_len)
#ugh   overthought it. the problem is nice to us
