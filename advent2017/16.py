
f=open("16.in",'r')
s=f.read().strip().split(",")
f.close()

def permutation_mul(a,b):
	# permute a with b
	return [a[i] for i in b]
	# new permutation should satisfy
	# [l[i] for i in new_p]
	# ==
	# nl=[l[i] for i in a]  # first permute with a,
	# [nl[i] for i in b]   # then with b
	# ==
	# [l[a[i]] for i in b]

def permutation_quickpow(p,n):
	if n==0:
		return range(len(p))
	elif n==1:
		return p
	t = permutation_quickpow(permutation_mul(p,p),n/2)
	if n%2:
		t = permutation_mul(t, p)
		# permutation_mul(p, t) # different? (consistency?)
		# since they're all p, it shouldn't matter.
	return t


name_swaps = range(16) # name_swaps[element] = element position
# swap ('a', 'b') --> name_swaps[a] is now what name_swaps[b] was, etc.
# eg if name_swaps[a=0] == b=1, then the 

perm = range(16)
swaps = [] # letter swaps: pA/B

for op in s: # generate a permutation
	if op[0]=="s":
		b = int(op[1:])
		perm = perm[-b:]+perm[:-b]
	elif op[0]=='x':
		A,B = map(int,op[1:].split('/'))
		perm[A],perm[B] = perm[B],perm[A]
	elif op[0]=='p': # leave all single-element swaps for last
		swaps.append(map("abcdefghijklmnop".index,op[1:].split('/')))
		A,B = map("abcdefghijklmnop".index,op[1:].split('/'))
		name_swaps[A],name_swaps[B] = name_swaps[B],name_swaps[A]

print perm

dancers = range(16)
iters = 1000000000%(15*14*13*12*3*11) # maximum cycle length (guess)
for t in xrange(iters):  # actually, 12 (max 60) for iters, and 2 for swaps
	dancers = [dancers[i] for i in perm] # permute
	for a,b in swaps: # unnecessary for even iters
		A = dancers.index(a)
		B = dancers.index(b)
		dancers[A],dancers[B] = dancers[B],dancers[A]
	if dancers==range(16): # cycle of length t+1
		print "cycle of ",t+1
		for t in xrange(iters%(t+1)):
			dancers = [dancers[i] for i in perm] # permute
		break

name_perm = map(name_swaps.index, range(16))
pow_perm = permutation_quickpow(perm, iters)
pow_name_perm = permutation_quickpow(name_perm, 10) # period of 10
print pow_name_perm
total = permutation_mul(pow_perm,pow_name_perm) # commutative

tostr = lambda p:"".join(["abcdefghijklmnop"[i] for i in p])
#for t in xrange(iters): # finally, swap the named elements
#	for a,b in swaps: # unnecessary for even iters
#		A = dancers.index(a)
#		B = dancers.index(b)
#		dancers[A],dancers[B] = dancers[B],dancers[A]

print tostr(total)
print tostr(dancers)


