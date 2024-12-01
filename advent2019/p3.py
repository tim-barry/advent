
# added:
def ctol(c):
    return [c.real, c.imag]
def ctom(c):
    return abs(c.real)+abs(c.imag)
# better solution (easier to code, no line-intersection testing):
# use bfs-strategy, keeping dict and marking as visited (with dist)
# 2 dicts (1/wire)

# original solution (meh) -- took 20/30 mins to code

with open('input3.txt', 'r') as f:
    r = f.read().strip()

M={'R':1, 'L':-1, 'U': 1j, 'D': -1j}

wires = [s.split(',') for s in r.split()]
def getpts(w):
    pts = [0]
    for s in w:
        pts.append(pts[-1] + M[s[0]]*int(s[1:]))
    return pts

w1, w2 = www = map(getpts, wires)


def intersect((p1, p2), (p3, p4)):
    d1 = (p1-p2)
    d2 = (p3-p4)
    swap=0
    pts = [p1,p2,p3,p4]
    if d1.imag==0:
        d1,d2 = d2,d1  # swap
        p1,p2,p3,p4 = p4,p3,p2,p1
        swap=1
    if d1.real==0 and d2.imag==0:
        ys = [x.imag for x in pts]
        xs = [x.real for x in pts]
        if (len(set(xs))<=3 and len(set(ys))<=3
            and xs.count(min(xs))==1 and xs.count(max(xs))==1
            and ys.count(min(ys))==1 and ys.count(max(ys))==1):
            pt = [sorted(xs,key=xs.count)[-1], sorted(ys,key=ys.count)[-1]]
            return pt
    return None


d1=0
cross = []
dist = []
sec = []
for sec1 in zip(w1, w1[1:]):
    d1+=abs(sec1[0]-sec1[1])
    d2=0
    for sec2 in zip(w2, w2[1:]):
        d2+=abs(sec2[0]-sec2[1])
        pt = intersect(sec1,sec2)
        if pt is not None:
            # print(pt)
            cp = complex(*pt)
            tdist = d1+d2 - abs(cp-sec1[1]) - abs(cp-sec2[1])
            cross.append(pt)
            dist.append(tdist)
            sec.append((sec1,sec2))

md = lambda t:sum(map(abs,t))
crosses = sorted(zip(cross, sec), key=lambda(t,s):md(t))
print crosses[0]
print md(crosses[0][0])
crosses2 = sorted(zip(cross, dist), key=lambda(t,s): s)
print crosses2[0]
print crosses2[0][1]
# l = r.split()

# print l

