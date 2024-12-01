
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall(r'\d+',s))

f = "input.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

tlines = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip().split('\n')
is_adj = defaultdict(lambda:False, {(a,b): lines[b][a] not in string.digits+"."
          for b in range(len(lines)) for a in range(len(lines[0]))})

#for each digit, check if it is next to a symbol
for b in range(len(lines)):
    for a in range(len(lines[0])):
        if lines[b][a].isdigit() and any(is_adj[a+dx,b+dy] for dx in [-1,0,1] for dy in [-1,0,1]):
            is_adj[a,b] = True
#then floodfill horizontally between digits
same = False
while not same:
    same = True
    for b in range(len(lines)):
        for a in range(len(lines[0])):
            if is_adj[a,b]: continue
            #check adj
            if lines[b][a].isdigit() and any(is_adj[a+dx,b] for dx in [-1,0,1]):
                is_adj[a,b] = True
                same = False

grid = [list(line) for line in lines]
for b in range(len(lines)):
    for a in range(len(lines[0])):
        if not is_adj[a,b]: grid[b][a] = ' '
ngrid = [''.join(linel) for linel in grid]

print('\n'.join(ngrid))

part_numbers = sum(lmap(ints,ngrid),[])
print(sum(part_numbers))

def nums_at(a,b):
    # ugly cases
    r = []
    if is_adj[a-1,b] and lines[b][a-1].isdigit():
        r.append(ints(lines[b][a-3:a])[-1])
    if is_adj[a+1,b] and lines[b][a+1].isdigit():
        r.append(ints(lines[b][a+1:a+4])[0])
    for dy in [-1,1]:
        if lines[b+dy][a].isdigit(): # central
            if lines[b+dy][a+1].isdigit(): #right or centered
                r.append(ints(lines[b+dy][a-1:a+3])[0])
            else: # left
                r.append(ints(lines[b+dy][a-2:a+1])[-1])
        else:
            if lines[b+dy][a-1].isdigit():
                r.append(ints(lines[b+dy][a-3:a])[-1])
            if lines[b+dy][a+1].isdigit():
                r.append(ints(lines[b+dy][a + 1:a + 4])[0])
    if len(r)==2:
        return r[0]*r[1]
    else: return 0

gears = [res for b in range(len(lines)) for a in range(len(lines[0]))
         if lines[b][a]=='*' for res in [nums_at(a,b)] if res]
# print(gears)

print(sum(gears))
