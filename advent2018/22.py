from collections import defaultdict,deque
"""
can't enter a region if tool unsuitable
can't switch to unsuitable tool for current region
ideas: use (x,y,tool)
start: (0,0,1)
goal: (tx,ty,1)
(p,t) -> (p+d,t) (1)  or  (p,other_t) (7)

import re
def extract_ints(a_string): # h/t day 10 /u/IGChris
    return map(int, re.findall(r'-?\d+', a_string))


fn = "input22.txt"
f=open(fn,'r')
r=f.read()
f.close()

test1="""
"""
#r=test1
r=r.strip()
lines=r.split('\n')
"""

depth=510
tx,ty=10,10

def geoind(geo,ero,x,y):
	if x==0:
		return (y*48271) % 20183
	if y==0:
		return (x*16807) % 20183
	return (ero[y][x-1]*ero[y-1][x]) % 20183

#puzzle input:
depth=7305
tx,ty=13,734
#test
EX = 100

geo = []
ero = []
for y in range(ty+1+EX):
	geo.append([])
	ero.append([])
	for x in range(tx+1+EX):
		geo[y].append(geoind(geo,ero,x,y))
		ero[y].append(((geo[y][x]+depth)%20183))
		if x==tx and y==ty:
			geo[ty][tx] = 0
			ero[ty][tx] = (depth%20183)
for row in ero:
	print ''.join([".=|"[r%3] for r in row])
print "part 1:", sum(r%3 for row in ero[:ty+1] for r in row[:tx+1])

# part 2: fewest # minutes to reach target
#edge=defaultdict(int) # shortest time to get there

time={(0,0,1):0} # (x,y,tool): minutes
dt={(0,0,1):0}
# adjacent: (dx,dy,tool); (x,y,other_tool)
visited={(0,0,1)}
#t=0


q = [(0,0,1)]
while q and not (tx,ty,1) in visited:
	q = sorted(q,key=lambda p:-time[p]) # shortest time last (for pop)
	#print q
	#try:
	x,y,tool = p = q.pop()
	#print "now at:",p
	#except:
	#	print x,y,tool # last
	#	raise
	for d in range(-1,3): # directions
		nx = x+d/2
		ny = y+1--d%3
		if 0<=ny<=ty+EX and 0<=nx<=tx+EX: # valid
			if tool != ero[ny][nx]%3: # can move there with tool
				np = (nx,ny,tool)
				if np not in visited:
					dt[np]=1
					time[np] = time[p]+1
					q.append( np )
					visited|={np}
				elif np in q: # not yet visited (this does happen: 1034 -> 1004)
					time[np] = min(time[np],time[p]+1)
	other_tool = next(t for t in range(3) if t!=tool and t!=ero[y][x]%3)
	np = (x,y,other_tool)
	#ttime = time[p]+7
	if np not in visited:
		dt[np]=7
		time[np]=time[p]+7
		q.append( np )
		visited|={np}
	else: # already in queue
		if time[p]+7<time[np]:
			print "shouldn't happen"
			time[np]=time[p]+7

print 'target:',(tx,ty,1)
print "in visited?",(tx,ty,1) in visited
print "in time?",(tx,ty,1) in time.keys()
print "part 2:",time[(tx,ty,1)]
# 1034: too high
# 1004: correct

"""
	# search all paths can visit without changing tool
	p=edge.keys()[0]
	p,(d,tool) = edge.pop(p)
	print d,tool
	q={p}
	for y in range(ty+1):
		print ''.join([".=|*"[((x,y)in visited)*3 or ero[y][x]%3] for x in range(tx+1)])
	raw_input()
	visited|={p}
	while q:
		d+=1
		nx=set()
		for p in q:
			for d in range(-1,3):
				x,y=n=p[0]+d/2,p[1]+1--d%3
				if x<0 or y<0 or x>=MX or y>=MY: continue
				print "xy:",x,y
				if tool!=ero[y][x]%3 and not n in visited: # can enter with tool
					visited|={n}
					spath[n][tool]=d
					nx|={n}
				elif not n in edge:
					edge[n]=n,(d,tool)
				#spath[x,y][tool] = 7+min(spath[tx,ty][tool
				#spath[x,y]=min(
		q=nx
	for y in range(ty+1):
		print ''.join([".=|*"[((x,y)in visited)*3 or ero[y][x]%3] for x in range(tx+1)])
	raw_input()
"""

"""
	q.sort(key=lambda p:(p[0],abs(p[1]-tx)+abs(p[2]-ty)))
	if p2 and pos[0][0]>p2[0][0]:p=p2.pop(0)
	else:p=pos.pop(0)
	if p[1:3]==(tx,ty):
		print p[0]
		break
	np=[]
	np2=set()
	for dy,dx in [(-1,0),(1,0),(0,1),(0,-1)]:
		if p[2]+dy>=0 and p[1]+dx>=0 and (p[1]+dx,p[2]+dy)not in visited:
			if ero[p[2]+dy][p[1]+dx]%3 != p[3]:
				np.append( (p[0]+1,p[1]+dx,p[2]+dy,p[3]) )
			else:
				np2|={(p[0]+7,p[1],p[2],(p[3]+1)%3)}
				np2|={(p[0]+7,p[1],p[2],(p[3]+1)%3)}
	for p in np:
		pos.append(p)
	for p in np2:
		p2.append(p)

"""
