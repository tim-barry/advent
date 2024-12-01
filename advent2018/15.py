
fn = "input15.txt"
f=open(fn,'r')
r=f.read()
f.close()

test0 = """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
"""

test1 = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
"""

test2 = """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
"""

test3 = """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
"""

testEx = """
###########
#G..#....G#
###..E#####
###########
"""

#r = testEx

data = r.strip()

# Utility
def printboard(unocc, units):
	for y,row in enumerate(unocc):
		s = ""
		for x,col in enumerate(row):
			if unocc[y][x]:
				s+='.'
			else:
				for u in units:
					if u[0]==y and u[1]==x:
						s+= "EG"[u[2]]
						break
				else:
					s+="#"
		print s

def printpath(unocc,path):
	unocc = [row[:] for row in unocc]
	units = []
	for y,x in path:
		unocc[y][x] = 0
		units.append([y,x,1,0])
	printboard(unocc,units)

# h/t /u/VikeStep (github: CameronAavik)
def neighbours(y, x):
	return [[y+dy,x+dx] for dy,dx in [(-1,0),(0,-1),(0,1),(1,0)]]

"""
from collections import deque
def bfs_orig(start, unocc, goals):
	# traverse the cave in distance/reading order
	visited = [[0]*len(unocc[0]) for _t in range(len(unocc))]
	check = deque([[start]])
	visited[start[0]][start[1]] = 1
	while len(check):
		path = check.popleft()
		y,x = c = path[-1] # most recent coord
		if c in goals:
			return path # next move is the first step in this path
		#for ty,tx in neighbours(y,x):
		#	if unocc[ty][tx] and not visited[ty][tx]:
		#		visited[ty][tx] = 1
		#		check.append(path+[[ty,tx]])
		for dy,dx in [(-1,0),(0,-1),(0,1),(1,0)]: # Reading order!
			if unocc[y+dy][x+dx] and not visited[y+dy][x+dx]:
				visited[y+dy][x+dx]=1
				check.append(path+[[y+dy,x+dx]])
	return [] # no path to any goals
"""

def bfs(start, unocc, goals):
	# traverse the cave in distance/reading order
	visited = [[0]*len(unocc[0]) for _t in range(len(unocc))]
	check = [[start]]
	visited[start[0]][start[1]] = 1
	while check:
		check_next = []
		while check:
			path = check.pop(-1) # pop from the end (faster)
			y,x = c = path[-1] # most recent coord
			if c in goals:
				return path # next move is the first step in this path
			for dy,dx in [(-1,0),(0,-1),(0,1),(1,0)]: # Reading order!
				if unocc[y+dy][x+dx] and not visited[y+dy][x+dx]:
					visited[y+dy][x+dx]=1
					check_next.append(path+[[y+dy,x+dx]])
		check = sorted(check_next, key=lambda path:path[-1], reverse=True)
		# sort by reading order of last position (thanks to /u/spencer8ab for pointing out the problem)
	return [] # no path to any goals

lines = data.strip().split('\n')
orig_units = [[y,x,lines[y][x]=="G",200]
				for y in range(len(lines))
				for x in range(len(lines[0]))
				if lines[y][x] in "EG"]
ELF = 0

ATP = 3
while ATP<300:
	units = [u[:] for u in orig_units]
	unoccupied = [[c=="." for c in line] for line in lines]
	elfDead = 0
	rounds = 0
	while 1: # rounds
		units.sort() # reading order
		combat_continues = 0
		for unit in units[:]: # this unit's turn
			if unit not in units:
				continue # was killed
			y,x,team,hp = unit
			adj = [[y+dy,x+dx,1-team] for dy,dx in [(-1,0),(0,-1),(0,1),(1,0)]]
			attack_list = [u for u in units if u[:3] in adj]
			if attack_list: # adjacent: go to Attack stage
				combat_continues = 1
			else:
				reachable = []
				combat_continues = 0
				for target in units:
					ty,tx,target_team,thp = target
					if target_team != team:
						combat_continues = 1
						target_adj = neighbours(ty,tx)
						#target_adj = [[ty+dy,tx+dx]
						#	for dy,dx in [(-1,0),(1,0),(0,1),(0,-1)]]
						reachable.extend([p for p in target_adj
							if unoccupied[p[0]][p[1]]])
				if combat_continues==0:
					break
				if not reachable: # no open squares in range of target: end turn
					continue
				mv = bfs([y,x], unoccupied, reachable)
				if not mv: # cannot find path (blocked): end turn
					continue
				mv = mv[1] # first step on path
				unoccupied[y][x] = 1 # leave current space
				y,x = unit[:2] = mv
				unoccupied[y][x] = 0 # occupy new space
				adj = [[y+dy,x+dx,1-team] for dy,dx in [(-1,0),(0,-1),(0,1),(1,0)]]
				attack_list = [u for u in units if u[:3] in adj]
			if attack_list: # Attack stage
				hit = min(attack_list, key=lambda u:(u[3],u[0],u[1]))
				if team==ELF:
					hit[3]-=ATP
				else:
					hit[3]-=3
				if hit[3]<=0: # unit died
					if hit[2]==ELF:
						#print "Lost an elf with ATP",ATP
						elfDead = 1
						if ATP!=3:
							break
					units.remove(hit)
					unoccupied[hit[0]][hit[1]] = 1 #passable
		if elfDead and ATP!=3:
			break
		if combat_continues==0:
			break
		rounds+=1
	if ATP==3:
		print "part 1:", rounds * sum(u[3] for u in units)
	if not elfDead:
		break
	ATP+=1

print "part 2:", rounds * sum(u[3] for u in units)
