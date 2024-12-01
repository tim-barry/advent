from collections import defaultdict,deque

fn = "input18.txt"
f=open(fn,'r')
r=f.read()
f.close()

test = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""

#r = test

yard = map(list,r.strip().split('\n'))
S = len(yard)

def adj(yard,y,x):
	return [yard[ty][tx] for ty in range(y-1,y+2) for tx in range(x-1,x+2)
		if (tx-x or ty-y) and 0<=ty<S and 0<=tx<S]

def step(yard,y,x):
	t = adj(yard,y,x)
	if yard[y][x]==".": #open
		if t.count("|")>=3:
			return "|"
		return "."
	elif yard[y][x]=="|": #tree
		if t.count("#")>=3:
			return "#"
		return "|"
	else: # "#" lumber
		if "#" in t and "|" in t:
			return "#"
		return "."

def newyard(yard):
	ny = [row[:] for row in yard]
	for y in xrange(S):
		for x in xrange(S):
			ny[y][x] = step(yard,y,x)
			if 0 and y==1 and x==5:
				print yard[y][x]
				print ny[y][x]
				print adj(yard,y,x)
				raw_input()
	return ny

def tot(yard):
	tot = [0]*3
	for row in yard:
		for s in row:
			if s=="#":
				tot[2]+=1
			elif s=="|":
				tot[1]+=1
			else:
				tot[0]+=1
			#tot[".|#".find(square)]+=1
	return tot[1]*tot[2]

def printyard(yard):
	for line in yard:
		print "".join(line)

#printyard(yard)
#raw_input()

t= 0
X = 1000
while t<X:
	yard = newyard(yard)
	if t%100==0:
		print t
	t+=1
"""
while not raw_input():
	yard = newyard(yard)
	t+=1
	printyard(yard)

oldyard = [row[:] for row in yard]
yard = newyard(yard)
t+=1
printyard(oldyard)
raw_input()
while oldyard!=yard:
	yard = newyard(yard)
	t+=1
"""

L = (1000000000-X) % (28) # modulo period
t = 0
while t<L:
	yard = newyard(yard)
	

print tot(yard)
