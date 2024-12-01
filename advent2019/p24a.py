with open("input24.txt") as f:
    r = f.read().strip()
t1 = """
....#
#..#.
#..##
..#..
#....
""".strip()

# r = t1
print(r)

# Can't do part 3 with current implementation
# O(n) in number of levels to calculate next state
# --> O(n^2) in total number of minutes
# even O(n) likely too long for 525948766245 (500 billion)

grid = [[c=='#' for c in l] for l in r.split('\n')]

gs = {(x,y,0) for x in range(5) for y in range(5) if grid[y][x]}

def biodiversity(g):
    return sum(1<<(x+5*y) for x,y,l in g)

part = 1
def expand(p, x, y, l):
    if 0<=p[0]<5 and 0<=p[1]<5:  # same level or down (l+1)
        # go down a level if centre in part 2
        if part==2 and p[0]==p[1]==2:
            if x==1: yield from [(0,nx,l+1) for nx in range(5)]
            if x==3: yield from [(4,nx,l+1) for nx in range(5)]
            if y==1: yield from [(nx,0,l+1) for nx in range(5)]
            if y==3: yield from [(nx,4,l+1) for nx in range(5)]
        else:  # same level
            yield p[0],p[1],l
    elif part==2:  # go up a level if part 2
        yield 2+p[0]//5, 2+p[1]//5, l-1

def adj3(p):
    x,y,l = p
    basic_adj = [
        (x+1,y+0),
        (x-1,y+0),
        (x+0,y+1),
        (x+0,y-1),
    ]
    actual_adj = [np
                  for bnp in basic_adj
                  for np in expand(bnp, x,y,l)]
    return actual_adj

def adjc3(g, p):  #number of neighbours
    return len(set(adj3(p)) & g)

def nex3(g):
    # positions we have to check: those next to at least one bug
    nps = {np for p in g for np in adj3(p)}
    return {p for p in nps for ac in [adjc3(g, p)]
            if (ac==1 if p in g else ac in [1,2])}

def printl(g):
    ls = sorted({l for x,y,l in g})
    for l in ls:
        print(f"Level {l}:")
        print("\n".join(''.join(['.#','?#'][x==y==2][(x,y,l) in g]
                                for x in range(5))
                        for y in range(5)))


def part1_better():
    global part
    part = 1
    seen = []
    lg = gs
    while lg not in seen:
        seen.append(lg)
        lg = nex3(lg)
    print("Part 1: biodiversity is",biodiversity(lg))

def part2_better(num_iters=200):
    global part
    part = 2
    lg = gs
    for x in range(num_iters):
        lg = nex3(lg)
    print("Part 2: number of bugs is", len(lg))

part1_better()
part2_better()

