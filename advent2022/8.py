
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('\d+',s))

f = "input8.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

# lines = """
# 30373
# 25512
# 65332
# 33549
# 35390""".strip().split()

#height
grid = [[int(c) for c in line] for line in lines]
print(grid)
#visLeft = [[max(grid[y][:x]+[-1])<grid[y][x] for x in range(len(grid[0]))]for y in range(len(grid))]
visible = [[max(grid[y][:x]+[-1])<grid[y][x] or max(grid[y][x+1:]+[-1])<grid[y][x]
           or max([grid[ty][x] for ty in range(y)], default=-1)<grid[y][x]
           or max([grid[ty][x] for ty in range(y+1,len(grid))], default=-1)<grid[y][x]
            for x in range(len(grid[0]))]
           for y in range(len(grid))]

#print(visible[1])
print(sum(sum(row) for row in visible))
#maxScoreL = [[0]*W for ti in range(H)]

tgrid : list[list] = lmap(list, zip(*grid))
maxScore=1
W=len(grid[0])
H=len(grid)
for y in range(H):
    for x in range(W):
        v=grid[y][x]
        dl = sum(all(tv<v for tv in grid[y][t:x]) for t in range(0,x)) +(v<=max(grid[y][:x], default=-1))
        dr = sum(all(tv<v for tv in grid[y][x+1:t]) for t in range(x+1,W))
        du = sum(all(tv<v for tv in tgrid[x][t:y]) for t in range(0,y)) +(v<=max(tgrid[x][:y], default=-1))
        dd = sum(all(tv<v for tv in tgrid[x][y+1:t]) for t in range(y+1,H))
        score = dl*dr*du*dd
        maxScore = max(maxScore,score)
print(maxScore)

# maxScoreL[y][x] = score, [dl,dr,du,dd]
