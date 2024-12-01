
import string
from collections import deque,defaultdict,Counter
from functools import reduce
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
tlines = """Time:      7  15   30
Distance:  9  40  200
""".split('\n')
def ways_to_beat(time, dist):
    ways = time+1  #hold for 0s to hold for all s
    t = 0
    while t <= (time+1)//2 and t*(time-t)<=dist:
        # print(t, t*(time-t))
        t += 1
    if t*(time-t)>=dist:
        return ways - 2*t
    return 0

def f(lines):
    times = ints(lines[0])
    dists = ints(lines[1])
    races = list(zip(times, dists))
    l = [ways_to_beat(t, d) for t, d in races]
#ways to beat record
    return reduce(lambda a,b: a*b, l)

print(f(lines))
print(f([''.join(line.split()) for line in lines]))
