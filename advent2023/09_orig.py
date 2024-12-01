
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

tlines = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".split('\n')

from math import comb
def sol(hist):
    L = len(hist)
    coef = []
    while any(hist):
        coef.append(hist[0])
        hist = [b-a for a,b in zip(hist[:-1], hist[1:])]
    ret = sum(c * comb(L,i) for i,c in enumerate(coef))
    return ret

def sol2(hist):
    L = len(hist)
    coef = []
    while any(hist):
        coef.append(hist[0])
        hist = [b-a for a,b in zip(hist[:-1], hist[1:])]
    res = [coef[-1]]
    for t in range(len(coef)-2, -1, -1):
        res.append(coef[t] - res[-1])
    return res[-1]

hists = lmap(ints, lines)
r1 = lmap(sol, hists)
print(sum(r1))
r2 = lmap(sol2, hists)
print(sum(r2))
