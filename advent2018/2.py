
fn = "input2.txt"
f=open(fn,'r')
r=f.read().strip()
f.close()
l = r.split()

t2=t3=0 # part 1
for s in l:
	if any(s.count(c)==2 for c in set(s)):
		t2+=1
	if any(s.count(c)==3 for c in set(s)):
		t3+=1
print t2*t3 # part 1

for a in l: # part 2
	for b in l:
		if sum([c1!=c2 for c1,c2 in zip(a,b)])==1:
			print ''.join([c1 for c1,c2 in zip(a,b) if c1==c2])

