
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall(r'-?\d+',s))

f = "input02.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

games = list(enumerate([[Counter({color:int(count)
                                  for cube in pull.strip().split(', ')
                                    for count, color in [cube.split()]})
                         for pull in line.split(":")[1].split(';')]
                        for line in lines]))

goal = Counter({"red": 12, "green": 13, "blue": 14})
def possible(game):
    return all(pull <= goal for pull in game)

def min_bag(pulls):
    return reduce(Counter.__or__, pulls)

def power(bag):
    return bag['red'] * bag['blue'] * bag['green']

print(sum(t[0] + 1 for t in games if possible(t[1])))
print(sum(power(min_bag(t[1])) for t in games))

#alt:
bags = [(int(gid.split()[1]),
         Counter({color:count
                  for count,color in sorted((int(count),color)
                                            for cube in game.replace(';',',').split(', ')
                                            for count,color in [cube.strip().split()])}))
        for line in lines for gid,game in [line.split(": ")]]
print(sum(b[0] for b in bags if b[1]<=goal))
print(sum(power(b[1]) for b in bags))

