
#(2024) moved input data (originally included as direct int)
step = eval(open("17.in").read().strip())

# part 1
i = 0
buf = [0]
for t in xrange(1,2017+1):
	i = (i+step)%len(buf) + 1
	buf[i:i] = [t] # couldn't remember .insert() syntax
print buf[i-5:i+5]

# part 2
i = 0
for t in xrange(1,50000000+1):
	i = (i+step)%t + 1
	if i==1:
		val_after_0 = t
print val_after_0

