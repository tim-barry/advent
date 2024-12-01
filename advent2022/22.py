
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input22.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

s = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
""".strip("\n")
# lgroups = s.split('\n\n')

board = lgroups[0].split('\n')
moves = lgroups[1]

from itertools import zip_longest
# dists = lmap(int,moves.replace("R","L").split("L"))
dists = ints(moves)
turns = [c for c in moves if c in "RL"]

# print(len(dists))
# print(len(turns))

def orend(p, mx):
    if p>=0: return p
    return mx
#always dist followed by turn
#with 1 final dist
firstcol = [row.rstrip().rfind(' ')+1 for row in board]
lastcol = [orend(row.find(' ',f)-1,len(row)-1) for row,f in zip(board,firstcol)]
zboard = [''.join(l) for l in zip_longest(*board, fillvalue='')]
firstrow = [col.rstrip().rfind(' ')+1 for col in zboard]
lastrow = [orend(col.find(' ',f)-1,len(col)-1) for col,f in zip(zboard,firstrow)]


#1j**0 = 1 (+x, right)
#1j**1 = 1j (+y, down)...
# facingL = [">", "v", "<", "^"]  #0,1,2,3

def pw(r,c,f):
    return 1000*r + 4*c + f
def pwp(p, f):
    return pw(int(p.imag)+1, int(p.real)+1, f)
def iswall(p):
    return board[int(p.imag)][int(p.real)] == "#"

def nextpos1(pos,f):
    pos += 1j**f
    if f==0 and pos.real > lastcol[int(pos.imag)]: # right edge
        return complex(firstcol[int(pos.imag)], pos.imag)
    elif f==2 and pos.real < firstcol[int(pos.imag)]: # left edge
        return complex(lastcol[int(pos.imag)], pos.imag)
    elif f==1 and pos.imag > lastrow[int(pos.real)]: # bottom edge
        return complex(pos.real, firstrow[int(pos.real)])
    elif f==3 and pos.imag < firstrow[int(pos.real)]: # top edge
        return complex(pos.real, lastrow[int(pos.real)])
    return pos

# START_LEFT = [50,50,0,0]
# END_RIGHT = [150, 100, 100, 50]
# START_TOP = [100,0,0]
# END_BOTTOM = [200,150,50]
def nextpos2(pos,f):
    pos += 1j**f
    if f==0 and pos.real > lastcol[int(pos.imag)]: # right edge
        if 0<=pos.imag<=49: # first: down to middle, facing left
            ny = 149-pos.imag
            nx = lastcol[int(ny)]
            return complex(nx,ny), 2  #face left
        elif 50<=pos.imag<=99:
            nx = 100 + (pos.imag - 50)
            ny = lastrow[int(nx)]
            return complex(nx,ny), 3 #face up
        elif 100<=pos.imag<=149:
            ny = 149-pos.imag
            nx = lastcol[int(ny)]
            return complex(nx,ny), 2  #face left
        else: # 150...
            nx = (pos.imag - 100)
            ny = lastrow[int(nx)]
            return complex(nx, ny), 3  # face up
    elif f==2 and pos.real < firstcol[int(pos.imag)]: # left edge
        if 0<=pos.imag<=49:
            #come in left side of middle-bottom
            nx = 0
            ny = 149 - pos.imag
            return complex(nx,ny), 0 #face right
        elif 50<=pos.imag<=99:
            #end up top of left face
            ny = 100
            nx = pos.imag - 50
            return complex(nx,ny), 1 #face down
        elif 100<=pos.imag<=149:
            #come in left side of top
            nx = 50
            ny = 49 - (pos.imag - 100)
            return complex(nx,ny), 0 #face right
        else: #100<=pos.imag<=149
            # go to top of main
            ny = 0
            nx = pos.imag - 100
            return complex(nx,ny), 1 #face down
    elif f==1 and pos.imag > lastrow[int(pos.real)]: # bottom edge/down
        if 0<=pos.real<=49:
            #go top of rightmost
            nx = pos.real + 100
            #ny = 0
            return nx, 1 # still facing down
        elif 50<=pos.real<=99:
            #go to right of lowest: imag 150+; change facing down -> left
            nx = 49
            ny = pos.real + 100
            return complex(nx,ny), 2
        else: #100<=pos.real<=149: go on right of mid
            ny = pos.real -50
            nx = 99
            return complex(nx,ny), 2 #face left
    elif f==3 and pos.imag < firstrow[int(pos.real)]: # top edge
        if 0<=pos.real<=49:
            #come in left of mid
            nx = 50
            ny = 50+pos.real
            return complex(nx,ny), 0 #facing right
        elif 50<=pos.real<=99:
            #come in left of bottom[left]
            nx = 0
            ny = 150+(pos.real-50)
            return complex(nx,ny), 0 #facing right
        else: #100<=pos.real<=149
            #come in bottom of bottom[left]
            ny = 199
            nx = pos.real-100
            return complex(nx,ny), 3 #still facing up
    return pos,f


# move: 1j**dir
def move(pos,f,d):
    for t in range(d):
        try:
            np, nf = nextpos2(pos,f)
            if iswall(np):
                return pos,f
            pos, f = np, nf
        except:
            print(pos,f)
            raise
    return pos, f

pos_x = board[0].index('.')
pos_y = 0
pos = pos_x
f = 0 # right
for i in range(len(turns)):
    d = dists[i]
    pos, f = move(pos,f,d)
    t = turns[i]
    if t=="R": f += 1
    else: f -= 1  # left
    f%=4
d = dists[-1]
pos, f = move(pos,f,d)
print(pwp(pos,f))



