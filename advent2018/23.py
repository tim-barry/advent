from collections import defaultdict,deque


fn = "input23.txt"
# fails hard on input23_adver.txt
f=open(fn,'r')
r=f.read()
f.close()

test1="""
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
"""
#r=test1
r=r.strip().replace("<","[").replace(">","]")
lines=r.split('\n')
#"""
bots = [eval('dict('+s+',inrange=[],both=[],intersect={})') for s in lines]
lbots= [list(b['pos'])+[b['r']] for b in bots]

dist=lambda p,q:sum(abs(a-b)for a,b in zip(p,q))

def inrange(p):
	return sum(1 for b in bots if dist(b['pos'],p)<=b['r'])

#position, signal radius
for b1 in range(len(bots)):
	for b2 in range(len(bots)):
			d=dist(bots[b1]['pos'],bots[b2]['pos'])
			bots[b1][b2]=d
			if d<=bots[b1]['r']:
				bots[b1]['inrange'].append(b2)
			if d<=bots[b1]['r']+bots[b2]['r']:
				bots[b1]['both'].append(b2)
			bots[b1]['intersect'][b2] = d-bots[b1]['r']-bots[b2]['r']
print "part 1:", len(max(bots,key=lambda d:d['r'])['inrange'])

print "upper bound on bots in reach of any position:",max(len(bot['both'])for bot in bots)
print "(likely smaller though)"


"""bestbot = max(bots,key=lambda d:len(d['both']))
# find largest clique in 'contain common squares graph' (approximate)
both_l = [set(bot['both']) for bot in bots]
"""
# use 'both': largest common list
"""
add = lambda p,q:[a+b for a,b in zip(p,q)]
def corners(bot):
	p=bot['pos']
	r=bot['r']
	for d in [-r,r]:
		for dp in [(d,0,0),(0,d,0),(0,0,d)]:
			yield add(p,dp)

def valid_intersection(bot1,bot2):
	p1,r1,p2,r2=bot1['pos'],bot1['r'],bot2['pos'],bot2['r']
	return any(dist(p,p2)<=r2 for p in corners(bot1)) or \
			any(dist(p,p1)<=r1 for p in corners(bot2))
"""

inval2=[[x for x in range(len(bots)) if x not in bots[b]['both']]
		for b in range(len(bots))]
inval=map(len,inval2)
print 'max inval:',max(inval),'at bot',inval.index(max(inval))
print 'min inval:',min(inval),'at bot',inval.index(min(inval))

def dorigin(bot):
	return max(0,sum(map(abs,bot['pos']))-bot['r'])

def far_dorigin(bot):
	return sum(map(abs,bot['pos']))+bot['r']

#tbot = {'pos':(1,1,1),'r':1}
#print "dorigin test",dorigin(tbot) # 2: correct

removed = [0]*len(bots)
while any(inval):
	i = inval.index(max(inval))
	#i = max([j for j,t in enumerate(inval) if t==max(inval)],key=lambda j:dorigin(bots[j]))
	#for j in inval2[i]:
	#	if inval[j]==inval[i]:
	#		if dorigin(bots[j])<dorigin(bots[i]): # remove bot i
	#			print "swapped with ",max(inval)
	#			i=j # remove whichever is further away from origin
	#print "worst misses",max(inval)
	print "removed bot",i,'with',inval[i],'unconnected, dorigin:',dorigin(bots[i])
	inval[i]=0 # ignore on further loops
	removed[i]=1 # remove it
	t=0
	for j in inval2[i]:
		inval[j]-=1
		if inval[j]==0:
			t+=1
		inval2[j].remove(i)

print removed.count(0),"in intersection (clique)"
#vol = intersect(*[v for v,r in zip(volumes,removed) if not r])
nbots = [bot for i,bot in enumerate(bots) if not removed[i]]

L=[]
for b1 in xrange(len(bots)):
	if removed[b1]:
		continue
	for b2 in xrange(len(bots)):
		if b1<b2 and not removed[b2]:
			if bots[b1]['intersect'][b2]==0:
				L+=(b1,b2),
print "pairs of bots with only 1 line/plane/point in common:",
print len(L)
print L


def abcd(bot):
	x,y,z = bot['pos']
	return [ x+y-z, x-y+z, -x+y+z, x+y+z ]
def edge_planes(bot): # [[amin,amax], [bmin,bmax] ... ]
	r = bot['r']
	return [[t+_r for _r in [-r,r]] for t in abcd(bot)]

