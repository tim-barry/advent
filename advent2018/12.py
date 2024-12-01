from collections import defaultdict,deque

#"""
fn = "input.txt"
f=open(fn,'r')
r=f.read()
data=r.strip()
f.close()
#"""

lines = r.strip().split('\n')
state = lines[0].split(":")[1].strip()
rules = zip(*[l.split(" => ") for l in lines[2:]])

d1= defaultdict(lambda:'.')
d2= defaultdict(lambda:'.')
for i,c in enumerate(state):
	d1[i]=c
ds = [d1,d2] # alternate current and next states

def nx(d,i):
	return rules[1][rules[0].index(d[i-2]+d[i-1]+d[i]+d[i+1]+d[i+2])]

st = 0
en = len(state)
x = 0
while x < 200: # look at the output to guess this
	if x==20: # part 1
		print sum(k for k in ds[0].keys() if ds[0][k]=="#")
	while ds[x%2][st]=='.': # jigger bounds
		st+=1
	st-=2
	while ds[x%2][en]=='.':
		en-=1
	en+=2
	for i in range(st,en): # next iteration
		ds[(x+1)%2][i] = nx(ds[(x)%2], i)
	x+=1

#after this point (x=200), there are a fixed number of spaceships going +1
print sum(k+(50000000000-x) for k in ds[0].keys() if ds[0][k]=="#")

