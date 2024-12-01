
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

games = list(enumerate([line.split(":")[1].split(';') for line in lines]))

goal = Counter({"red": 12, "green": 13, "blue": 14})
def possible(pulls):
    for pull in pulls:
        cubes = pull.strip().split(', ')
        c2 = Counter({color:int(count) for c in cubes for count, color in [c.split()]})
        if not all(c2[k]<=goal[k] for k in c2.keys()):
            return False
    return True

def min_bag(pulls):
    r = Counter({"red": 0, "green": 0, "blue": 0})
    for pull in pulls:
        cubes = pull.strip().split(', ')
        c2 = Counter({color:int(count) for c in cubes for count, color in [c.split()]})
        for k in c2.keys():
            r[k] = max(r[k], c2[k])
    return r

def power(bag):
    return bag['red'] * bag['blue'] * bag['green']

print(sum(t[0] + 1 for t in games if possible(t[1])))

print(sum(power(min_bag(t[1])) for t in games))


