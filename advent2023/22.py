
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

test="""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
# lines = test.split('\n')

bricks = [list(sorted((i[:3],i[3:]),key=lambda t:t[::-1])) for line in lines for i in [ints(line)]]
#assume sorted by Z

# print(bricks[:3])
#ground at z=0
# brick is resting if its lowest Z is at z=1
# or supported by another?
bricks = sorted(bricks,key=lambda t:t[0][2])
#Let fall
max_z = {}
occupied = {}
def highest_pos(brick):
    (x1,y1,_),(x2,y2,_) = brick
    return max(max_z.get((tx,ty),0) for ty in range(min(y1,y2),1+max(y1,y2)) for tx in range(min(x1,x2),1+max(x1,x2)))

def move(brick, dz):
    (x1,y1,z1),(x2,y2,z2) = brick
    return [(x1,y1,z1+dz),(x2,y2,z2+dz)]

def rg(brick):
    (x1,y1,z1),(x2,y2,z2) = brick
    return [(x,y,z)
            for x in range(min(x1,x2),1+max(x1,x2))
            for y in range(min(y1,y2),1+max(y1,y2))
            for z in range(min(z1,z2),1+max(z1,z2))
            ]

cant_remove = set()
supports = []
# let fall
for i in range(len(bricks)):
    b = bricks[i]
    nz = highest_pos(b)+1
    dz = nz-b[0][2]
    bricks[i]=move(b,dz)
    supports.append(set())
    for p in rg(bricks[i]):
        below = (p[0],p[1],p[2]-1)
        if below in occupied:
            #mark as unable to be removed
            supports[i].add(occupied[below])
        occupied[p]=i
        max_z[p[:2]]=p[2]
    supports[i]-={i}
    if len(supports[i])==1:
        cant_remove|=supports[i]

print("part 1:", len(bricks)-len(cant_remove))
#supports[i of brick]  : set of other bricks supporting i
# suppose we remove brick j
# then all bricks only supported by j will fall;
print(f"{len(bricks)=}")


#O(n^2)
tbl = {}
total = 0
rlb = range(len(bricks))
# for i
for i in reversed(range(len(bricks))):
    if i not in cant_remove: continue  # doesn't cause any collapse
    print("i=",i)
    collapsing = {i}
    changed = True
    while changed:
        changed = False
        add = {i for i in range(len(bricks)) if supports[i] and supports[i]<=collapsing}-collapsing # all supports are collapsing
        # print(add)
        if add:
            changed = True
            collapsing |= add
    t = len(collapsing)-1  # Other bricks that would fall
    # print(t)
    total += t
print(total)

