
f = "input1.txt"
def lmap(f,l): return list(map(f,l))

with open(f) as r:
    s = r.read()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

#v1
groups = s.split('\n\n')
arrs = [list(map(int,g.split())) for g in groups]

l = sorted(arrs,key=sum)[::-1]
print(sum(l[0]))
print(sum(l[0]+l[1]+l[2]))

#v2
arrs = [lmap(int,g.split()) for g in lgroups]
l = sorted(arrs, key=sum)[::-1]
#...
