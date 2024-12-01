
fn = "input10_alt.txt"
f=open(fn,'r')
r=f.read()
data=r.strip()
f.close()

test = """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
""".strip().split('\n')

lines = data.split('\n')
#lines = test

def extract_ints(a_string): # h/t day 10 /u/IGChris
    return map(int, re.findall(r'-?\d+', a_string))


# updated parsing (1)
lines = [line.replace("<","[").replace(">","]")[9:] for line in lines]
ptvs = [map(eval,line.split(" velocity=")) for line in lines]


# re parsing (2)
import re
re_ptvs = [extract_ints(s) for s in lines]
re_ptvs2 = map(lambda l:[l[:2],l[2:]], re_ptvs)

def bounds(l):
	return map(min,l),map(max,l)

def printpts(points):
	(xmin,ymin),(xmax,ymax) = bounds(zip(*points))
	for y in xrange(ymin,ymax+1):
		line=""
		for x in xrange(xmin,xmax+1):
			if [x,y] in points:
				line+="#"
			else:
				line+=" "
		print line

def add(v1,v2):
	return [a+b for a,b in zip(v1,v2)]

# Method 1: iterate
def method1(ptvs):
	points,velocities = zip(*ptvs)
	ytol = 15	# tolerance for height of text
	s = 0		# seconds to wait
	while True:
		(xmin,ymin),(xmax,ymax) = bounds(zip(*points))
		if abs(ymax-ymin) < ytol:
			break
		points = [add(pt,v) for pt,v in zip(points,velocities)]
		s+=1
	# originally, I had a larger height tolerance
	# and printed in another while loop here.
	return (points,s) # part 1, part 2

# Method 2: solve the linear equation: p1 + kv1 = p2 + kv2
# ->  k = (p2-p1)/(v1-v2)   (use either component)
# solve using points that have large velocities for best accuracy.
# re_ptvs: [ [x,y,vx,vy] ...]


import re
def extract_ints(a_string): # h/t /u/IGChris
	return map(int, re.findall(r'-?\d+', a_string))

def bounds(l):
	return map(min,l),map(max,l)

def printpts(points):
	(xmin,ymin),(xmax,ymax) = bounds(zip(*points))
	for y in xrange(ymin,ymax+1):
		line=""
		for x in xrange(xmin,xmax+1):
			if [x,y] in points:
				line+="#"
			else:
				line+=" "
		print line

def parallel(p1,p2): # are their (integer) velocities parallel?
	return p1[2]*p2[3] == p2[2]*p1[3]

ptvs2 = [extract_ints(s) for s in lines]
#end = 30 # take the first 30 points to get a good solution

def method2(ptvs,end=30):
	vel = lambda v:(v[2]*v[2] + v[3]*v[3])
	ptvs = sorted(ptvs, key=vel, reverse=True) # sort by velocity
	print "using first %d points: velocities"%end , map(vel,ptvs[:end])
	ks = [] # guess seconds based on intersections of each pair
	for i,p1 in enumerate(ptvs[:end]): # O(pts^2)/2
		for p2 in ptvs[i+1:end]:
			if not parallel(p1,p2):
				if p1[2] != p2[2]: # avoid division by 0
					_k = (p2[0]-p1[0])/(p1[2]-p2[2]) # use x component
				else:
					_k = (p2[1]-p1[1])/(p1[3]-p2[3]) # use y component
				ks.append(_k)
	k = max(set(ks),key=ks.count) # use mode instead of mean as it is more stable
	points = [[p[0] + k*p[2], p[1] + k*p[3]] for p in ptvs]
	return (points,k)

print "Method 2:"
points,k = method2(ptvs2,6)
printpts(points)
print ""
print k
print ""
"""
print "Method 1:"
points,s = method1(ptvs)
printpts(points)
print k
"""
