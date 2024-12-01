# related to langton's ant

with open("22.in",'r') as f:
	grid=[[int(c=="#")*2 for c in row] for row in f.read().strip().split("\n")]

# d is 0,1,2,3 for right,down,left,up
d = 3 # start going up
def turnleft(d):
	return (d-1)%4
def turnright(d):
	return (d+1)%4

tot = 0
y = len(grid)/2
x = len(grid[0])/2

for t in xrange(10000000):
	if grid[y][x]==0:   # clean (0)
		d = turnleft(d)
	elif grid[y][x]==1: # weakened (1)
		tot+=1
	elif grid[y][x]==2: # infected (2)
		d = turnright(d)
	elif grid[y][x]==3: # flagged (3)
		d = (d+2)%4 # reverse
	grid[y][x] = (grid[y][x]+1)%4 # change state
	
	# move
	if d==0: #right
		x+=1
	elif d==1: # down
		y+=1
	elif d==2: # left
		x-=1
	elif d==3: # up
		y-=1
	
	# make grid infinite
	if y==-1:
		grid[0:0] = [[0]*len(grid[0])] # extend upwards
		y=0
	elif y==len(grid):
		grid[y:y] = [[0]*len(grid[0])] # extend downwards
	elif x==-1:
		for row in grid:
			row.insert(0,0) # left
		x=0
	elif x==len(grid[0]): # right
		for row in grid:
			row.append(0)

print tot

