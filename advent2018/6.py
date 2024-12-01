
from collections import defaultdict
# from math import *

fn = "input6.txt"
f=open(fn,'r')
r=f.read()
r=r.strip()
f.close()

test1 = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""".strip()
input2 = """
 337, 150
 198, 248
 335, 161
 111, 138
 109, 48
 261, 155
 245, 130
 346, 43
 355, 59
 53, 309
 59, 189
 325, 197
 93, 84
 194, 315
 71, 241
 193, 81
 166, 187
 208, 95
 45, 147
 318, 222
 338, 354
 293, 242
 240, 105
 284, 62
 46, 103
 59, 259
 279, 205
 57, 102
 77, 72
 227, 194
 284, 279
 300, 45
 168, 42
 302, 99
 338, 148
 300, 316
 296, 229
 293, 359
 175, 208
 86, 147
 91, 261
 188, 155
 257, 292
 268, 215
 257, 288
 165, 333
 131, 322
 264, 313
 236, 130
 98, 60
 """.strip()
r = input2

l = r.split('\n')
coords = map(eval,l)

def DNE(p):
	return p[1]+p[0]

def DNW(p):
	return p[1]-p[0]

xs,ys = zip(*coords)
#NE = max(l,key=DNE)
#NW = max(l,key=DNW)
#SW = min(l,key=DNE)
#SE = min(l,key=DNW)
xmin = min(xs)
xmax = max(xs)
ymin = min(ys)
ymax = max(ys)
d = defaultdict(int)

rsize = 0
for x in xrange(xmin,xmax+1):
	for y in range(ymin,ymax+1):
		td = 0
		mind = xmax+ymax+3
		cr = None
		for i,c in enumerate(coords):
			md = abs(c[0]-x)+abs(c[1]-y)
			td+=md
			if md<mind:
				mind = md
				cr = i
			elif md==mind:
				cr = None
		if cr is not None:
			d[(x,y)] = cr # closest
		else:
			d[(x,y)] = -1
		if td < 10000:
			rsize+=1
print rsize

#cs = sorted(d.keys())
"""for y in xrange(ymin,ymax+1):
	s = ''
	for x in xrange(xmin,xmax+1):
		s+=`d[(x,y)]`[0]
	print s
"""

#cand = coords[:]
tot = [0]*(len(coords)+1)
for c in d.keys():
	tot[d[c]]+=1
#print tot
for x in xrange(xmin,xmax+1):
	for y in [ymin,ymax]:
		tot[d[(x,y)]]=0
for y in xrange(ymin,ymax):
	for x in [xmin,xmax]:
		tot[d[(x,y)]]=0
tot[-1]=0
print max(tot)
