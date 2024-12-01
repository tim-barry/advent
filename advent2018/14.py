

inp = 540391
linp = map(int,str(inp))
LL = len(linp)

elf = [0,1] # indices into scb
scb = [3,7]
curr = scb[:] # most recent recipe scores
ls = len(scb)
t = -1
while t==-1 or ls<inp+20:
	ns = str(scb[elf[0]]+scb[elf[1]])
	for d in ns: # add new recipe scores
		scb.append(int(d))
		curr.append(int(d))
	ls+=len(ns)
	for i in [0,1]: # update elf positions
		elf[i]+=1+scb[elf[i]]
		elf[i]%=ls
	if t==-1: # check if has appeared
		while len(curr)>LL:
			if curr[:LL]==linp:
				t = ls-len(curr)
			curr = curr[1:]

print "part 1:", ''.join(map(str,scb[inp:inp+10])) # part 1
print "part 2:",t

