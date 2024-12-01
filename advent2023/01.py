
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input01.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

def first_last_dig(l, part=1):
    digs = [(x, str(x)) for x in range(10)]
    if part==2: digs += list(enumerate(["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]))
    first = min((l.find(dig), x) for x,dig in digs if dig in l)
    last = max((l.rfind(dig), x) for x,dig in digs if dig in l)
    return 10*first[1] + last[1]

print(sum(first_last_dig(l) for l in lines))
print(sum(first_last_dig(l, part=2) for l in lines))
