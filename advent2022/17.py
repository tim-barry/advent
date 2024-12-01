import functools
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input17.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

#tetris
rocks = [
    [(0,0),(1,0),(2,0),(3,0)], # ____
    [(1,0),(0,1),(2,1),(1,1),(1,2)], # +
    [(0,0),(1,0),(2,0),(2,1),(2,2)], # _|
    [(0,0),(0,1),(0,2),(0,3)], # ||||
    [(0,0),(0,1),(1,0),(1,1)], # []
]
rocks = [[complex(*t) for t in l] for l in rocks]
rockRight = [3,2,2,0,1]
#every 5: repeat

grid = defaultdict(int)
# 0: air
# 1: rock
for ti in range(7):
    grid[ti-1j] = 1

def move(grid,rockI,p,d):
    if d=='<':
        if p.real==0: return p,False
        if any(grid[p-1+r] for r in rocks[rockI]): return p,False
        return p-1, False
    if d=='>':
        if p.real+rockRight[rockI]==6: return p,False
        if any(grid[p+1+r] for r in rocks[rockI]): return p,False
        return p+1, False
    else: # down
        if any(grid[p+r-1j] for r in rocks[rockI]):
            maxH = 0
            for r in rocks[rockI]: #upd grid
                grid[p+r]=1
                maxH = max(maxH, (p+r).imag)
            return p,int(maxH+1)
        else: # can move down
            return p-1j, False

def printgrid(grid,top):
    print('\n'.join(''.join('.#'[grid[x+1j*y]] for x in range(7)) for y in range(top,top-10,-1)))


t = 0
# W = 7
jets = lines[0]
# jets = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
LJ = len(jets)
print(LJ)

lowestEmptyRow = 0
AppearPos = 2 + 1j*(3+lowestEmptyRow)

rock = 0
rp = AppearPos
heights = [0]
LL = len(jets)*5
lastT = 0
maxFallDist = 0
seen = defaultdict(int)
seen10 = 0
while 1:  # find a loop point where t==0 and rock==0 and will fall at 0
    rp, _ = move(grid, rock%5, rp, jets[t%LJ])
    rp, newH = move(grid, rock%5, rp, 'v')
    if newH != 0:
        if newH > lowestEmptyRow:
            lowestEmptyRow = newH
            AppearPos = 2 + 1j * (3 + lowestEmptyRow)
        heights.append(lowestEmptyRow)
        rock += 1
        rp = AppearPos
        fdist = t+1-lastT
        lastT=t
        # print('rock fell:',rock)
        # if fdist>maxFallDist:
        #     maxFallDist = fdist
        #     print(f"Max fall dist: rock {rock},fall dist {maxFallDist}")
        if rock%100==99:  # cleanup+save mem
            # print("rock:",rock)
            ngrid = defaultdict(int)
            ngrid.update({k:v for k,v in grid.items() if lowestEmptyRow-k.imag<100})  # only keep 100 (need at least 40)
            del grid
            grid = ngrid
        seen[rock%5,t%LJ]+=1
        if seen[rock%5, t%LJ]>100 and not seen10:
            print(100,rock,t)
            seen10=rock,t
        if seen[rock%5, t%LJ]>101:
            seen11 = rock,t
            print(101,rock,t)
            break

    t += 1


# print(lowestEmptyRow)

print(seen10,seen11)

#first attmpt: 1585472202931
#actual:       1585673352422
M = 1000000000000

#test: 1514285714288
loopStart = seen10[0]
loopEnd = seen11[0]
loopLen = loopEnd-loopStart
loopHeight = heights[loopEnd]-heights[loopStart]
looptimes = ((M-loopStart)//loopLen)
print(loopHeight*looptimes + heights[M-looptimes*loopLen] )

