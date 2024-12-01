
l = [int(line.strip()) for line in open("10.txt")]

from collections import Counter

test = [
    28,
    33,
    18,
    42,
    31,
    14,
    46,
    20,
    48,
    47,
    24,
    23,
    49,
    45,
    19,
    38,
    39,
    11,
    1,
    32,
    25,
    35,
    8,
    17,
    7,
    9,
    4,
    2,
    34,
    10,
    3,
]

a = sorted(l)


a.append(a[-1]+3)
a.insert(0,0)

print(a)
diffs = [a[i]-a[i-1] for i in range(1,len(a))]
print(diffs)
c = Counter(diffs)
print(c)
print(c[1]*c[3])

res = [len(s) for s in ''.join(map(str,diffs)).split('3')]
# print(max(res))  = 4
#diffs[i] == 3 -> a[i], a[i+1] are mandatory
# count combos for in-between sections
poss = {
    0: 1,
    1: 1,
    2: 2,
    3: 4,
    4: 7
}
result = 1
for r in res:
    result *= poss[r]
print(result)

