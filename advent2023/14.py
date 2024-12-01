import functools
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

f = "input14.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

# Lava!!!!

tlines = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".split()

def load(lines, sort=True):
    total = 0
    for col in lmap(''.join, zip(*lines)):
        x = 0
        L = len(col)
        for part in col.split('#'):
            if sort:
                for tk in range(x,x+part.count('O')):
                    total += L - tk
            else:
                for i in range(x,x+len(part)):
                    if part[i-x]=='O':
                        total += L-i
            x += len(part)+1
    return total

print(load(lines))

# print('.'<'O')

def cycle(lines: tuple[str]):
    lines = lmap(''.join, zip(*lines))
    lines = ['#'.join(''.join(sorted(part, reverse=True)) for part in row.split('#')) for row in lines]
    lines = lmap(''.join, zip(*lines))
    #west : move O left
    lines = ['#'.join(''.join(sorted(part, reverse=True)) for part in row.split('#')) for row in lines]

    lines = lmap(''.join, zip(*lines))
    lines = ['#'.join(''.join(sorted(part)) for part in row.split('#')) for row in lines]
    lines = lmap(''.join, zip(*lines))
    # move O right
    lines = ['#'.join(''.join(sorted(part)) for part in row.split('#')) for row in lines]
    return tuple(lines)

#part2:
M = 1_000_000_000

lines = tuple(lines) #hashable

seen = [lines]
# [0 cycles].  [0, 1 cycles]. [0,1,2 cycles]. then at 3 we see 1 again: the length is r=2 so we expect the last to be 2
for i in range(1,M):
    lines = cycle(lines)  # lines after i cycles
    if lines in seen:
        r = i - seen.index(lines)  #i = 3, seen.index = 1, r = 2
        break
    seen.append(lines)

# 1 + (M-3)%2 = 1+1 = 2: correct? yes, was overthinking
lines = seen[seen.index(lines) + (M-i)%r]

print(load(lines,sort=False))


