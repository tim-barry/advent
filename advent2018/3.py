
fn = "input3.txt"
f=open(fn,'r')
r=f.read().strip()
f.close()
l = [(lambda p:(int(p[0][1:-1]),p[1][1:]))(s.split("@")) for s in r.split('\n')]

print l[0]

l = [[map(int,(lambda s:s[0].split(',')+s[1].split('x'))(s.split(": "))),i] for i,s in l]
l = [[s[0],s[1],s[0]+s[2],s[1]+s[3],i] for s,i in l]
print l[0]
print l[519]
l1 = sorted(l) # sorted by min x
l2 = sorted(l1,key=lambda x:x[2]) # max x
i1 = 0
i2 = 0
arr = [0]*1000
tot = 0

for x in xrange(0,1000): # part 1
	#add = []
	#sub = []
	while i1<len(l1) and l1[i1][0]==x:
		# add to scanarr
		#add+= l1[i1][1::2]
		y1,y2 = l1[i1][1::2]
		arr[y1:y2] = [t+1 for t in arr[y1:y2]]
		i1+=1
	while i2<len(l2) and l2[i2][2]==x:
		# add to scanarr
		#sub+= l2[i2][1::2]
		y1,y2 = l2[i2][1::2]
		arr[y1:y2] = [t-1 for t in arr[y1:y2]]
		i2+=1
	#scanarr.append( [add,sub] )
	tot+=sum(t>=2 for t in arr)
print tot

#part 2 - three different false starts before this sol
i1 = 0
i2 = 0
poss_list = set(zip(*l)[4])
arr = [list() for x in xrange(1000)]
for x in xrange(0,1000): # part 1
	while i1<len(l1) and l1[i1][0]==x:
		y1,y2 = l1[i1][1::2]
		arr[y1:y2] = [t+[l1[i1][4]] for t in arr[y1:y2]]
		i1+=1
	while i2<len(l2) and l2[i2][2]==x:
		y1,y2 = l2[i2][1::2]
		for y in range(y1,y2):
			arr[y].remove(l2[i2][4])
		i2+=1
	for yl in arr:
		if len(yl)>=2:
			for i in yl:
				if i in poss_list:
					poss_list.remove(i)
print poss_list

exit()	
