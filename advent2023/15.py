
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

# LAVA TIME??? FINALLY????? please

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

# i'm feeling a 2D grid problem coming...
#g = defaultdict(int, {x+y*1j: (c) for y,line in enumerate(lines) for x,c in enumerate(line)})

def H(s):
    cv = 0
    for c in s:
        cv += ord(c)
        cv = (cv*17)%256
    return cv

#box = H(label)
#op : =-

print(sum(H(part) for part in s.split(',')))

boxes = [dict() for _ in range(256)]

#actually nowadays dicts preserve insertion order
for part in s.split(','):
    if part[-1]=="-":
        lbl = part[:-1]
        box = boxes[H(lbl)]
        if lbl in box:
            del box[lbl]
    elif part[-2]=="=":
        lbl = part[:-2]
        focal = int(part[-1])
        box = boxes[H(lbl)]
        box[lbl] = focal
    else:
        raise NotImplemented

total = 0
for i, box in enumerate(boxes):
    for j,(k,v) in enumerate(box.items()):
        total += (i+1) * (j+1) * v
print(total)
