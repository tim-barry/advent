
from collections import defaultdict
import copy

f=open("24.in",'r')
bridg = [map(int,line.split("/")) for line in (line for line in f.read().strip().split("\n") if line[0]!="#")]
f.close()

# generate ~318,000 possible bridges
def nextpath(path=[],pos=0):
	poss_parts = [part for part in bridg if pos in part and part not in path]
	if not poss_parts:
		return [path]
	out = [] # possible full paths
	for part in poss_parts:
		i = part.index(pos)
		out.extend(nextpath(path+[part],part[1-i]))
	return out

value = lambda l:sum(a+b for a,b in l) # sum of parts

paths = nextpath()
#print len(paths)
npaths = sorted(paths,key=value)
print value(npaths[-1])
lpaths = sorted(npaths,key=lambda l:len(l))
print value(lpaths[-1])

"""
Originally tried graph search...
but it will check bridges several times
and generally takes much too long.


d = defaultdict(list)
for a,b in bridg:
	d[a].append(b)
	d[b].append(a)

#for a,b in bridg:
#	print a,'->',b,';'


nq = [0]
visited = []
while len(nq):
	curr = nq.pop()
	visited.append(curr)
	print " %d -> "%curr + ', '.join([str(x) for x in d[curr]])
	nq = nq + [x for x in d[curr] if x not in visited]

path = [0]
"""
"""
def dfs(graph,path,m=0):
	if not graph[path[-1]]:
		return 2*sum(path)-path[-1]
	for poss in graph[path[-1]]:
		nd = copy.deepcopy(graph)
		npath = path[:]+[poss]
		nd[path[-1]].remove(poss)
		nd[poss].remove(path[-1])
		t = dfs(nd,npath,m)
		if m<t:
			m=t
			print m
	return m
dfs(d,path)
"""
""" # BFS
q = [(d,path)]
strengths = []
while len(q):
	d,path = q.pop() # bfs takes too long
	if not d[path[-1]]:
		strengths.append( sum(path)*2 -path[-1] )
		#print path
	for poss in d[path[-1]]:
		nd = copy.deepcopy(d) # copy
		npath = path[:] + [poss] # copy
		nd[path[-1]].remove(poss)
		nd[poss].remove(path[-1])
		q.append((nd,npath))

print strengths
print max(strengths)
"""
