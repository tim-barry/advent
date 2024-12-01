
f=open("11.in",'r')
s=f.read().strip().split(",")
f.close()


pos = [0,0,0]
maxd = 0
for t in s:
	if t=="n":
		pos[0]+=1
	elif t=="s":
		pos[0]-=1
	elif t=="nw":
		pos[1]+=1
	elif t=="se":
		pos[1]-=1
	elif t=="ne":
		pos[2]+=1
	elif t=="sw":
		pos[2]-=1
	t = map(abs,pos)
	d = sum(t) - min(t)
	if d>maxd:
		maxd = d

print d    #part 1
print maxd #part 2
