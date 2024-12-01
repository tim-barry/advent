
import re
def lmap(f,l): return list(map(f,l))
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input15.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')


sens = [ints(line) for line in lines]
ss = [complex(*a[:2]) for a in sens]
beacons = [complex(*a[2:]) for a in sens]

def MD(a,b):
    d = a-b
    return int(abs(d.real)+abs(d.imag))

MAX = 2_000_000
ds = [MD(s,b) for s,b in zip(ss,beacons)]
d_2M = [int(abs(s.imag - MAX)) for s in ss]

def rg(s,d:int,d2m:int):
    if d2m > d:
        return []
    if d2m==d:
        return [s.real,s.real]
    f = d-d2m
    return [s.real-f, s.real+f]

def count(rgs):
    curr = rgs[0]
    tot = 0
    for i in range(1,len(rgs)):
        c2 = rgs[i]
        if c2[0]<= curr[1]+1:  # overlap
            curr[1] = max(curr[1],c2[1])
        else: # no overlap
            tot+=curr[1]-curr[0]+1
            curr = c2
    tot += curr[1]-curr[0]+1
    return tot

rgs = [rg(s,d,d2m) for s,d,d2m in zip(ss, ds, d_2M)]

tot = count(sorted([x for x in rgs if len(x)==2]))
#ignore beacons in the line
bc = [b for b in set(beacons) if b.imag==MAX]
#Part 1
print(int(tot-len(bc)))

#Part 2 - copy+paste formulae into Desmos
print("\n\nTable 1:  (x1, y1)")
for line in sens:
    print('\t'.join(map(str,line[:2])))
print("\n\nTable 2:  (x2, y2)")
for line in sens:
    print('\t'.join(map(str,line[2:])))

print('\n\nSensor-beacon Distance: ')
print(r'd=\left|x_{1}-x_{2}\right|+\left|y_{1}-y_{2}\right|')

diamond_equation = r"d\left[i\right]>\left(\left|x-x_{1}\left[i\right]\right|+\left|y-y_{1}\left[i\right]\right|-0.5\right)"
print("\n\nDiamonds:")
for i in range(1,len(sens)+1):
    print(diamond_equation.replace(r"i\right", str(i)+r"\right"))


