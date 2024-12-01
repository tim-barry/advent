
import string
from collections import deque,defaultdict,Counter
from functools import reduce
def lmap(f,l): return list(map(f,l))

f = "input4.txt"

with open(f) as r:
    s = r.read()
    lines = s.strip().split('\n')
    lgroups = s.strip().split('\n\n')

#print(lines[0].split(','))

ps = [lmap(int,a.split('-')+b.split('-')) for line in lines for [a,b] in [line.split(',')]]
#print(ps)

print(len([a for [a,b,c,d] in ps if a<=c<=d<=b or c<=a<=b<=d]))
print(len([a for [a,b,c,d] in ps if a<=c<=b or a<=d<=b or c<=a<=d or c<=b<=d]))


tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
def ints(s: str): return lmap(int, s.translate(tbl_digits).split())
ps = [ints(line) for line in lines]
#print(ps)
