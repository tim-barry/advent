
# 2016-1
# practice for 2019-1

f = open('input2016-1.txt', 'r')
r = f.read().strip()
f.close()
l = [s for s in r.split(', ')]

dist=lambda c:abs(c.real)+abs(c.imag)
vis = set()
twice = None

p = 0+0j
d = 1j  # N
for s in l:
    rot = s[0]
    go = int(s[1:])
    if rot=="R":
        d*=1j
    else:
        d*=-1j
    for t in range(go):
        p+=d
        if twice is None and p in vis:
            twice = p
        vis.add(p)
print dist(p)
print twice
print dist(twice)
