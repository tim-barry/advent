
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input20.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

test = """1
2
-3
3
-2
0
4""".split()
# lines = test

data = lmap(int,lines)
L = len(data)

def get_mix(l, idx):
    for i in range(L):
        dist = l[i]
        src = idx.index(i)
        dest = src + dist
        t = idx.pop(src)
        idx.insert(dest%(L-1), t)
    return idx

def mix(l, n=1):
    mixer = list(range(len(l)))
    orig_l = l
    for i in range(n):
        mixer = get_mix(orig_l, mixer)
    l = [l[ni] for ni in mixer]
    return l

def coords(d):
    z = d.index(0)
    L = len(d)
    coords = d[(z+1000)%L], d[(z+2000)%L], d[(z+3000)%L]
    return sum(coords)

mixed = mix(data)
print(coords(mixed))

data2 = [d*811589153 for d in data]
mix2 = mix(data2,10)
print(coords(mix2))
