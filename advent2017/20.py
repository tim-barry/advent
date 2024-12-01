
f=open("20.in",'r')
s=f.read().strip().split("\n")
f.close()

def add(a,b):
	return [x+y for x,y in zip(a,b)]

def make_particle(s):
	return map(lambda q:eval(q[q.find("=")+1:].replace("<","[").replace(">","]")), s.split(", "))

l = [make_particle(line) for line in s]

while True:
	#mindist = 10000000000000000 #infinity  # part 1
	for i,t in enumerate(l):
		t[1] = add(t[1],t[2]) #add vel acc
		t[0] = add(t[0],t[1]) #add pos vel
		#dist = sum([abs(x) for x in t[0]]) # part 1
		#if dist<mindist:
		#	mindist = dist
		#	closest = i
	pos = zip(*l)[0]
	l = [p for p in l if pos.count(p[0])==1] # part 2
	print len(l)
	#print closest #part 1


