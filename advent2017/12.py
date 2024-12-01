
from math import *

s = """

"""

#"""
f=open("12.in",'r')
s=f.read().strip().split("\n")
f.close()
#"""

d = {}
visited = {}

for line in s:   # build graph - may have duplicates
	a,b = line.split(" <-> ")
	b = b.split(', ')
	d[a] = d.get(a,[])+b
	for t in b:
		d[t] = d.get(t,[])+[a]

groups = 0
while sorted(visited.keys())!=sorted(d.keys()):
	q = [k for k in d.keys() if k not in visited][:1]
	#q = ["0"] #part 1
	i = 0
	while i<len(q):
		if q[i] not in visited:
			visited[q[i]] = 1
			q.extend(d[q[i]])
		i+=1
	groups+=1
	#break #part 1


#print len(visited.keys()) #part 1
print groups
