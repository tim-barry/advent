
fn = "input25.txt"
f=open(fn,'r')
r=f.read()
f.close()

lines = r.strip().split('\n')

pts = [eval(line) for line in lines]

def manhattan(p1,p2):
	return sum(abs(a-b) for a,b in zip(p1,p2))

def same_const(p1,p2):
	return manhattan(p1,p2)<=3

def union(d,p1,p2):
	d[d[p1]] = d[p2] # parent p1 = parent p2

def find(d,p):
	if d[p]!=p: # not own parent
		new_parent = find(d,d[p]) # update
		d[p] = new_parent
	return d[p] # parent

# union-find
const = {p:p for p in pts}
for i,p1 in enumerate(pts):
	for j,p2 in enumerate(pts):
		if j>i: # avoid double-counting
			if find(const,p1)!=find(const,p2):
				if same_const(p1,p2): # in same constellation (edge)
					union(const,p1,p2) # join constellation

for p in pts:
	find(const,p) # final update to correct parents

print len(set(const.values())), "constellations"
