
TEST = 0

with open("21.in",'r') as f:
	rules=f.read()[:].strip().split("\n")
	# use [3:] for 21b.in since has weird format issue ["\xef ..."]
#print rules

if TEST:
	rules = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#""".split("\n")


def flip(square):
	return square[::-1]

def rotate(square): # ccw
	return tuple([tuple([square[y][x] for y in range(len(square))]) for x in range(len(square))[::-1]])

def printimg(img):
	print "\n".join(["".join(row) for row in img]) + "\n"



rd = {}

for s in rules:
	a,b = s.split(" => ")
	a=tuple(map(tuple,a.split("/")))
	b=tuple(map(tuple,b.split("/")))
	for i in range(4):
		rd[a] = b
		rd[flip(a)] = b
		a = rotate(a)
	# correct


print len(rd.keys())

def squaresum(squares):
	return tuple([sum(row,()) for row in zip(*squares)])


img = tuple(map(tuple, [".#.","..#","###"]))

printimg(img)

iters = 5 and 18
if TEST:
	iters = 2

for t in xrange(iters):
	oldimg = img
	if len(img)%2==0:
		step = 2
	else:
		step = 3
	if t%3==0: # 3
		if step!=3:
			print "Wrong"
	else:
		if step==3:
			print "Wrong"
	
	rows = [img[i:i+step] for i in range(0,len(img),step)]
	
	"""
	nrows = []
	for row in rows:
		squares = [tuple([r[i:i+step] for r in row]) for i in range(0,len(img),step)]
		#printimg(squaresum(squares)) # correct ^
		nrow = squaresum([rd[sq] for sq in squares]) # correct
		nrows.append(nrow)
	
	img = sum(nrows,()) # correct
	"""
	img = sum([
		squaresum([rd[sq] for sq in 
			[tuple([r[i:i+step] for r in row])
				for i in range(0,len(img),step)]])
		for row in rows],())
	#"""
	#printimg(img)
	"""
	block_size = step
	n = len(oldimg)
	pattern = oldimg
	new_blocks = []
	for r in range(n/block_size):
		block_row = []
		for c in range(n/block_size):
			block_in = tuple([tuple([pattern[r*block_size+rr][c*block_size+cc] for cc in range(block_size)]) for rr in range(block_size)])
			block_row.append(rd2[block_in])
		new_blocks.append(block_row)
	new_n = n/block_size*(block_size+1)
	def from_block(r,c):
		r0, r1 = r/(block_size+1), r%(block_size+1)
		c0, c1 = c/(block_size+1), c%(block_size+1)
		return new_blocks[r0][c0][r1][c1]
	new_pattern = [[from_block(r,c) for c in range(new_n)] for r in range(new_n)]
	pattern = new_pattern
	printimg(pattern)

"""

print "\ndone:"

print sum(img[y][x]=="#" for y in xrange(len(img)) for x in xrange(len(img)))
print sum(c=="#" for r in img for c in r)
