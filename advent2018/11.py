
"""
def max2d(l):
	return max(map(max,l))

#def gsum(g,x,y,s):
#	return sum(sum(row[x:x+s]) for row in g[y:y+s])

import re
def extract_ints(a_string): # h/t /u/IGChris
	return map(int, re.findall(r'-?\d+', a_string))

"""

#from itertools import accumulate # (python 3)
def accumulate(iterable): # from stackoverflow
	total = 0
	for i in iterable:
		total += i
		yield total

serialno = 9424 # puzzle input
#test: serialno = 8

def powerlevel(x,y):
	rid = x+10
	pl = rid*y
	pl+= serialno
	pl*= rid
	pl = (pl // 100)%10
	return pl-5

def colmap(func,grid): # map on columns instead of rows
	return zip(*map(func,zip(*grid)))

grid = [[powerlevel(x+1,y+1) for x in xrange(300)] for y in xrange(300)]
partial_row = map(accumulate, grid)
partial_2d = colmap(accumulate, partial_row)

NWsums = map(list,partial_2d)
NWsums = [[0]+row for row in NWsums] # pad with zeros along top/left
NWsums = [[0]*301] + NWsums

ms,mx,my = 0,0,0
best = 0
for s in xrange(1,300+1):
	for x in xrange(300-s+1):
		for y in xrange(300-s+1):
			power = NWsums[y+s][x+s] - NWsums[y+s][x] \
					- NWsums[y][x+s] + NWsums[y][x]
			if power > best:
				best = power
				mx,my,ms = x+1,y+1,s
				#print best,mx,my,ms
	if s==3:
		print "part 1: %d,%d"%(mx,my)
print "part 2: %d,%d,%d"%(mx,my,ms)
