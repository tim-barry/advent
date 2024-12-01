import functools
import itertools
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
from pprint import pprint
from typing import Set, Any


def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input16.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

test = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip()
# lines = test.split('\n')


valves = [[line.split()[1],ints(line)[0],line.split('to valve')[1].lstrip('s ').split(', ')] for line in lines]

#g[node] = list of adjacent nodes
g: dict[str,list[str]] = {v[0]:v[2] for v in valves}
#p[node] = pressure of node
p: dict[str,int] = {v[0]:v[1] for v in valves}
#we don't care about paths - just distances
# path: dict[str,dict[str,list[str]]] = {v[0]:{} for v in valves}

hallway = {k for k in g.keys() if p[k]==0 and len(g[k])==2}

#find relevant distances - shortest paths between all valve-having spots
d: dict[str,dict[str,int]] = {v:{} for v in sorted(g.keys()) if v not in hallway}
for source in sorted(g.keys()):
    if source in hallway:
        # zero pressure and only connects 2 nodes (hallway): ignore; don't compute distances from here
        continue
    #find dist to all other relevant positions  (BFS)
    q = [source]
    td = 0
    visited = set()
    while q:
        q2 = set()
        for dest in q:  # next dist out: set dist and add
            visited.add(dest)
            if dest not in hallway:
                d[source][dest] = td
            adj = set(g[dest]) # next to dest
            q2.update(adj)
        td += 1
        q = list(q2 - visited)
p = {k:v for k,v in p.items() if k not in hallway}

nodes = sorted(p.keys())#-{'AA'})
# print(nodes)
# print(p)
d2 = [[d[a][b] for b in nodes] for a in nodes]
nodeiset = set(range(1,len(nodes)))

# TODO: implement parsing in the zig file?
# ouput the distance array for zig
# for row in d2:
#     print(f"    &[16]Time{{ {', '.join(map(str,row))} }},")
# exit()

# def find_max_pres(nodes_unordered, curr, time):
#     # have just arrived at curr and opened valve, so will get time*flow from here
#     # determine the other valves we can open with enough time to have them matter
#     nexts = [(nextnd, time-d[curr][nextnd]-1)
#              for nextnd in nodes_unordered
#              if time-d[curr][nextnd]-1 > 0]
#     if nexts:
#         res = max(find_max_pres(nodes_unordered - frozenset({nextnd}), nextnd, nextT)
#                   for nextnd, nextT in nexts)
#         return res + time*p[curr]
#     else:
#         return time*p[curr]

# @functools.lru_cache(None)
def find_max_presI(nodesT, curr, time):
    # have just arrived at curr and opened valve, so will get time*flow from here
    # determine the other valves we can open with enough time to have them matter
    nexts = [(nextnd, time-d2[curr][nextnd]-1)
             for nextnd in nodesT
             if time-d2[curr][nextnd]-1 > 0]
    if nexts:
        res = max(find_max_presI(tuple(tn for tn in nodesT if tn!=nextnd), nextnd, nextTm)
                  for nextnd, nextTm in nexts)
        return res + time*p[nodes[curr]]
    else:
        return time*p[nodes[curr]]

#Part 1
print(find_max_presI(tuple(range(1,15)), 0, 30))
#
# part1_sol_a = ['KQ','RF','AZ','VI','IM','IY','AQ','HA']
# part1_sol_b = [nodes.index(tnode) for tnode in part1_sol_a]


max_flow_for_set_26 = {ti:{} for ti in [6,7,8,9]}
print("starting to run...")
for i1 in [6,9]:
    print(i1)
    for c in itertools.combinations(range(1,16), i1):  # nodes[1:] excludes 'AA'; sorted order
        # f = frozenset(c)
        # max_flow_for_set_26[i1][f] = find_max_pres(f,'AA',26)
        max_flow_for_set_26[i1][c] = find_max_presI(c,0,26)

print("Done...")
# nodeset = frozenset(nodes)-frozenset({'AA'})
mxflow = 0
mxSet = 0
# for fs,tflow in max_flow_for_set_26[8].items():
#     other = nodeset - fs
#     tflow += max_flow_for_set_26[7][other]
#     if tflow > mxflow:
#         mxflow = tflow
#         mxSet = fs
#         print(mxflow,sorted(mxSet),sorted(other))
# all_9_items = sorted(max_flow_for_set_26[9].items(), key=lambda t:t[1])
for fs,tflow in max_flow_for_set_26[9].items():
    other = tuple(i for i in range(1,16) if i not in fs)
    totflow = tflow + max_flow_for_set_26[6][other]
    if totflow > mxflow:
        mxflow = totflow
        mxSet = fs
        print(mxflow,mxSet,other)
print(mxflow) #Part 2

#testsol: DD, HH, EE
# and:    JJ, BB, CC

#Example:
# 0 at aa (start at min.0: 30 min left)
#   30 * 0
# 2 to kq (turn on min.3: 27 min left)
#   27 * kq (17)
# 3 to rf (turn on min.7)
#   23 * rf (18)
# 2 to az (turn on min.10)
#   20 * az (20)
# 2 to vi (turn on min.13)
#   17 * vi (22)   [still on shortest path to here from AA]


