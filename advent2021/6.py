
#2024-01-09

l = eval(open("input6.txt").read())
from collections import Counter

#l = (3,4,3,1,2)
c = Counter(l)

res = {}
tc = Counter({6:1})
for t in range(256):
    nc = Counter({k-1:v for k,v in tc.items()})
    nc[6] += nc[-1]
    nc[8] += nc[-1]
    del nc[-1]
    tc = nc
res[6] = sum(tc.values());
for t in range(1,6):
    nc = Counter({k-1:v for k,v in tc.items()})
    nc[6] += nc[-1]
    nc[8] += nc[-1]
    del nc[-1]
    tc = nc
    res[6-t] = sum(tc.values())
print(res)

r2 = sum(res[age]*count for age,count in c.items())
print(r2)
for t in range(80):
    nc = Counter({k-1:v for k,v in c.items()})
    nc[6] += nc[-1]
    nc[8] += nc[-1]
    del nc[-1]
    c = nc
print(sum(c.values()))

