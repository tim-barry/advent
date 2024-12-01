#(2024) moved input data (was included as multiline string)
s = open("7.in").read().strip().split("\n")

import sys
sys.setrecursionlimit(10000)

#l = []

d = {}
rests = []
holds = []

for line in s:
	i = line.find(" ")
	name = line[:i]
	weight = int(line[line.find("(")+1:line.find(")")])
	d[name] = [weight,[]]
	if ">" in line:
		above =  line[line.find(">")+2:].strip().split(", ")
		rests.extend(above)
		d[name][1] = (above)
		holds.append(name)
		

def find_wrong(l):
	if(len(l)<2):
		return -1
	if len(l)==2:
		if l[0]!=l[1]:
			return 0
		else:
			return -1
	if l[0]==l[1]:
		goal = l[0]
	else:
		goal = l[2]
	if all([x==goal for x in l]):
		return -1
	return l.index( [x for x in l if x!=goal][0] ),goal

def set_totals(d,root):
	for s in d[root][1]:
		set_totals(d,s)
	totals = [d[s][2] for s in d[root][1]] # their total weights
	
	thistotalweight = d[root][0] + sum(totals)
	d[root].append(thistotalweight)
	d[root].append(totals)

def validate(d, name, goal=0): # return 0 [for 2] or "correct value"
	if goal==d[name][2]:
		return 0
	
	t = find_wrong(d[name][3])
	print name, goal, 'd[name]:',d[name], 't:',t
	
	if t==-1:
		return str( goal - sum(d[name][3]) )
	elif len(d[name][1])==2: # 2 children
		a = validate(d, d[name][1][0], d[name][3][1])
		b = validate(d, d[name][1][1], d[name][3][0])
		return a or b
	else:
		return validate(d, d[name][1][ t[0] ], t[1] )

#rests = sum([line[2:] for line in s if line[2:]],[])


root =  [h for h in holds if h not in rests][0]
print root #aapssr

set_totals(d,root)
print validate(d,root) # 1458
