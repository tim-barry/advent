
from intcode import Intcode, asyncio, printgc, defaultdict

with open('input.txt', 'r') as f:
    r = f.read().strip()
    cc = [int(s) for s in r.split(',')]

dirs = [1j, -1j, -1, 1]

def mdc(a,b): return int(abs(a.real-b.real)+abs(a.imag-b.imag))
def printgcregion(g, c, dist=1):
    printgc(defaultdict(int,{p:g[p] for p in g if mdc(p,c)<=dist}))

def shortpath(g, a, b):  # bfs
    path = {a:[]}
    edge = {a}
    while b not in path and edge:
        new_edge = set()
        for p in edge:
            for d in dirs:
                if p+d not in path and g[p+d]==2:  # open
                    path[p+d] = path[p]+[d]
                    new_edge.add(p+d)
        edge = new_edge
        # print(f"pathd is: {path}")
    return path[b]


async def part1(code):
    g = defaultdict(int)  # unknown, wall, open
    g[0] = 2
    p = 0+0j
    d = 1j
    dist = defaultdict(lambda:1e999, {p:0})
    edge = set()
    new_edge = set()
    def in_f():
        while 1:
            # N,S,W,E = 1,2,3,4
            # print(f"pos: {p}  moving: {d}  cur_explore: {cur_explore} path: {path}  edge: {edge} new_edge:{new_edge}")
            # c = g[p]
            # g[p] = 4
            # printgc(g)
            # g[p] = c
            # input()
            yield dirs.index(d)+1
    comp = Intcode(code, input_src=in_f())
    new_pos = True
    cur_explore = p
    path = []
    path_i = 0
    async for status, in comp.async_output(1):
        # update according to status
        first_time_here = 0
        if status == 0:  # hit wall
            g[p+d] = 1
        elif status == 1:
            p += d
            if g[p]==0:
                first_time_here = 1
                g[p] = 2  # mark open
            dist[p] = min(dist[p], dist[p-d] + 1)
        elif status == 2:
            # oxy = p+d
            print(dist[p]+1)  # OUTPUT
            break
        #
        if path:  # following a path
            if path_i==len(path):  # reached end
                path = []
                path_i = 0
            else:  # continue on path
                d = path[path_i]
                path_i += 1
                continue
        # are we exploring?
        # p is old pos before move
        if p-d==cur_explore:  # came from exploration point
            if first_time_here:
                print("")
                new_edge.add(p)  # add to new edge
                d = -d  # go back
            else:
                print("err: came from explore point, but not first time here")
        elif p==cur_explore:  # moved to known spot
            unknown_left = sum(g[p+d]==0 for d in dirs)
            if unknown_left == 0:  # done exploring
                print(f"done exploring from {p}")
                if not edge:
                    # print(f"cleared edge")
                    edge = new_edge
                    new_edge = set()
                cur_explore = edge.pop()
                # set a course to next position with unknown neighbours
                # print(f"generating path from {p} to {cur_explore}...")
                path = shortpath(g, p, cur_explore)
                d = path[0]
                path_i = 1
                print(f"set path from {p} to {cur_explore}: {path}, d={d}")
            else:  # next to explore
                for d in dirs:
                    if g[p+d]==0:  # unknown
                        break
                # print(f"Continue exploring from {p} in direction {d}")



async def part2(code):
    g = defaultdict(int)  # unknown, wall, open
    g[0] = 2
    p = 0+0j
    d = 1j
    dist = defaultdict(lambda:1e999, {p:0})
    edge = set()
    def in_f():
        while 1:
            yield dirs.index(d)+1
    comp = Intcode(code, input_src=in_f())
    cur_explore = p
    path = []
    path_i = 0
    oxy = None
    async for status, in comp.async_output(1):
        # update according to status
        first_time_here = 0
        if status == 0:  # hit wall
            g[p+d] = 1
        elif status:
            p += d
            if g[p]==0:
                first_time_here = 1
                g[p] = 2  # mark open
            dist[p] = min(dist[p], dist[p-d] + 1)
            if status==2:
                oxy = p
        # Are we moving to the next explore point?
        if path:  # following a path
            if path_i==len(path):  # reached end
                path = []
                path_i = 0
            else:  # continue on path
                d = path[path_i]
                path_i += 1
                continue
        # Are we exploring?
        if p-d==cur_explore:  # came from exploration point
            if first_time_here:
                edge.add(p)  # add to edge
                d = -d  # go back to exploration point
            else:
                print("err: came from explore point, but not first time here")
        elif p==cur_explore:  # At exploration point -- time to explore
            unknown_left = sum(g[p+d]==0 for d in dirs)
            if unknown_left == 0:  # done exploring
                if not edge:
                    comp.halt()
                    continue  # explored all points -- exit main loop
                cur_explore = edge.pop()
                # set a course to next position with unknown neighbours
                path = shortpath(g, p, cur_explore)
                d = path[0]
                path_i = 1
            else:  # next to explore
                for d in dirs:
                    if g[p+d]==0:  # adjacent position in this direction is unknown
                        break  # explore this way
    print(len(shortpath(g, 0+0j, oxy)))  # part 1
    print(max(len(shortpath(g, p, oxy)) for p in g if g[p]==2))  # part 2

asyncio.run(part2(cc))

