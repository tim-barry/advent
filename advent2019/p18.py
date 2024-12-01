
import time
start = time.time()
def to_p(c): return [int(c.real), int(c.imag)]

with open('input18.txt', 'r') as f:
    r = f.read().strip()

t0 = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""".strip()

t1 = """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
""".strip()

t2 = """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
""".strip()

t3 = """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
""".strip()

# r = t2

def is_key(c): return c.upper()!=c
def is_door(c): return c.lower()!=c
keys = [c for c in r if is_key(c)] + ['@']

grid = [s for s in r.split('\n')]
gc = {complex(x,y):c for y, row in enumerate(grid) for x,c in enumerate(row)}
key_pos = {k:p for p,k in gc.items() if k in keys}

edg = {p:[np for np in (p+1j**d for d in range(4)) if gc[np]!='#'] for p in gc if gc[p]!='#'}
print("trimming dead ends...")
ends = {p for p,a in edg.items()
        if len(a)==1 and not is_key(gc[p]) and gc[p]!='@'}
tot_ends_removed = 0
# trim ends (except keys)
while ends:
    nends = set()
    for end in ends:
        tot_ends_removed+=1
        [nend] = edg.pop(end)
        edg[nend].remove(end)
        if len(edg[nend])==1 and not is_key(gc[nend]):
            nends.add(nend)
    ends = nends
print(f"Trimmed {tot_ends_removed} squares from dead ends")
tgc = {p:gc[p] if p in edg else '#' for p in gc}
print("Trimmed graph is:")
print("\n".join(''.join(tgc[x+1j*y] for x in range(len(grid[0])))
                for y in range(len(grid))))
print()
# compute path length between nodes (key/door/intersection)
# nodes = {p for p,a in edg.items() if gc[p].upper()!=gc[p].lower() or len(a)>=3}

# run BFS on graph to compute dist to adjacent nodes (key/door/intersection)
def node_bfs(node):  # return distance to all adj nodes
    visited = set()
    local_edg = {}  # (node, cost)
    q = {node}
    dist = 0
    while q:
        visited.update(q) # visit
        for p in q-{node}: # ignore node itself
            # a node is: intersection or key or door
            if len(edg[p])>=3 or gc[p].upper()!=gc[p].lower():
                local_edg[p] = dist
        q = {np for p in q-local_edg.keys() for np in edg[p]} - visited
        # except:
        #     lq = list(q)
        #     print(f"q is: {lq} => edg: {[edg.get(p) for p in lq]}")
        #     raise
        dist += 1
    return local_edg

print("Running node bfs...")
node_edg = {}
cur_nodes = {key_pos['@']}
vis_nodes = set()
while cur_nodes:
    nnodes = set()
    # bfs from each node to adjacent nodes. each segment covered twice.
    # node has at most 4 adjacent nodes (intersection is node).
    vis_nodes.update(cur_nodes)
    for n in cur_nodes:
        ne = node_bfs(n)
        node_edg[n] = ne
        nnodes.update(ne.keys())
        # print(f"from node {n}:{gc[n]} => {ne} : {''.join(gc[tp] for tp in ne)}")
    cur_nodes = nnodes - vis_nodes

# clean up centre of grid (remove middlepoints
stat = key_pos['@']
# print(node_edg[stat])
ostarts = [stat]
ostart_vis = {stat}
if stat==40+40j:
    corners = [stat + (1j+1)*1j**d for d in range(4)]
    mids = {stat + 1j**d for d in range(4)}
    for c1 in corners:
        for m in mids:
            if m in node_edg[c1]:
                del node_edg[c1][m]
        for c2 in corners:
            if c2!=c1:
                node_edg[c1][c2] = int(round(abs(c1-c2)**2))//2
    for m in mids:
        del node_edg[m]
    node_edg[stat] = {c1:2 for c1 in corners}
    # print(node_edg[corners[0]])
    # print(node_edg[stat])
    ostarts += corners
    ostart_vis |= mids

def build_corner_path(p, excl, T=None, path=None):
    if T is None: T = {}
    if path is None: path = [p]
    T[p] = path  # shortest path to p
    nps = {np for np in node_edg[p] if np not in excl}  # adjacent positions
    excl.update(nps)  # don't visit them again
    for np in nps:
        build_corner_path(np, excl, T, path + [np])
    return T
t_visited = ostart_vis.copy()
paths = {k: v for corner in ostarts[:]
              for k, v in build_corner_path(corner, t_visited).items()}
paths[key_pos['@']] = [key_pos['@']]

def path_between_keys(ka,kb):  # shortest path on weighted tree
    if ka==kb: return []
    pa, pb = paths[key_pos[ka]], paths[key_pos[kb]]
    while len(pa)>1 and len(pb)>1 and pa[1]==pb[1]:
        pa = pa[1:]
        pb = pb[1:]
    if pa[0]==pb[0]:
        pa = pa[1:]
    path_ka_kb = pa[::-1] + pb
    if key_pos['@'] in path_ka_kb[1:]:
        path_ka_kb.remove(key_pos['@'])
    return path_ka_kb

def key_pathlen(ka,kb):
    path = path_between_keys(ka,kb)
    d = sum(node_edg[p1][p2]
            for p1,p2 in zip(path, path[1:]))
    return d

# precompute key distances
kkdist = {}
for k1 in keys:
    for k2 in keys:
        if k1<k2:
            kkdist[k1,k2] = kkdist[k2,k1] = key_pathlen(k1,k2)
print("Precomputed path distances")

start_paths = {k: path_between_keys('@',k) for k in key_pos if k!='@'}
req_keys = {k: {d.lower()
                for d in (gc[p] for p in path[:-1])
                if d.upper()!=d.lower()}  # include doors and keys on the path
            for k, path in start_paths.items()}
# turned 23s part 2 into 0.1s part 2 by including keys on the path

from functools import reduce
necessary_keys = reduce(set.union, req_keys.values())
print("Necessary keys:", necessary_keys)
print(f"({len(necessary_keys)} of them)")
print("Last keys:", req_keys.keys() - necessary_keys)


nreq = {}
def add_nreq(k):
    if k not in nreq:
        nreq[k] = req_keys[k].copy()  # keys/doors on the path to this key
        for nk in nreq[k].copy():
            nreq[k] |= add_nreq(nk)  # add requirements of required keys
    return nreq[k]
for k in req_keys: add_nreq(k)
print("Deterimined full (cascaded) requirements")
# for k in nreq: print(f"{k} requires: {nreq[k]}")

def available_keys(have_keys):
    return {k for k, v in nreq.items()
            if have_keys>=v}

print(f"Preprocessing completed in {time.time() - start:.3f} seconds")
# run nearest-first exploration
from heapq import heappop, heappush
part1_start = time.time()
h = []
# state is distance-traveled, keys, position (last key)
state =  0, frozenset('@'), '@'
heappush(h, state)
def get_next_states(s):
    d, keys, pos = s
    next_keys = available_keys(keys) - keys  # must get new key
    for nk in next_keys:
        add_dist = kkdist[pos,nk]
        yield d+add_dist, keys|{nk}, nk

best = {}
while h:
    state = heappop(h)
    st = state[1:]
    if st in best:
        continue # not the best, skip
    best[st] = state[0]
    if state[1]>=key_pos.keys():
        print(f"part 1: {state[0]}")
        break
    for next_state in get_next_states(state):
        heappush(h, next_state)
print(f"Part 1 finished in {time.time() - part1_start:.3f} seconds")

print("running part 2...")
part2_start = time.time()
# part 2: 4 mazes
from cmath import phase
from math import floor, pi
# trim distances to start point
for kk in kkdist:
    if '@' in kk:
        kkdist[kk]-=2
# generate quadrant list
quadrant = {k: floor(2*phase(key_pos[k]-key_pos['@'])/pi)
            for k in key_pos if k!='@'}
key_by_quadrant = {q: {k for k, tq in quadrant.items() if tq==q}
                   for q in set(quadrant.values())}
state = 0, frozenset('@'), ('@',)*4
best = {}
def get_next_state2(s):
    d, keys, pos = s
    next_keys = available_keys(keys) - keys  # must get new key
    for nk in next_keys:
        k_quad = quadrant[nk]
        # move robot in this quadrant
        new_pos = list(pos)
        add_dist = kkdist[pos[k_quad],nk]
        new_pos[k_quad] = nk
        yield d+add_dist, keys|{nk}, tuple(new_pos)

# def uniform_cost_search(start_state, goal_test, get_next_states):
h = []
heappush(h, state)
assert h==[state]
while h:
    state = heappop(h)
    st = state[1:]
    if st in best:
        continue # not the best
    best[st] = state[0]
    if state[1]>=key_pos.keys():
        print(f"part 2: {state[0]}")
        break
    for next_state in get_next_state2(state):
        heappush(h, next_state)

# uniform_cost_search(state, is_goal, get_next_state2)

print(f"Part 2 finished in {time.time() - part2_start:.3f} seconds")
exit()


build_tree = False
if build_tree:
    # run bfs outward again on nodes
    # start at corners of central square
    starts = ostarts[:]
    visited = ostart_vis.copy()|set(starts)

    def rec_build_tree(p, excl, T=None, dhere=None):
        if T is None: T = {}
        nps = sorted({np for np in node_edg[p] if np not in excl}, key=lambda np:-ord(gc[np]))
        excl.update(nps)
        if dhere is None: dhere = 2
        T[(gc[p], dhere)] = {(gc[np], node_edg[p][np]):None for np in nps}
        for np in nps:
            rec_build_tree(np, excl, T[(gc[p], dhere)], node_edg[p][np])
        return T
    trees = [rec_build_tree(p, visited) for p in starts]
    # from pprint import pprint
    # pprint(trees, indent=2, compact=False)

# correct! but takes several seconds.
# completed evening of 23rd (3am 24th)



# p needs pLGSAMxBHRy
# nothing needs P or X -> can do last
# g needs gl.amFu.wJkn..
#           s    b    .@
#
#                c
# f needs fUDQ.YV.....@
#             h  I o
#                t
#
#            .@
# r needs rE...
#           O
#         ._.Nj
# manual attempt:
# path (5268 = too high):
# nk / oc / KCe / Er OiqdNj * / It / Jwbu / zvTy / VYhQDUf * / Fmalgs * / RHBxMASLGp *
manual = False
if manual:
    tot = 0
    tot+=2
    tot += 2*(26+18)  # nk  SE
    tot+=2
    tot += 2*(12+36+2+86+38)  # oc  SW
    tot+=4
    tot += 2*(46+15+28+29)  # KCe  NE
    tot+=2
    tot += 2*(4+125+79+13+7+108+22+90+18+19+25)  # Er OiqdNj *   NW
    tot+=2
    tot += 2*(12+36+86+33+1)  # It  SW
    tot+=2
    tot += 2*(26+18+33+181+14+22+62)  # Jwbu  SE
    tot+=2
    tot += 2*(46+56+38+41+5)   # zvTy  NE
    tot+=4
    tot += 2*(12+36+86+15+52+31+1+14+92+13+50)  # VYhQDUf **  SW
    tot+=2
    tot += 2*(26+18+33+181+14+62+21+7+24+10+20+18+4)  # Fmalgs ***  SE
    tot+=2
    tot += (46+56+38+41+5+33+66+20+7+67+14+16+22+12+9) # RHBxMASLGp ****  NE
    print(tot)

# def doors_on_path(path):
#     return [d for d in (gc[p] for p in path) if d.lower()!=d]

# # collect all keys
# # assume only one path
# def bfs(gc, key):
#     print("running BFS from key", key)
#     start = key_pos[key]
#     path = {start:[]}
#     shortpath={}
#     # position sequence.
#     visited = set()
#     while path.keys() - visited:  # BFS to fill in path from @
#         for p in path.keys() - visited:
#             visited.add(p)
#             for dd in range(4):
#                 d = (1j**dd)
#                 if p+d in path:
#                     continue
#                 c = gc[p+d]
#                 if c!='#':
#                     # add to path
#                     path[p+d] = path[p]+[p+d]
#                     if c in keys:
#                         shortpath[key,c] = path[p+d]
#     return shortpath  # path to all keys
#
# # nsp = {k:[len(shortpath[k]),] for k in shortpath}
# # for k1,p1 in shortpath:
# #     for k2,p2 in shortpath:
# #         c1 = k1[1]
# #         c2 = k2[1]
# #         if c1<c2:  # path between keys
# #             # path c1-c2 is path c1-common@-c2
# #             p1 = p1[:]
# #             p2 = p2[:]
# #             while p1[1]==p2[1]:
# #                 p1.pop(0)
# #                 p2.pop(0)
# #             nsp[c1,c2] = p1[::-1] + p2[1:]
# #             nsp[c2,c1] = nsp[c1,c2][::-1]
#
# # keys needed to travel between points
# all_shortpath = {kk:pp for k in keys for kk,pp in bfs(gc, k).items()}
# print("Finished searching, generating edges...")
# edges = {kk: (frozenset(d.lower() for d in doors_on_path(pp)), len(pp))
#                for kk,pp in all_shortpath.items()}
# rk = {k: edges['@',k][0] for k in keys if k!='@'}
# for k in rk:
#     old_rkk = set()
#     while rk[k]!=old_rkk:
#         old_rkk = rk[k].copy()
#         for req in old_rkk:  #requirements
#             rk[k]|=rk[req]
# # rk -- requirements to get to k
# edgel = {k:[] for k in set(keys)|{'@'}}
# for (k1,k2),(need,cost) in edges.items():
#     edgel[k1].append([k2, cost])
#
# # do extension on need_keys from @ (assume one path)
# # eg, if y needs t, t needs i, i needs o
# # then then we order...?
#
# print("rk:")
# for t in rk.items():
#     print(t)
#
# # need keys, path length
# print("running search...")
# start_keypath = '@'
# states = {start_keypath: 0}  # keypath: cost
# # guaranteed can always reach a key
# # import heapq
# # edges = heapq.heapify([(cost, k2) for k2,cost in edgel['@'] if set('@')>=rk[k2]])
# while not any(set(kpath)>=set(keys) for kpath in states):
#     heuristic, cost, next_keypath = min(
#         (cur_cost+cost-190*len(kpath), cur_cost+cost, kpath+k2)
#         for kpath, cur_cost in states.items()
#         for k2, cost in edgel[kpath[-1]]
#         if k2 not in kpath
#         and set(kpath)>=rk[k2]
#         and not any(set(skp[:-1])==set(kpath) for skp in states if skp[-1]==k2)
#     )
#     print("keypath is", next_keypath, "cost", cost)
#     # assert next_keypath not in states
#     states[next_keypath] = cost
#
# last_kpath = [kpath for kpath in states if set(kpath)>=set(keys)][0]
# print(states[last_kpath])

