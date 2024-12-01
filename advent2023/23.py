
import string
import sys
from collections import deque,defaultdict,Counter
from functools import reduce
from itertools import batched, starmap, accumulate, pairwise
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall(r'-?\d+',s))

f = "input23.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

test = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
# lines = test.split()

# i'm feeling a 2D grid problem coming...
g = {x+y*1j: (c) for y,line in enumerate(lines) for x,c in enumerate(line)} #if c!='#'

#maze
def adj(p):
    j = [p+1j**d for d in range(4)]
    # if g[p]!='.':
    #     j = [j[">v<^".find(g[p])]]
    return [np for np in j if np in g and g[np]!='#']

start = 1
end = max(g.keys(), key=lambda p:p.real+p.imag) -1  # 1 left of edge

intersections = {k:[*a] for k in g.keys() if g[k]!='#' and len(a:=adj(k))>2}
intersections[start] = [start+1j]
intersections[end] = [end-1j,1]
print(intersections)
print(len(intersections))
# calculate undirected adjacency between intersections
Und = {}
Dir = {}
for i,a in intersections.items():  #does 2x the work
    neigh = {}
    di_neigh = {}
    for last in a: #adj
        # follow trail to next intersection
        slide_ok = g[last]=='.' or i+1j**(">v<^".find(g[last])) == last
        visited = {i}
        while last not in intersections:
            visited.add(last)
            last = [np for np in adj(last) if np not in visited][0]
        neigh[last] =len(visited)  # next intersection, distance
        if slide_ok:
            di_neigh[last] = len(visited)
    Und[i] = neigh
    Dir[i] = di_neigh
print(Dir)

def longest2(path,g):
    if path[-1]==end:
        return sum(g[i][j] for i,j in zip(path,path[1:]))
    return max((longest2(path+[n],g) for n in g[path[-1]].keys() if n not in path),default=0)

print(longest2([start],Dir))
# we take all paths... slow (~1 minute)
print(longest2([start],Und))

# sys.setrecursionlimit(1000_000)
def longest(path,last):
    while len(nx:= [p for p in adj(last) if p not in path])==1:
        last = nx[0]
        path=path|{last}
        if last==end:
            return len(path)-1 # includes start and end
    return max((longest(path|{np},np) for np in nx if np not in path), default=0)

# print(longest({1},1))

