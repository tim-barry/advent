
f = "input3.txt"

with open(f) as r:
    lines = [l.strip() for l in r]
    W = len(lines[0])
    ns = [int(l,2) for l in lines]
    L = len(ns)

gamma = 0
epsil = 0

for b in range(W):
    bitsum = sum((x>>b)&1 for x in ns)
    most = bitsum>L/2
    gamma += most<<b
    epsil += (not most)<<b

print(gamma*epsil)

def rating(l, w, criteria):
    for b in range(w-1, -1, -1):
        #print([f"{x:0{b+1}b}" for x in l])
        bitsum = sum((x>>b)&1 for x in l)
        #print(bitsum)
        most_common = bitsum >= len(l)/2
        match = most_common
        if criteria:
            match = not match
        l = [x for x in l if (x>>b)&1==match]
        if len(l)==1:
            return l[0]
    print("more than 1 left! l=", l)
    return l[0]


l2 = [
0b00100,
0b11110,
0b10110,
0b10111,
0b10101,
0b01111,
0b00111,
0b11100,
0b10000,
0b11001,
0b00010,
0b01010,
]

#o2 = rating(l2, 5, 0)
#co2 = rating(l2, 5, 1)
o2 = rating(ns, W, 0)
co2 = rating(ns,W, 1)
print(o2,co2)
print(o2*co2)


