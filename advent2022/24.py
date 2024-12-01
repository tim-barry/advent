
import heapq
from pprint import pprint

f = "input24.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

test = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".strip().split('\n')

grid = lines
H = len(grid)
W = len(grid[0])
from math import lcm
cycle_len = lcm(H-2, W-2)
# print(cycle_len)
blizz = [((x,y),c) for y,row in enumerate(grid) for x,c in enumerate(row) if c in "><v^"]
def moveb(b):
    (x,y),c = b
    if c=='<':
        return ((x-2)%(W-2)+1, y),c
    elif c=='>':
        return ((x)%(W-2)+1, y),c
    elif c=='v':
        return (x, y%(H-2)+1),c
    elif c=='^':
        return (x, (y-2)%(H-2)+1),c

def moveblizz(blizz):
    return [moveb(b) for b in blizz]


bblizz = []
for t in range(cycle_len):
    # pprint(blizz)
    bblizz.append({p for p,dir in blizz})
    blizz = moveblizz(blizz)

def moves(p):
    return [
        p,
        (p[0]+1, p[1]),
        (p[0]-1, p[1]),
        (p[0], p[1]+1),
        (p[0], p[1]-1),
    ]

start1 = (1,0)
goal1 = (W-2, H-1)

#each round: can move or wait
# act simultaneously with blizzards
# cannot share pos.

def heuristic1(postime): # want to minimize: time + distance to goal
    return postime[1] + ( (W-2)-postime[0][0] + (H-1)-postime[0][1] )
def heuristic2(postime): # want to minimize: time + distance to goal
    return postime[1] + postime[0][0] + postime[0][1]


# from pprint import pprint
# pprint([[heuristic(((x,y),0)) for x in range(len(row))] for y,row in enumerate(grid)])

#priority queue state: (heuristic, position, time)
#fewest minutes to reach goal
def part1(start,goal,startT, heuristic):
    qp = (start, startT)
    q = [(heuristic(qp),qp)]
    it = 0
    while q:
        h, (pos, time) = heapq.heappop(q)
        if pos == goal:
            return time
        next_blocked = bblizz[(time+1)%cycle_len]
        filtmoves = [np for np in moves(pos)
                     if np==start or np==goal or
                     (1<=np[0]<=W-2 and 1<=np[1]<=H-2)]
        for np in filtmoves:
            if np in next_blocked: continue
            nt = np,time+1
            res = (heuristic(nt),nt)
            if res not in q:
                heapq.heappush(q, (heuristic(nt),nt))
        it += 1
    print("unreachable")

p1 = part1(start1, goal1, 0, heuristic1)
p2a = part1(goal1, start1, p1, heuristic2)
p2b = part1(start1, goal1, p2a, heuristic1)
print(p1)
print(p2b)
