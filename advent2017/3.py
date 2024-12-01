
from math import *

# (2024) moved input data (originally included as single int)
IN = eval(open("3.in").read().strip())
IN = 1000000000

# part 1 - find distance from center
s = int(sqrt(IN)) #floor, then add until reach
# doesn't handle even/odd

move_left = IN - s**2

# will probably be off by one
if move_left >= s:
	move_left-=s
dist_in = s/2
dist_along = move_left - s/2
ans = dist_in + abs(dist_along)

print "part 1 answer:",ans,"\n\n\n"
# should be 430 = 558 - 128



# part 2
m = [[0]*100 for tt in xrange(100)]
nei = lambda x,y:[(x+a,y+b) for a in (-1,0,1) for b in (-1,0,1)]
getnval = lambda x,y: sum(getm(x1,y1) for x1,y1 in nei(x,y))
getm = lambda x,y: m[x][y]

m[0][0] = 1
i = 1
d = 0 # starting direction doesn't matter as long as it's consistent
x = 0
y = 0
while i<log(IN)/log(2):
	for t in xrange(i):
		if d==0:
			y+=1
		elif d==1:
			x+=1
		elif d==2:
			y-=1
		elif d==3:
			x-=1
		m[x][y] = getnval(x,y)
	d+=1
	for t in xrange(i):
		if d==0:
			y+=1
		elif d==1:
			x+=1
		elif d==2:
			y-=1
		elif d==3:
			x-=1
		m[x][y] = getnval(x,y)
		if m[x][y]>IN:
			break
	d=(d+1)%4
	i+=1
	if m[x][y]>IN: break

m = [row for row in m[-(len(m)/2):] + m[:len(m)/2] if any(row)]
m = [row[-(len(m)/2)-1:]+row[:len(m)/2 +1] for row in m[::-1]]

formatstr = "%%%dd"% len(str(max(map(max,m))))
print '\n'.join([' '.join([formatstr%i for i in row]) for row in m])

tmax = lambda l:min([i for i in l if i>=IN] or [0])
answer = tmax(map(tmax,m))
print "answer:", answer
