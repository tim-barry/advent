
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall(r'-?\d+',s))

f = "input04.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')


grid = [ints(line) for line in lines]
L = 10+1
res = [len(set(row[1:L]) & set(row[L:])) for row in grid]
print(res)
r2 = [int(2**(r-1)) for r in res]
print("part1:", sum(r2))

counts = [1]*len(res)
for i in range(len(res)):
    wins = res[i]  # win x times on card i
    for t in range(wins):  # add that many of the next cards
        counts[i+t+1]+=counts[i]
print(counts)
print(sum(counts))