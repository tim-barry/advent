#(2024) moved input data (originally included as multiline string)
s = open("13.in").read().strip()

d = eval("{"+s.replace('\n',',')+"}")

"""
f=open("13.in",'r')
s=f.read().strip().split("\n")
f.close()
#"""

#pos = 0
delay = 0
while 1:
	tot_sev = 0
	was_caught = 0
	#for k in d.keys():
	#	d[k][1:] = [0,1]
	#for t in range(delay):
	#	for k in d.keys():
	#		if d[k][1]==d[k][0]-1: # if at end
	#			d[k][2]=-1 # turn around
	#		elif d[k][1]==0: #if at start
	#			d[k][2]=1 #turn around
	#		d[k][1]+=d[k][2] #move
	for depth in d.keys():
		if (depth+delay)%(d[depth]*2-2)==0:
			sev = depth*d[depth]
			tot_sev += sev
			was_caught = 1
			#break
		#for k in d.keys():
		#	if d[k][1]==d[k][0]-1:
		#		d[k][2]=-1
		#	elif d[k][1]==0:
		#		d[k][2]=1
		#	d[k][1]+=d[k][2]
	#else:
	if not was_caught:
		break
	delay+=1
	#if delay%10000==0:
	#	print delay
	break

print "part 1:",tot_sev

print "part 2:",
""" Better Part 2 solution """
def gcd(a,b):
	if a>b:
		if a%b==0:
			return b
		return gcd(b,a%b)
	if b%a==0:
		return a
	return gcd(a,b%a)

#delay+depth =/= 0 (mod d[depth]*2-2)
# sieve via Chinese Rem Theorem?
from collections import defaultdict

# d is {depth:range}, eg:
d = eval("{"+s.strip().replace('\n',',')+"}")

neq = defaultdict(list) # of the form {b:[a1,a2...]} where delay != a_i (mod b)
for depth in d.keys():
	neq[d[depth]*2-2] +=  [(-depth)%(d[depth]*2-2)]
moduli = sorted(neq.keys()) # moduli

"""for m in moduli:
	print m,":",sorted(set(range(0,m,2))-set(neq[m])) #"""

prev_lcm=1
lcm = 1
residues = [0] #mod 1
tot = 1 # == len(residues)
for m in moduli:
	g = gcd(m,lcm) # simple Euclidean algorithm
	prev_lcm = lcm
	lcm = lcm*m/g  #new modulus
	residues = [x for x in
		sum([range(i,lcm,prev_lcm) for i in residues],[])
		if x%m not in neq[m]]
	tot *= (m/g - len(neq[m]))
	print "residues now:",len(residues)
	print "total now:", tot

print sorted(residues)[0], "(mod",lcm,")" # the smallest residue
print len(residues) , "residues"
print len(moduli) , "moduli"
print reduce(lambda a,b:a*b, [len(neq[m]) for m in moduli]), "is the product of neq[m]"

#print tot_sev
#print delay # 3823370