for b1,b2 in L:
	p1 = edge_planes(bots[b1])
	p2 = edge_planes(bots[b2])
	for c,d1,d2 in zip('abcd',p1,p2):
		t1 = d1[0]==d2[1]  # d1 min == d2 max
		t2 = d1[1]==d2[0]  # other
		if t1 or t2:
			print c,": bot", [b1,b2][t2],'<=',d1[t2],'<= bot',[b1,b2][t1]


furthest_bot = max(nbots,key=dorigin)
closest_bot = min(nbots,key=far_dorigin)
print 'part 2 bounded by:', dorigin(furthest_bot),far_dorigin(closest_bot)

# use 3-dimensional abc(d) bounds to directly calculate x,y,z
pmin3 = [[x+y-z-r,x-y+z-r,-x+y+z-r,x+y+z-r]for r,(x,y,z)in[(b['r'],b['pos'])for b in nbots]]
pmax3 = [[x+y-z-r,x-y+z-r,-x+y+z-r,x+y+z-r]for r,(x,y,z)in[(-b['r'],b['pos'])for b in nbots]]
# pmin3,pmax3 = zip(*[zip(*edge_planes(b)) for b in nbots])
pmin3max = [max(col)for col in zip(*pmin3)]
pmax3min = [min(col)for col in zip(*pmax3)]
for i in range(4):
	print ['x+y-z','x-y+z','-x+y+z','x+y+z'][i],'in',
	mn,mx = pmin3max[i],pmax3min[i]
	print mn,mx,':',mx-mn

z1 = (pmin3max[2]+pmin3max[1])/2
y1 = (pmin3max[2]+pmin3max[0])/2
x1 = (pmin3max[1]+pmin3max[0])/2
z2 = (pmax3min[2]+pmax3min[1])/2
y2 = (pmax3min[2]+pmax3min[0])/2
x2 = (pmax3min[1]+pmax3min[0])/2
#for z in range(z1,z2):
#	for y in range(y1,y2):
#		for z in range(z1,z2):
print "final result (assuming single point): part 2:", x1+y1+z1


# Trying someone else's solution: gives 94481130
def calc2(bots):
	#bots = lbots #get_bots(values)
	#xs = [x[0] for x in bots]
	#ys = [x[1] for x in bots]
	#zs = [x[2] for x in bots]
	xs,ys,zs,rs = zip(*bots)
	dist = 1
	while dist < max(xs) - min(xs):
		dist *= 2
	while True:
		target_count = 0
		best = None
		best_val = None
		for x in xrange(min(xs), max(xs) + 1, dist):
			for y in xrange(min(ys), max(ys) + 1, dist):
				for z in xrange(min(zs), max(zs) + 1, dist):
					count = 0
					for bx, by, bz, bdist in bots:
						calc = abs(x - bx) + abs(y - by) + abs(z - bz)
						if (calc - bdist) / dist <= 0:
							count += 1
					if count > target_count:
						target_count = count
						best_val = abs(x) + abs(y) + abs(z)
						best = (x, y, z)
					elif count == target_count:
						if abs(x) + abs(y) + abs(z) < best_val:
							best_val = abs(x) + abs(y) + abs(z)
							best = (x, y, z)
		if dist == 1:
			return best_val
		else:
			xs = [best[0] - dist, best[0] + dist]
			ys = [best[1] - dist, best[1] + dist]
			zs = [best[2] - dist, best[2] + dist]
			dist /= 2

print "part 2 (someone else's solution):",calc2(lbots) # gives 94481130

sub=lambda p,q:[a-b for a,b in zip(p,q)]
#add=lambda
#minxs = [bot['pos'][0]-bot['r'] for bot in nbots]
#print "min x:",max(minxs)

