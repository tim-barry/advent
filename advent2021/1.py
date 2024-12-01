
f="input1.txt"
with open(f) as r:
    s = r.readlines()

l = [int(line.strip()) for line in s]

p1 = sum(b>a for a,b in zip(l,l[1:]))
print(p1)

sums = [a+b+c for a,b,c in zip(l,l[1:],l[2:])]
p2 = sum(b>a for a,b in zip(sums,sums[1:]))
print(p2)

