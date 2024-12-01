
def A_gen(a):
	while 1:
		a = (a*16807)% 2147483647
		if a&3==0:   # part 2
			yield a

def B_gen(a):
	while 1:
		a = (a*48271)% 2147483647
		if a&7==0:   # part 2
			yield a

A,B = A_gen(679), B_gen(771)
tot = 0
for i in xrange(5*1000000): # part 1: 40 million, part 2: 5 million
	if (next(A)&65535 == next(B)&65535):
		tot+=1
	if i%500000==0: #debug - every 1/2 million
		print i
print tot