""" 1- and 2- dimensional mins
pmin1 = [[p-bot['r']for p in bot['pos']] for bot in nbots]
pmax1 = [[p+bot['r']for p in bot['pos']] for bot in nbots]
for c,mns,mxs in zip('xyz',zip(*pmin1),zip(*pmax1)):
	print c,'in',max(mns),min(mxs),":",min(mxs)-max(mns)

pmin2 = [[[x+y-r,x-y-r],[x+z-r,x-z-r],[y+z-r,y-z-r]]for r,(x,y,z) in [(b['r'],b['pos'])for b in nbots]]
pmax2 = [[[x+y-r,x-y-r],[x+z-r,x-z-r],[y+z-r,y-z-r]]for r,(x,y,z) in [(-b['r'],b['pos'])for b in nbots]]
pmin2s = zip(*pmin2)
pmin2max = [map(max,zip(*col))for col in pmin2s]
pmax2min = [map(min,zip(*col))for col in zip(*pmax2)]

for c in [0,1]:
	for d in [1,2]:
		if c!=d:
			i=c+d-1
			cc,dd="xyz"[c],"xyz"[d]
			mn1,mn2 = pmin2max[i]
			mx1,mx2 = pmax2min[i]
			print cc,'+',dd,'in',mn1,mx1,":",mx1-mn1
			print cc,'-',dd,'in',mn2,mx2,":",mx2-mn2
"""

"""
print "volume in abc coords:",vol
xvol = xyz(*vol[0]),xyz(*vol[1])
print "volume in xyz coords:",
xyzlim = zip(*xvol)
print "smallest distance:",sum(map(min,xyzlim))
#import itertools as it
#comb = it.combinations
"""

"""
def intersect(*vs): # given smaller & larger corners of each
	vs,vl = zip(*vs)
	return [map(max,zip(*vs)),map(min,zip(*vl))]

# if we have bot at origin with r=1:
# we want (+-1,0,0),(0,+-1,0),(0,0,+=1) to be represented.
def DiagCube(bot): # pos,r
	# our dimensions are abc: x+y+z,x+y-z,x-y-z
	# we want xyz(-1,0,0) -> abc(-1,-1,-1)
	# and xyz(1,0,0) -> abc (1,1,1)
	#x,y,z = bot['pos']
	r = bot['r']
	a,b,c = abc(*bot['pos'])
	return [[a-r,b-r,c-r],[a+r,b+r,c+r]]

def abc(x,y,z):
	return [x+y+z,x+y-z,x-y-z]
	#return [x-y,y

def xyz(a,b,c):
	return (a+c)/2,(b-c)/2,(a-b)/2

#print intersect([[0,0,0],[2,1,2]],[[0,0,0],[2,2,1]],[[0,0,0],[1,2,2]])

def valid(vol): # cuboid area not negative
	return all(s<=l for s,l in zip(*vol))

#va =[[0,0,0],[2,2,2]] # cube
#vb =[[0,1,1],[2,3,3]] # cube offset by [0,1,1]
#print zip(va,vb)
#print intersect(va,vb)
#tbot = {'pos':(0,0,0),'r':1}
#tbot2= {'pos':(1,0,0),'r':1}
#print intersect(DiagCube(tbot),DiagCube(tbot2))
#volumes = [DiagCube(bot) for bot in bots]

# remove the one that has the most invalid intersections
# O(N^4)
"""

"""
vol = [[0,0,0],[-1,-1,-1]]
best_d = 1e30
N = 1
while best_d==1e30:
	for c in comb(volumes,N):
		nvol = reduce(intersect,c)
		if valid(nvol):
			d=dist(nvol)
			if d<best_d:
				best_d=d
				print best_d
	N+=1
print "part 2:",best_d
# use binary search
#q = []
#while q:
	
"""
""" Old code (bad ideas)
#avg=lambda ps:[sum(p)/len(p) for p in zip(*ps)] # guess with 'center'
#ax,ay,az = avg([bot['pos'] for bot in bots])
bestp = (0,)*3
bestc = 0
bestd = 10000000000000
#print ax,ay,az
ax,ay,az=(24569905, 44301676, 21411458) # ??
ax,ay,az=(24819905, 45251676, 22361458) # 878
ax,ay,az=(24809905, 45241676, 22351458) # 878
ax,ay,az=(24799905, 45241676, 22360458) # 878
ax,ay,az=(24788665, 45241922, 22370574)
#(24788675, 45241921, 22370565)
#(24788705, 45241936, 22370538)
#(24788905, 45241976, 22370358)#(24789905, 45242676, 22369458)
M=10
m= 1 #M/10
Ax,Ay,Az = [range(at-M,at+M,m) for at in [ax,ay,az]]
for x in Ax:
	for y in Ay:
		for z in Az:
			count = sum(dist((x,y,z),bot['pos'])<=bot['r'] for bot in bots)
			d=x+y+z
			if count>bestc or (count==bestc and d<bestd):
				bestc,bestp = count,(x,y,z)
				bestd=d
	print bestc,bestp
	print 'dist:',bestd
#can_transmit
"""
