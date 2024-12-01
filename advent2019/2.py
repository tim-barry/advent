
# 2016-2
# after 2019-2

with open('input2016-2.txt', 'r') as f:
    r = f.read().strip()

# l = [int(s) for s in r.split()]
l = r.split()
# print(l)

p = [1,1]
M = [[1,2,3],[4,5,6],[7,8,9]]
r = []
for line in l:
    for c in line:
        if c=='U' and p[1]>=1:
            p[1]-=1
        if c=='D' and p[1]<=1:
            p[1]+=1
        if c=='L' and p[0]>=1:
            p[1]-=1
        if c=='R' and p[0]<=1:
            p[1]+=1
    r.append(M[p[1]][p[0]])

print ''.join(str(i) for i in r)

