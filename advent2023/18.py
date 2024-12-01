
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

f = "input18.txt"

# LAVA!!!!! >:D

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

# i'm feeling a 2D grid problem coming...
#g = defaultdict(int, {x+y*1j: (c) for y,line in enumerate(lines) for x,c in enumerate(line)})


seq = [("RDLU".find(d), int(n)) for line in lines for d,n,c in [line.split()]]
seq2 = [(int(c[-2]), int(c[2:-2],16)) for line in lines for d,n,c in [line.split()]]

horiz_lines = []
vertical_lines = []
corners = {0}
# what's the correct data structure for this again....

# print(seq)
p = 0
for d,n in seq2:
    np = p + n * 1j**d
    if d in [1,3]:
        vertical_lines.append((p,np))
    else:
        horiz_lines.append((int(p.imag),n,d))
    corners.add(p)
    p = np

bottom_line_dir = max(horiz_lines)[2]
bottom_line_lens = [line[1] for line in horiz_lines if line[2]==bottom_line_dir]

xs = sorted([int(p.real) for p in corners])
ys = sorted([int(p.imag) for p in corners])
vertical_lines = sorted(vertical_lines, key=lambda pair:pair[0].real)  # sorted by x-coord

#O(n^2) (vertical lines * horizontal lines) should be fast enough
total = 0
for ylo,yhi in zip(ys,ys[1:]):  # coords are inclusive
    ydiff = yhi-ylo  # don't include bottom trench - will be included in next iteration (except last) (except bottom)
    # scan across all vertical lines;
    left_edge = None
    for vl in vertical_lines:
        yps = int(vl[0].imag), int(vl[1].imag)
        if not (min(yps)>=yhi or max(yps)<=ylo):  # crosses this region, not just on the edge
            if left_edge is None:
                left_edge = int(vl[0].real)
            else:
                xdiff = int(vl[0].real) - left_edge +1  #include right trench
                total += ydiff * xdiff
                left_edge = None
    #left_edge is None

print(total + sum(bottom_line_lens) + 1)

