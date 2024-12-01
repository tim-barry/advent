import string
from collections import deque,defaultdict,Counter
from functools import reduce

def lmap(f,l): return list(map(f,l))

f = "input3.txt"

with open(f) as r:
    s = r.read()
    lines = s.strip().split('\n')
    lgroups = s.strip().split('\n\n')



def f(l):
    m = len(l)//2
    x = l[:m]
    b = l[m:]
    return x,b

def pri(c):
    return ord(c.lower())-ord('a')+1 + 26*(c.isupper())

print(sum([pri(list(set(a)&set(b))[0]) for [a,b] in lmap(f,lines)]))


groups = [list(set(lines[x])&set(lines[x+1])&set(lines[x+2]))[0] for x in range(0,len(lines),3)]
print(sum(lmap(pri, groups)))

# try:
#     arr1 = lmap(int,lines)
# except:
#     pass
# try:
#     arr2 = lmap(int,lgroups)
# except:
#     pass
# try:
#     wordgrid = [line.strip().split() for line in lines]
#     cgrid = lmap(list, lines)
#     igrid = [lmap(int, words) for words in wordgrid]
# except:
#     pass


