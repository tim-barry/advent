
import time

#(2024) moved input data (originally included as string)
s = open("14.in").read().strip()


to_index = "01234567890abcdef"

def binary_knot_hash(s): #bin arr
	s = map(ord,s) + [17, 31, 73, 47, 23]
	i = 0
	l = range(256)
	skipsize = 0
	currpos = 0
	for junk in range(64):
		for t in s:
			#reverse(l, t, i)
			l[:t] = l[:t][::-1]
			i = (t+skipsize)%len(l) # <- need to mod
			skipsize+=1
			skipsize%=len(l)
			l = l[i:] + l[:i]  # move currpos to front
			currpos+=i
			currpos%=len(l)
	l = l[-currpos:] + l[:-currpos]
	dense_hash = []
	for x in range(16):
		dense_hash.append(reduce(lambda a,b:a^b, l[x*16:x*16+16]))
	return sum([ [(x&128)>>7, (x&64)>>6, (x&32)>>5, (x&16)>>4, (x&8)>>3 , (x&4)>>2, (x&2)>>1, x&1 ] for x in dense_hash],[])
	return ''.join(["%02x"%x for x in dense_hash])

#def to_binarr(hx):


def vis(l):
	return "\n".join([''.join([".#"[x] for x in row]) for row in l])

l = []
for i in range(128):
	hash_input = "ffayrhll" + "-" + str(i)
	hash_out = binary_knot_hash(hash_input)
	l.append(hash_out)
	#print i

#raw_input()

regions = 0
used = 0
for r in range(128):
	#time.sleep(0.3)
	while any(l[r]):
		#time.sleep(0.2)
		#print vis(l[r:r+30]) + "\n"
		q = [ (l[r].index(1),r) ]
		while len(q):
			x,y = q.pop()
			l[y][x]= 0 # set to 0
			if (y>0)   and (l[y-1][x]==1) and ((x,y-1) not in q):
				q.append((x,y-1))
			if (x>0)   and (l[y][x-1]==1) and ((x-1,y) not in q):
				q.append((x-1,y))
			if (x<127) and (l[y][x+1]==1) and ((x+1,y) not in q):
				q.append((x+1,y))
			if (y<127) and (l[y+1][x]==1) and ((x,y+1) not in q):
				q.append((x,y+1))
			used+=1
			#time.sleep(0.2)
			#print vis(l[r:r+25])+"\n"

		regions+=1

print "part 1:",used
print "part 2:",regions

