from collections import defaultdict

fn = "input8.txt"
f=open(fn,'r')
r=f.read()
data=r.strip()
f.close()

test = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
#r = test

l = map(int,data.split())

def parse(l, i, part1=False):
	num_children = l[i]
	num_meta = l[i+1]
	i = i+2
	child_vals = []
	val = 0
	for c in xrange(num_children):
		i,ch_val = parse(l,i,part1)
		child_vals.append(ch_val)
	if part1:
		return i+num_meta,sum(l[i:i+num_meta])+sum(child_vals)
	for m in xrange(num_meta):
		meta = l[i]
		if len(child_vals)==0:
			val += meta
		else:
			if 0 <= meta-1 < len(child_vals): # valid
				val += child_vals[meta-1]
		i+=1
	return i,val

print parse(l,0,True)
print parse(l,0)
