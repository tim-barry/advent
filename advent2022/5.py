
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('\d+',s))

f = "input5.txt"

with open(f) as r:
    s = r.read()
    lgroups = s.rstrip().split('\n\n')

stacks = lgroups[0][:-1].split('\n')
ss = [[sl[4*i+1] for i in range(9)] for sl in stacks[:-1]]
ss = [list(''.join(tl).strip()[::-1]) for tl in zip(*ss)]

lines = lgroups[1].split('\n')
moves = [lmap(int,re.findall('\d+',line)) for line in lines]
for n,src,dst in moves:
    src -= 1
    dst -= 1
    moved = ss[src][-n:]
    ss[src] = ss[src][:-n]
    ss[dst] += moved[::]
print(''.join(stack[-1] for stack in ss))

