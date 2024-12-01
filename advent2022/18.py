
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input18.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

test = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""".strip().split('\n')

data = lmap(ints,lines)
# data = lmap(ints,test)

mins = lmap(min, zip(*data))
maxs = lmap(max, zip(*data))

# print(mins)
# print(maxs)
# 0 ~ 21
s = set(map(tuple,data))
total = set((x,y,z)
            for x in range(mins[0]-1,maxs[0]+1)
            for y in range(mins[1]-1,maxs[1]+1)
            for z in range(mins[2]-1,maxs[2]+1))
outs = total-s

DIRS = range(6)
def move(c,d):
    i = d//2
    a = 1 if d%2==0 else -1
    return c[0]+a*(i==0), c[1]+a*(i==1), c[2]+a*(i==2)

def surface(coords):
    return sum(sum(move(c,d) not in coords for d in DIRS) for c in coords)

print(surface(s))

#floodfill from a point we know is outside
q = {(mins[0]-1,mins[1]-1,mins[2]-1)}
seen = set()  # can be seen from outside
# i=0
while q:
    nq = set()
    # print("len",len(q))
    for tp in q:
        # i+=1
        # if i%1000==0:
        #     print(i)
        seen.add(tp)
        for d in DIRS:
            np = move(tp,d)  # guaranteed not in q from parity
            if (np in outs) and (np not in seen) and (np not in nq):
                nq.add(np)
    q = nq

new=total-seen # all internal points, whether lava or airpocket
print(surface(new))









