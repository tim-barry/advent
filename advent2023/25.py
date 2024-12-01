
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

test = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
# lines = test.split("\n")

G = [(a,b.split()) for line in lines for a,b in [line.split(': ')]]
g=defaultdict(list)
for a,l in G:
    g[a]+=l
    for t in l:
        g[t].append(a)
#too much mem to dump into graphviz directly
# the graph is highly connected; most nodes have 4-5 ish edges

#clustering : TODO lookup actual algo
# hacked together
# use the power of ARTIFICIAL INTELLIGENCE!!!!!!!
from random import random, randint
# p = {k:[random() for t in range(100)] for k in g.keys()}   # number of dimensions
p = {k:[randint(0,1) for t in range(10)] for k in g.keys()}   # number of dimensions
# C=0.1  # factor to move towards average of neighbors
C=0.8  # factor to move towards average of neighbors  (how fast do we hill-climb)
for t in range(30):  # training steps
    p = {k:[x*(1-C) + C*sum(L)/len(L)
            for x,*L in zip(p[k],*[p[k2] for k2 in g[k]])]
            for k in p.keys()}

# use as proxy to determine clusters
lo = min(p.values(),key=sum)
hi = max(p.values(),key=sum)
print("cluster distance:",sum(hi)-sum(lo))

print(lo,hi)
D = lambda k,X: sum((a-b)**2 for a,b in zip(p[k],X))
g1 = [k for k in p.keys() if D(k,lo)<D(k,hi)]
g2 = [k for k in p.keys() if k not in g1]

edge_cands = []   # use as a sanity check
for k1 in g1:
    for k2 in g2:
        if k2 in g[k1]:  # connected
            edge_cands.append((k1,k2))
print(len(edge_cands))
print(len(g1)*len(g2))  # poggers FUCK unlucky


