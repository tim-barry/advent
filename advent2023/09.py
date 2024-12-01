
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

f = "input09.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

from math import comb
def get_coefs(hist):
    coef = []
    while any(hist):
        coef.append(hist[0])
        hist = [b-a for a,b in zip(hist[:-1], hist[1:])]
    return coef

def sol(hist):
    L = len(hist)
    coef = get_coefs(hist)
    ret = sum(c * comb(L,i) for i,c in enumerate(coef))
    return ret

def sol2(hist):
    L = len(hist)
    coef = get_coefs(hist)
    res = [coef[-1]]
    for t in range(len(coef)-2, -1, -1):
        res.append(coef[t] - res[-1])
    return res[-1]

hists = lmap(ints, lines)
r1 = lmap(sol, hists)
print(sum(r1))
r2 = lmap(sol2, hists)
print(sum(r2))
