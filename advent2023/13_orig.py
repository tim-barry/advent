
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

# i'm feeling a 2D grid problem coming...
#g = defaultdict(int, {x+y*1j: (c) for y,line in enumerate(lines) for x,c in enumerate(line)})

tlgroups = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".split('\n\n')

grids = [lines.split('\n') for lines in lgroups]

def summ(notes):
    return x+100*y
total = 0
for g in grids:
    for y in range(1,len(g)):
        if sum(c1!=c2 for a,b in zip(g[:y][::-1], g[y:]) for c1,c2 in zip(a,b))==1:
            total += y*100
            # print("horizontal reflection: ", y)
            break
    else:
        #horiz refl
        g = lmap(''.join, zip(*g))
        for x in range(1, len(g)):
            if sum(c1!=c2 for a,b in zip(g[:x][::-1], g[x:]) for c1,c2 in zip(a,b))==1:
                # print("vertical: ", x)
                total += x
                break

print(total)
