
import string
from collections import deque,defaultdict,Counter
from functools import reduce
from itertools import batched, starmap, accumulate, pairwise
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall(r'-?\d+',s))

f = "input21.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

# i'm feeling a 2D grid problem coming...
g = defaultdict(int, {x+y*1j: (c) for y,line in enumerate(lines) for x,c in enumerate(line)})

# print(max(g.keys(),key=lambda i:i.real+i.imag))

# nice big diagonal empty lanes
# and horiz+vertical paths along the edges and center

W = len(lines[0])
H = len(lines)
# takes W+H steps to completely fill [the outside of] a tile

s = [k for k in g.keys() if g[k]=='S'][0]
s_parity = int(s.real+s.imag)%2
# diff_parity = sum(1 for k in g.keys() if int(k.real+k.imag)%2!=s_parity and g[k]=='.')
# print(diff_parity)  # note there are some unreachable ones
# enclosed = sum(1 for k in g.keys()
#                if int(k.real+k.imag)%2!=s_parity
#                and g[k]!='#'
#                and not 3<=sum(g[k+1j**d]=='#' for d in range(4)
#                        if k+1j**d in g))
# print(enclosed)

steps_to_top = int(s.imag)
steps_to_left = int(s.real)
print(W,H,steps_to_left, steps_to_top)

# too many to iterate over, O(steps^2)
M = 26501365   # Parity: Odd

#try bruteforce - fails terribly (not even memory issue)
# prev = set()
# q = {s}
# total = 0
# for t in range(M):
#     if t%100==0:
#         print(t,len(q))
#     nq = set()
#     for p in q:
#         for d in range(4):
#             np = p + 1j ** d
#             np2 = complex(int(np.real)%131, int(np.imag)%131)
#             if g[np2] != '#' and np not in prev:
#                 nq.add(np)
#     prev = q
#     q = nq
#     if t%2==0: # odd number of steps from origin
#         total += len(nq)
# print(total)
# exit()

tiles = M//131   # when you see 2023_00, you know you're right
extra = M%131
print(tiles, extra)   # can get exactly to a boundary

# No blockers on the boundary either

def reachable(start, steps): #ignoring wraparound
    q = {start}
    for t in range(steps):
        nq = set()
        for p in q:
            for d in range(4):
                np = p + 1j ** d
                if np in g and g[np] != '#':
                    nq.add(np)
        q = nq
    return len(q)

# s65 = reachable(s, 65)
# print(s65) #part1 - actually s64
s131 = reachable(s, 131)
print(s131)

corners = [0, 0+130j,130,130+130j]
small = [reachable(p,64) for p in corners]   # side small: 64 steps (used 66 of 130 already)
print(small)
large = [reachable(p,64+131) for p in corners]  # side large: start from corner having traveled 66 steps from centre-bottom
print(large)
sides = [65, 65j, 65+130j, 130+65j]    #s-65,s-65j,s+65,s+65j
vs3 = [reachable(p,130) for p in sides]   # corners: from center, enough steps to reach opposite side exactly
print(vs3)
# Guaranteed a shortest path to a tile (center edge)
# is along an unbroken straight/manhattan line that crosses tiles in 131 squares

#full_cells = 2
r"""
# tiles = 2: can walk 2 full tiles + one half
    /\
   /\/ \
  /\/\/\
 /\/\/\/ \
/\/\/\/\/\    side len = 2x small, 1x large ; 4+1 full; 1 corners
\/\/\/\/\/
 \/\/\/\/
  \/\/\/
   \/\/
    \/

       /\
    /  EE  \
    /\F7 E\
   /\/LJ EE  \
  /\F7EEF7 F\
 /\/LJEELJ LJ  \
/\F7F7##F7F7 F\    tiles=3: side len = 3x small, 2x large ; 9+4 full;  1x each corner
\/LJLJ##LJLJ L/
 \/\/\/\/\/\/
  \/\/\/\/\/
   \/\/\/\/
    \/\/\/
     \/\/
      \/
tiles = 4: side len = 

  /\
 /\/\
/\/\/\     1x small, 0x large;   1 full
\/\/\/
 \/\/
  \/ 
/\ * 4(1) +1  Single  + 4*outside-corners combined
\/
#1, 5, 5+6+2=13, 7+5+5+3+3+1+1 = 27 (+5+7), +7+9 = +16 = 43,
#n^2 + (n-1)^2
Or:  Full*1,  + 1*Single (corners) + 1*outside corners
 Full*5 + (single+3corners)*[8 = perimeter = 2*full_cells]
"""
f = tiles
#AUGH tiles are of different parity. duh.
#tiles is even (2023_00); so central tile (definitely has the original odd parity) is in the smaller group
s131even = reachable(s, 132)
print(s131even,s131)
print(sum(small),sum(large),sum(vs3))
print(s131even*(f*f) + s131*(f-1)*(f-1) + sum(small)*f + sum(large)*(f-1) + sum(vs3))

#bad: 613718735941799
#bad: 613718715307199
#bad: 617565654534893
#correct: 617565692567199
