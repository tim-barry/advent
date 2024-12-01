#(2024) moved input data (originally included as multiline string)
s=open("5.in").read().strip().split()

l=map(int,s)

# this takes a long time in python for part 2
# (especially since i originally did it inefficiently)
# which probably cost me a spot on the leaderboard for part 2
# ( over 40s waiting for part 2 output --> rank 113 )

# however, I was able to code it very quickly -> 29th for part 1.

# I can't see any shortcuts to solving the problem

i = 0
tot=0
lee = len(l)
while 0<=i<lee:
	if l[i]>=3: # part 2
		l[i]-=1
		i+=l[i]+1
	else:       # part 1
		l[i]+=1
		i+=l[i]-1
	tot+=1



print tot
