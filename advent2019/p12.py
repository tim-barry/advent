
from math import gcd
import re
with open('input12.txt') as f:
    moons = [list(map(int,re.findall(r'-?\d+', line))) for line in f]
    orig_coords = list(zip(*moons))

vs = [[0]*3 for m in moons]

def up_v(moons, vs):
    for x,m1 in enumerate(moons):
        for m2 in moons: # each other moon
            for i, (p1,p2) in enumerate(zip(m1,m2)):
                vs[x][i] += 1 if p1 < p2 else 0 if p1==p2 else -1
def add_v(moons, vs):
    for v,moon in zip(vs,moons):
        for i in range(len(moon)):
            moon[i]+=v[i]

def energy(l): return sum(map(abs, l))
def tot_energy(moon, v): return energy(moon)*energy(v)  # potential * kinetic

period = [0]*3
for x in range(1000):
    up_v(moons, vs)
    add_v(moons,vs)

print(sum(tot_energy(moon, v) for moon, v in zip(moons,vs)))

period = 1
for c, ps in enumerate(map(list, orig_coords)):
    pv = [0]*len(ps)
    xd = 0
    while xd==0 or any(pv):  # while velocity is not 0
        for i,x1 in enumerate(ps):
            for x2 in ps:
                pv[i] += 1 if x1<x2 else 0 if x1==x2 else -1
        for i in range(4):
            ps[i]+=pv[i]
        xd+=1
    print("period %s: %s" % (c, xd))
    period *= xd // gcd(period, xd)  # fix to compute lcm instead of prod

print(period * 2)  # part 2
