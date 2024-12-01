
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

f = "input17.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

tlines = """111111111111
999999999991
999999999991
999999999991
999999999991""".split()

# i'm feeling a 2D grid problem coming...
g = defaultdict(int, {x+y*1j: int(c) for y,line in enumerate(lines) for x,c in enumerate(line)})

#pathfinding

import heapq

#state: heuristic, heatloss, position, direction, line length
# Heuristic is heatloss + distance to goal (we want to minimize it); used as sort key for priority queue
# heat loss only incurred when entering
# line length: is number of consecutive moves in direction D to get to position p
# Hack: heappush complains that `complex` can't be compared with </>
#  so we 'unwrap' position into components (and the same for direction)
#   (we don't actually care about ordering with position and direction)
dest = (len(lines)-1)*1j + (len(lines[0])-1)

def adj(state):
    h, l, px,py, d, n = state
    p = complex(px,py)
    res = []
    for nd,nn in [((d-1)%4,1),((d+1)%4,1)]+([(d,n+1)] if n<3 else []):
        np = p+1j**nd
        if np in g:
            nl = l+g[np]  # add heatloss of entered square
            dpos = dest-np
            dist = abs(dpos.real)+abs(dpos.imag)
            nh = nl + dist  # lower heuristic better
            res.append((nh,nl,np.real,np.imag,nd,nn))
    return res

def adj2(state):
    h, l, px,py, d, n = state
    p = complex(px,py)
    res = []
    #ultra crucible
    # can continue in D (with new consecutive n+1) if n is less than 10; if n==10 must turn
    # can only turn if consecutive moves is 4 or more
    for nd,nn in ([((d-1)%4,1),((d+1)%4,1)] if n>=4 else [])+([(d,n+1)] if n<10 else []):
        np = p+1j**nd
        if np in g:
            nl = l+g[np]  # add heatloss of entered square
            dpos = dest-np
            dist = abs(dpos.real)+abs(dpos.imag)
            nh = nl + dist  # lower heuristic better
            res.append((nh,nl,np.real,np.imag,nd,nn))
    return res

for part in [0,1]:
    partfunc = [adj,adj2][part]
    q = [(len(lines)+len(lines[0]),0,0,0,0,0)]
    best = {}  # (pos,dir,linelen):heatloss
    # for part 2: need to have at least 4 linelen to stop at the end
    while q and not (complex(*q[0][2:4])==dest and (part==0 or q[0][-1]>=4)):
        cur = heapq.heappop(q)
        if cur[2:] in best:  #avoid circles: unnecessary?
            continue
        best[cur[2:]] = cur[1]
        for nx in partfunc(cur):
            heapq.heappush(q,nx)
    print(q[0][1])
