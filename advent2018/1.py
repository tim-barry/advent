
s = "input1.txt"
f=open(s,'r')
r=f.read().split()

l= [int(s.strip()) for s in r if s.strip()]

print sum(l) # part 1

s = [0]
i = 0
t = 0
while 1:
	t = t+l[i%len(l)]
	if t in s:
		break
	i+=1
	s.append(t)

print t # part 2

