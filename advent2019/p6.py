
# 36/12
# cleaned up 20.1.3

with open('input6.txt') as f:
    ol = [line.strip().split(')') for line in f]

d = {b:a for a,b in ol}  # b orbits a
tot = 0
for b in d:
    while b != "COM":
        b = d[b]
        tot+=1
print tot  # part 1 -- sum of distances to COM from every object

a = d['YOU']
b = d['SAN']
def path_to_COM(p):
    pth = [p]
    while pth[-1]!="COM":
        pth.append(d[pth[-1]])
    return pth
# distance to common ancestor
ac = path_to_COM(a)
bc = path_to_COM(b)
while ac and bc and ac[-1]==bc[-1]:
    ac.pop(-1)
    bc.pop(-1)

print(len(ac)+len(bc))  # part 2
