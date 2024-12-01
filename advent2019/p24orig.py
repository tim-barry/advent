
from intcode import printgi
with open("input.txt") as f:
    r = f.read().strip()
t1 = """
....#
#..#.
#..##
..#..
#....
""".strip()

# r = t1

grid = [[c=='#' for c in l] for l in r.split('\n')]

def biodiversity(g):
    return sum( g[y][x] * 2**(x + 5*y)
               for y in range(5)
               for x in range(5))

def adj(g, y, x):
    return [g[(y+dy)%5][(x+dx)%5]
            for dx,dy in [
                [1, 0],
                [-1, 0],
                [0, 1],
                [0, -1],
            ]
            if 0<=y+dy<5 and 0<=x+dx<5
            ]

def adj2(g, y, x, lv):
    return [g[ny][nx]
            if not (ny==nx==2) else None
            for nx, ny in [
                [x+1, y+0],
                [x+-1,y+ 0],
                [x+0, y+1],
                [x+0, y+-1],
            ]
            if lv!=0 or (0 <= ny < 5 and 0 <=nx< 5)
            ]

g = {(x,y,0): grid[y][x] for x in range(5) for y in range(5)}

def expand(p, x, y, l):
    # yield x,y,l
    # go up a level:
    if p[0]<0:
        yield (1,2,l-1)
    elif p[0]>4:
        yield (3,2,l-1)
    elif p[1]<0:
        yield (2,1,l-1)
    elif p[1]>4:
        yield (2,3,l-1)
    elif p[0]==p[1]==2:  # go down a level (touching 5)
        if x==1:  # came from left
            assert x==1 and y==2
            yield from [(0,nx,l+1) for nx in range(5)]
        elif x==3: # right
            yield from [(4,nx,l+1) for nx in range(5)]
        elif y==1:
            yield from [(nx,0,l+1) for nx in range(5)]
        elif y==3:
            yield from [(nx,4,l+1) for nx in range(5)]
    else:  # same level
        yield (p[0],p[1],l)

part = 1
def expand2(p, x, y, l):
    # improved version can handle part 1/2
    if 0<=p[0]<5 and 0<=p[1]<5:  # same level or down (l+1)
        # go down a level if centre in part 2
        if part==2 and p[0]==p[1]==2:
            if x==1: yield from [(0,nx,l+1) for nx in range(5)]
            if x==3: yield from [(4,nx,l+1) for nx in range(5)]
            if y==1: yield from [(nx,0,l+1) for nx in range(5)]
            if y==3: yield from [(nx,4,l+1) for nx in range(5)]
        else:  # same level
            yield (p[0],p[1],l)
    elif part==2:  # go up a level if part 2
        yield (2+p[0]//5, 2+p[1]//5, l-1)
        # if p[0]<0:
        #     yield (1,2,l-1)
        # if p[0]>4:
        #     yield (3,2,l-1)
        # if p[1]<0:
        #     yield (2,1,l-1)
        # if p[1]>4:
        #     yield (2,3,l-1)


def adj3(g, p):
    x,y,l = p
    basic_adj = [
        (x+1,y+0),
        (x-1,y+0),
        (x+0,y+1),
        (x+0,y-1),
    ]
    actual_adj = [np
                  for bnp in basic_adj
                  for np in expand2(bnp, x,y,l)]
    return actual_adj

def adjc3(g, p):
    return sum(g.get(np, 0) for np in adj3(g, p))


# def nex(g):
#     ng = [row[:] for row in g]
#     for y, r in enumerate(g):
#         for x, c in enumerate(r):
#             a = adj(g, y, x)
#             if g[y][x]:
#                 if sum(a)!=1:  # die if not exactly 1
#                     ng[y][x] = 0
#             else:
#                 if sum(a) in [1,2]:
#                     ng[y][x] = 1
#     return ng

# g = grid
# while g not in seen:
#     print('\n'.join(''.join('.#'[c] for c in row) for row in g))
#     print()
#     seen.append(g)
#     g = nex(g)
# print(g in seen)
# print('\n'.join(''.join('.#'[c] for c in row) for row in g))
# print()

# print(biodiversity(g))

# def nex2(g, parentng=None):
#     if parentng is None:
#         ng = deepcopy(g)
#     else:
#         ng = parentng[2][2]
#     for y, r in enumerate(g):
#         for x, c in enumerate(r):
#             if x==y==2: # recurse
#                 if g[2][2]==0:
#                     ng[2][2]
#                 nex2(g[2][2], ng)
#             else:
#                 a = adj2(g, y, x, 1)
#                 if g[y][x]:
#                     if sum(a)!=1:  # die if not exactly 1
#                         ng[y][x] = 0
#                 else:
#                     if sum(a) in [1,2]:
#                         ng[y][x] = 1
#     return ng

def nex3(g):
    # positions we have to check:
    nps = {np for p in g for np in adj3(g, p)}
    return {p:1
            for p in nps
            for ac in [adjc3(g, p)]
            if (g.get(p,0) and ac==1) or (not g.get(p,0) and ac in [1,2])
            # put the if here to ignore non-bug spaces
            # gives 1-2 second speedup
            }


def printl(g):
    ls = sorted({l for x,y,l in g.keys()})
    for l in ls:
        lvl = [[g.get((x,y,l))
                for x in range(5)]
               for y in range(5)]
        if lvl==[[None]*5]*5:
            break
        print("Level %d:"%l)
        print("\n".join(''.join('?' if x==y==2 else '.#'[bool(c)]
                                for x,c in enumerate(row))
                        for y,row in enumerate(lvl)))

def biodiversity2(g):
    return sum(2**(x+5*y) for (x,y,l) in g)

def part1_better():
    global part
    part = 1
    seen = []
    lg = g
    while lg not in seen:
        seen.append(lg)
        lg = nex3(lg)
    print(biodiversity2(lg))

def part2_better(num_iters=200):
    global part
    part = 2
    lg = g
    for x in range(num_iters):
        lg = nex3(lg)
    print(len(lg))

part1_better()
part2_better()

# def count(g):
#     t = sum(sum(c for x, c in enumerate(row) if not (x==y==2))
#             for y, row in enumerate(g))
#     if g[2][2]:
#         t+= count(g[2][2])
#     return t
