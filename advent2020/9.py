
l = [int(line.strip()) for line in open("9.txt")]

def ok(i, l):
    prevs = l[i-25:i]
    v = l[i]
    for p in prevs:
        if v-p in prevs:
            return True
    return False

i = 25
while ok(i,l):
    i += 1
print(l[i])
v = 85848519

def accum(l):
    tot = 0
    l2 = [0]
    for x in l:
        tot += x
        l2.append(tot)
    return l2

test = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576,
]

# print(accum(test))
# l = test
# v = 127

l2 = accum(l)
i = j = 0
while l2[i] - l2[j] != v:
    while l2[i] - l2[j] < v: i += 1
    print(l[j:i])
    while l2[i] - l2[j] > v: j += 1
    print(l[j:i])
print(min(l[j:i])+max(l[j:i]))

