
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('\d+',s))

f = "input14.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')


ps = [[complex(*eval(pair.strip())) for pair in line.split('->')] for line in lines]

air = 0
rock = 1
sand = 2
grid = defaultdict(int)  #default air
for wall in ps:
    p1 = wall[0]
    for np in wall[1:]:
        dist = int(abs(np-p1))
        dir = (np-p1)/dist
        for i in range(dist+1):
            grid[p1+i*dir] = rock
        p1 = np

gridX = [int(k.real) for k in grid.keys()]
gridLeft = min(gridX)
gridRight = max(gridX)
gridY = [int(k.imag) for k in grid.keys()]
gridTop = 0
gridBottom = max(gridY)
def pgrid(grid):
    gridX = [int(k.real) for k in grid.keys()]
    gridLeft = min(gridX)
    gridRight = max(gridX)
    gridY = [int(k.imag) for k in grid.keys()]
    gridTop = 0
    gridBottom = max(gridY)
    grid2 = [['.+o'[grid[x+1j*y]] for x in range(gridLeft,gridRight+1)] for y in range(gridTop,gridBottom+1)]
    grid3 = '\n'.join(''.join(row) for row in grid2)
    print(grid3)

lowestWall = gridBottom
floor = 2+lowestWall
for tx in range(-10,1010):
    grid[tx+1j*floor] = rock

sandstart = 500+0j
def sandmove(pos,grid):
    if grid[pos+1j]==air:return pos+1j
    elif grid[pos-1+1j]==air:return pos-1+1j
    elif grid[pos+1+1j]==air: return pos+1+1j
    else:return pos

sandfallen = 0
while grid[sandstart]==air:
    p = sandstart
    pp = sandstart-1j
    while p!=pp:
        pp = p
        p = sandmove(p,grid)
    grid[p] = sand
    sandfallen += 1

pgrid(grid)
print(sandfallen)


