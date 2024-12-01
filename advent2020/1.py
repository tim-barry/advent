import sys

l = [int(line) for line in sys.stdin]
print([a*b for a in l for b in l if a<=b and a+b==2020][0])
print([a*b*c for a in l for b in l for c in l if a<=b<=c and a+b+c==2020][0])
