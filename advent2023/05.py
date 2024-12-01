
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall(r'-?\d+',s))

f = "input05.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

tlgroups = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".split("\n\n")

seeds = ints(lgroups[0])
ns = seeds[:]
d = lmap(ints, lgroups)
print(ns)
for l in d[1:]:
    tl = list(zip(l[::3], l[1::3], l[2::3]))
    # print(tl)
    ns = [tt[0] if tt else x
          for x in ns
          for tt in [[x-b+a for a,b,c in tl if b<=x<b+c]]
          ]
    # print(ns)
print(min(ns))

rs = [(t[0], t[0]+t[1]) for t in zip(seeds[::2], seeds[1::2])] # start,end
print(rs)
for l in d[1:]:
    tl = list(zip(l[::3], l[1::3], l[2::3]))
    moved = []
    # print("using map: ", tl)
    # print("rs:", rs)
    for dst, start, ln in tl:
        # print("using map part:", (start,start + ln) , "->",dst)
        unmoved = []
        for rg in rs:
            if start<rg[1] and rg[0] < start+ln: # they intersect (y)
                #intersection is the smallest overlap
                new_r = (max(start, rg[0]), min(start+ln, rg[1]))
                if rg[0] < new_r[0]: # part of range was not moved
                    # print("adding left side")
                    unmoved.append((rg[0], new_r[0]))  # left split of seed range: stays same
                if new_r[1] < rg[1]: # "
                    # print("adding right side")
                    unmoved.append((new_r[1], rg[1]))  # right "
                moved.append((new_r[0] - start + dst, new_r[1] - start + dst))  # matching range
            else:  # no intersection; unchanged
                # print("no intersection")
                unmoved.append(rg)
        # print("unmoved:", rs)
        # print("moved:", moved)
        rs = unmoved  # don't move twice
    # print("moved ranges:", moved)
    # print("unmoved range:", rs)
    rs = (rs + moved)
    # print(len(rs))
print(min(rs)[0])