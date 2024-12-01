
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
g = defaultdict(int, {x+y*1j: (c) for y,line in enumerate(lines) for x,c in enumerate(line)})

#/\ mirror |- splitter

# g = lines
# fw = [i for i,s in enumerate(line) if s=="/"]
#energized if visited
#bfs
def energ(start):
    visited = set()
    nodes = {start}  # loc, dir
    while not set(nodes)<=visited:
        nnodes = []
        nodes -= visited
        visited = visited | set(nodes)
        for p,d in nodes:
            if g[p]=='.' or (g[p]=='|' and d in [1j,-1j]) or (g[p]=='-' and d in [1,-1]):
                if p+d in g:
                    nnodes.append((p+d,d))
            elif g[p]=='|':
                # if d in [1j,-1j]:
                #     raise NotImplemented
                for nd in [-1j, 1j]:
                    if p+nd in g:
                        nnodes.append((p+nd,nd))
            elif g[p]=='-':
                # if d in [1,-1]:
                #     raise NotImplemented
                for nd in [-1, 1]:
                    if p+nd in g:
                        nnodes.append((p+nd,nd))
            elif g[p]=='/':
                nd = d*1j if d in [-1j,1j] else d/1j
                if p + nd in g:
                    nnodes.append((p + nd, nd))
            elif g[p] == '\\':
                nd = d/1j if d in [-1j, 1j] else d*1j
                if p + nd in g:
                    nnodes.append((p + nd, nd))
        # print(nnodes)
        nodes = set(nnodes)
        # print(len(set(nodes)))
    return len({p for p,d in visited})

W = len(lines[0])
H = len(lines)

print(energ((0,1)))

topdown = [(i,1j) for i in range(W)]
bottomup = [(i+((H-1)*1j),-1j) for i in range(W)]
fromLeft = [(i*1j, 1) for i in range(H)]
fromRight = [(W-1 + i*1j, -1) for i in range(H)]
a = topdown + bottomup + fromLeft + fromRight
res = lmap(energ, a)
print(max(res))
