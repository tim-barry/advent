
# (2024) moved input data (originally included as string)
s = open("10.in").read().strip() #.split(',')

#s = "1,2,4"


s = map(ord,s) + [17, 31, 73, 47, 23]
i = 0
l = range(256)
skipsize = 0

startpos = 0
currpos = 0

#def reverse(l, t, i): #i=curr, t=length
#	

#print l

for junk in range(64):
	for t in s:
		#reverse(l, t, i)
		l[:t] = l[:t][::-1]
		i = (t+skipsize)%len(l) # <- need to mod
		skipsize+=1
		skipsize%=len(l)
		
		l = l[i:] + l[:i]  # move currpos to front
		currpos+=i
		currpos%=len(l)

l = l[-currpos:] + l[:-currpos]

dense_hash = []
for x in range(16):
	dense_hash.append(reduce(lambda a,b:a^b, l[x*16:x*16+16]))

print ''.join(["%02x"%x for x in dense_hash]) # <- "%02x" -- keep leading 0's
#print l[-currpos], l[1-currpos], '->' , l[-currpos] * l[1-currpos]


