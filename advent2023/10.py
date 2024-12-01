
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
g = defaultdict(lambda:'.', {x+y*1j: c for y,line in enumerate(lines) for x,c in enumerate(line)})

print(set(g.values()))
def dirs(c):
    if c=="|": return -1j,1j
    elif c=="-": return -1,1
    elif c=="L": return -1j,1
    elif c=="7": return -1,1j
    elif c=="F": return 1,1j
    elif c=="J": return -1,-1j
    elif c=="S": return -1j,-1,1,1j
    elif c==".":
        return ()
    raise NotImplemented

def connects(p):
    c = g[p]
    if c=="S": return True
    if c==".": return False
    for d in dirs(c):
        if -d not in dirs(g[p+d]): #doesnt connect back
            return False
    return True

bconnects = {k:connects(k) for k in list(g.keys())}
# print(len(bconnects))
# print(bconnects[8+0j])
def left(k):
    return k + dirs(g[k])[0]
def right(k):
    return k + dirs(g[k])[1]


adj = {k:((left(k),right(k)) if g[k]!="S" else [k+1j**i for i in range(4)]) for k in bconnects.keys() if bconnects[k]}
changed = True
while changed:
    changed = False
    for k in list(adj.keys()):
        if g[k]=="S":  continue
        l,r = adj[k]
        if l not in adj or r not in adj:
            adj.pop(k)
            changed = True



# groups = {k:k for k in adj.keys()}
Sloc = next(k for k in adj.keys() if g[k]=="S")
tot = 0
#TODO actually determine which direction(s) are good
adj[Sloc] = adj[Sloc][1::2]  # after solving pt1
which_side = {k:0 for k in bconnects.keys()}
which_side[Sloc] = 2
turn = 0
# using this path we turn once clockwise, so the outside is on the left
path = [Sloc]
for nx in adj[Sloc][1:]:
    if nx not in adj: continue
    prev = Sloc
    cur = nx
    d = cur-prev
    while cur != Sloc:
        path.append(cur)
        which_side[cur] = 2 # on line
        nx = next(iter(set(adj[cur])-{prev}))
        nd = nx-cur
        #left and right directions
        l = d * -1j
        r = d * 1j
        if nd!=d:
            this_turn = nd/d   # 1j: cw, -1j: ccw
            turn += this_turn
            if this_turn == 1j: # cw/right
                if which_side[cur + l] == 0:
                    which_side[cur + l] = -1
                if which_side[cur+d]==0:
                    which_side[cur+d] = -1
            else: # ccw/left
                if which_side[cur + r] == 0:
                    which_side[cur + r] = 1
                if which_side[cur+d]==0:
                    which_side[cur+d] = 1
        else:
            if which_side[cur+l]==0:
                which_side[cur+l] = -1
            if which_side[cur+r]==0:
                which_side[cur+r] = 1
        #move
        prev = cur
        cur = nx
        d = nd
        tot += 1

    print((tot+1)//2)
    print(turn)
#flood fill L/R
while not all(which_side.values()):
    for k in which_side.keys():
        if which_side[k]==0:
            tadj = {which_side.get(k+1j**i, 2) for i in range(4)} - {2,0}
            if tadj:
                which_side[k] = tadj.pop()
print(list(which_side.values()).count(turn/4j))







