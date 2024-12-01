import itertools
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

f = "input.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

tlines = """....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......""".split('\n')

# i'm feeling a 2D grid problem coming...
expanded_rows = []
expanded_cols = []
for col in range(len(lines[0])):
    if all(lines[i][col]=='.' for i in range(len(lines))):
        expanded_cols.append(col)
for row in range(len(lines)):
    if set(lines[row])=={'.'}:
        expanded_rows.append(row)
print(expanded_cols)
print(expanded_rows)
print('done expanding')
g = {(x,y) for y,line in enumerate(lines) for x,c in enumerate(line) if c=="#"}
print('found gals')
d = {}
M = 1_000_000
lg = sorted(g)
for i in range(len(lg)):
    a = lg[i]
    for j in range(i+1, len(lg)):
        b = lg[j]
        k = a,b
        # print(a,b)
        dxl = [M if x in expanded_cols else 1 for x in range(min(a[0],b[0]),max(a[0],b[0]))]
        dyl = [M if y in expanded_rows else 1 for y in range(min(a[1],b[1]),max(a[1],b[1]))]
        # print(dxl)
        # print(dyl)
        # input()
        d[k] = sum(dxl)+sum(dyl)

# print(len(d.values()))
print(sum(d.values()))

