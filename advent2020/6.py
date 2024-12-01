
with open("6.txt") as f:
    r=f.read()

groups = r.split('\n\n')
counts = [len(set(g)-{" ","\n"}) for g in groups]
print(sum(counts))

from functools import reduce
print(sum(len(reduce(set.intersection, [set(p) for p in g.split()])) for g in groups))
