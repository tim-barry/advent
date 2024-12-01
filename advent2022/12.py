
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('\d+',s))

f = "input12.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')




heightmap = [lmap(ord,line) for line in s.replace("S",'a').replace("E",'z').split()]
H = len(heightmap)
W = len(heightmap[0])
hmap2 = {x+1j*y: heightmap[y][x] for x in range(W) for y in range(H)}
# found by manual inspection
start = 0+20j
end = (W-25)+20j
#BFS backwards from end
dist = {end:0}
q = [end]
while start not in dist:
    p = q.pop(0)
    for adj in range(4):
        np = p + 1j**adj
        if np not in hmap2: # outofbounds
            continue
        if hmap2[np]+1 >= hmap2[p]: # source at most 1 below dest
            if np not in dist:
                dist[np] = dist[p]+1
                q.append(np)

print(dist[start])
aa = [p for p,h in hmap2.items() if h==ord('a')]
print(min(dist[p] for p in aa if p in dist))




