import functools
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

test = "?###???????? 3,2,1"

@functools.lru_cache(100)
def arrs(row, counts:tuple):
    if sum(counts)+len(counts)-1>len(row): return 0
    if len(counts)==0: return ("#" not in set(row))
    tot = 0
    if row[0] in "#?":  #try start a run here
        for t in range(counts[0]):  # count 3: 0123 are "#??." => OK, row[ct0]=="." OK
            if row[t] not in "#?": #invalid
                break
        else:
            if counts[0]==len(row) or row[counts[0]] in ".?":
                tot += arrs(row[counts[0]+1:], counts[1:])
    if row[0] in ".?":
        tot += arrs(row[1:], counts)
    return tot

#really this is a SAT solver day
tot = 0
for line in lines:
    a,b = line.split()
    b = eval(b) #tuple
    tot += arrs(a,b)
print(tot)

tot = 0
for line in lines:
    a,b = line.split()
    b = eval(b) #tuple
    tot += arrs("?".join([a]*5),b*5)
print(tot)

#damaged is #, op .
#run-length encoding
# solve of japanese puzzle thingy





