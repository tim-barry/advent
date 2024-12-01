
from math import sqrt
from itertools import combinations

def product(l):
	r = 1
	for t in l:
		r*=t
	return r
prod = product
# ispalin = lambda s:all(s[i]==s[~i] for i in range(len(s)//2))

def gcd(a,b):
	if b==0: return a
	return gcd(b, a%b)

def lcm(a,b): return (a*b)//gcd(a,b)

""" Primes """
# from primes import prim

def checkpr(prime_list,candidate):
	sq_cand = sqrt(candidate)
	for p in prime_list:
		if p > sq_cand :
			break
		yield p

def nextpr(prime_list):
	candidate = prime_list[-1]+2
	while any(candidate%p==0 for p in checkpr(prime_list,candidate)): # while not isprime(candidate)
		candidate+=2
	prime_list.append(candidate)

def isprime(prime_list,x):
	#2018-06-11: replace 'not any ==0' with 'all'
	return all(x%p for p in checkpr(prime_list,x))


# 2019-07-30 rewrite
from itertools import takewhile
def isprime2(prime_list, x):
	return all(x%p for p in takewhile(sqrt(x).__ge__, prime_list))

def nextpr2(prime_list):
	candidate = prime_list[-1]+2
	while not isprime2(prime_list, candidate):
		candidate += 2
	prime_list.append(candidate)


""" Factorization """
def pfactors(n,prime_list):
	fac_list = []
	pr_i = 0
	while prime_list[pr_i]**2<=n:
		if n%prime_list[pr_i]==0:
			fac_list.append([])
			while n%prime_list[pr_i]==0:
				n/=prime_list[pr_i]
				fac_list[-1].append(prime_list[pr_i])
		pr_i+=1
	if n>1:
		i = ([f[0] for f in fac_list]+[n]).index(n)
		if i==len(fac_list):
			fac_list.append([n])
		else:
			fac_list[i].append(n)
	return fac_list

def pfactors_pe(n,prime_list): # O(log n)
	fac_list = []
	pr_i = 0
	while prime_list[pr_i]**2<=n: # need to reevaluate n each run
		if n%prime_list[pr_i]==0:
			fac_list.append([prime_list[pr_i],0])
			while n%prime_list[pr_i]==0:
				n/=prime_list[pr_i]
				fac_list[-1][1]+=1
		pr_i+=1
	if n>1:
		i = ([f[0] for f in fac_list]+[n]).index(n)
		# check if this factor's already in the list
		if i==len(fac_list): # not in the list
			fac_list.append([n,1])
		else:
			fac_list[i][1]+=1 # this shouldn't really happen
	return fac_list


def factor_count(n,prime_list):
	return prod([len(f)+1 for f in pfactors(n,prime_list)])

def pfactorsflat(n,prime_list):
	fac_list = []
	pr_i = 0
	while prime_list[pr_i]**2<=n:
		while n%prime_list[pr_i]==0:
			n/=prime_list[pr_i]
			fac_list.append(prime_list[pr_i])
		pr_i+=1
	if n>1:
		fac_list.append(n)
	return sorted(fac_list)

def all_factors(n,prime_list): # not including n itself
	pf = pfactorsflat(n,prime_list) # flatten
	return sorted(set(product(list(c)) for i in range(len(pf)) for c in combinations(pf,i)))

def all_factors_2(n):
	# 2018-06-11
	# O(sqrt(n) || n*sqrt(n))
	q=sqrt(n)
	i = 2
	l = [1]
	while i<=q:
		if n%i==0:
			l.append(i)
		i+=1
	if int(q)**2 == n: # square: don't count twice
		l.extend([n/x for x in l[-2::-1]])
	else:
		l.extend([n/x for x in l[::-1]])
	return l

def factor_sum(prime_list):
	def fsum(n):
		return sum(all_factors(n,prime_list))
	return fsum

""" Collatz sequence """
def collatz(n):
	if n%2==0:
		return n/2
	return n*3+1

collatz_d = {1:1}

def collatz_steps(n): # memoized
	if n not in collatz_d:
		collatz_d[n] = 1 + collatz_steps(collatz(n))
	return collatz_d[n]

""" Fibonacci sequence """
fibs = [0,1,1] # fib_1 = 1, fib_2 = 1
def nextfib(fib):
	fib.append(fib[-1]+fib[-2])
def genfibs(n):
	while len(fibs)-1<n:
		nextfib(fibs)


