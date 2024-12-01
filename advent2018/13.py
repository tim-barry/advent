from collections import defaultdict,deque

#"""
fn = "input13.txt"
f=open(fn,'r')
r=f.read()
f.close()
#"""
test = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""

def nx(lines,y,x):
	ct = [(0<=y+dy<h and 0<=x+dx<w and lines[y+dy][x+dx] != ' ')
		for dx,dy in [[-1,0],[0,-1],[1,0],[0,1]] ]
	if ct[0] and ct[2]:
		return '-'
	elif ct[1] and ct[3]:
		return '|'
	else:
		return "!"

lines = map(list,r.split('\n'))
lines = lines[:-1]

w = len(lines[0])
h = len(lines)
carts = []
cid = 1
cts = [[0]*w for _ in range(h)]
for y,line in enumerate(lines):
	for x,c in enumerate(line):
		if c in "<>^v":
			carts.append([x,y,"<>^v".find(c),0,cid])
			cid+=1
			cts[y][x] = 1
			lines[y][x] = nx(lines,y,x)
#for line in lines:
#	print ''.join(line)

def right(i):
	return [2,3,1,0][i]
def left(i):
	return right(right(right(i)))

def printcarts():
	tl = [line[:] for line in lines]
	for c in carts:
		tl[c[1]][c[0]] = "<>^v"[cart[2]]
	for line in tl:
		print ''.join(line)

part1 = 1
while len(carts)>1:
	remove_carts = []
	carts.sort()
	for i,cart in enumerate(carts):
		if cts[cart[1]][cart[0]]==0:
			continue
		cts[cart[1]][cart[0]]=0
		d = cart[2]
		cart[d//2] += (d&1) or -1
		nxc = lines[cart[1]][cart[0]]
		if nxc == " ":
			print "something wrong",cart
		if nxc == '+':#turn l,s,r
			if cart[3]==0:
				cart[2] = left(cart[2])
			elif cart[3]==2:
				cart[2] = right(cart[2])
			cart[3] = (cart[3]+1)%3
		elif nxc == "\\":
			cart[2] = cart[2]^2
		elif nxc == '/':
			cart[2] = cart[2]^3
		if cts[cart[1]][cart[0]]: # collision
			if part1:
				print cart[:2]
				part1 = 0
			remove_carts.append(cts[cart[1]][cart[0]])
			cts[cart[1]][cart[0]] = 0 # signal remove other
			remove_carts.append(cart[4])
		else:
			cts[cart[1]][cart[0]] = cart[4] #id of cart here
	carts = [c for c in carts if c[4] not in remove_carts]
	if len(carts)==1:
		break

print carts[0]
