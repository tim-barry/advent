
from collections import deque,defaultdict,Counter
def lmap(f,l): return list(map(f,l))

f = "input2.txt"

with open(f) as r:
    s = r.read()
    lines = s.strip().split('\n')
    lgroups = s.split('\n\n')

def score(t):
    a=ord(t[0])-ord('A')
    b=ord(t[1])-ord('X')
    return b+1 + 3*(a==b) + 6*((a+1)%3==b)

def score1(t):
    a=ord(t[0])-ord('A')
    b=ord(t[1])-ord('X')
    return (a+(b-1))%3+1 + 3*b

print(sum(score(list(line.strip().split())) for line in lines))
print(sum(score1(list(line.strip().split())) for line in lines))
