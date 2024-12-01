#(2024) moved input data (originally included as string)
s = open("6.in").read().strip().split()

l = map(int,s)

cycles = 0
prevs = []

while l not in prevs:
	prevs.append(l[:])
	m = max(l)
	i = l.index(m)
	l[i] = 0
	while m:
		i=(i+1)%len(l)
		l[i]+=1
		m-=1
	cycles+=1

print cycles
print len(prevs)-prevs.index(l)
