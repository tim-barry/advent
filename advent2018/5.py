
# from collections import defaultdict
# from math import *

fn = "input.txt"
f=open(fn,'r')
r=f.read()
#print len(r)
r=r.strip()
#print len(r)
f.close()

# stack-based solution (like parenthesis matching)
# significantly faster, but original solution is the commented one.
def reactlen(s):
	stk = []
	for c in s:
		if stk and c==stk[-1].swapcase():
			stk.pop(-1)
		else:
			stk.append(c)
	return len(stk)

#part 1 - r is the input
r1 = r
"""
l1 = len(r1)
l2 = l1+1
while l1!=l2:
	l2 = l1
	for c in "qwertyuiopasdfghjklzxcvbnm":
		r1 = r1.replace(c+c.upper(),"").replace(c.upper()+c,"")
	l1 = len(r1)
print l1
"""
print reactlen(r1)

# part 2 - takes ~5 seconds with Pypy 2 on my machine
m = 100000000
for _c in "qwertyuiopasdfghjklzxcvbnm":
	r2 = r.replace(_c,"").replace(_c.upper(),"")
	# h/t /u/dark_terrax: can use r1 instead of r
	i = reactlen(r2)
	if i<m:
		m = i
	"""
	l1 = len(r2)
	l2 = l1+1
	while l1!=l2:
		l2 = l1
		for c in "qwertyuiopasdfghjklzxcvbnm":
			r2 = r2.replace(c+c.upper(),"").replace(c.upper()+c,"")
		l1 = len(r2)
	if l1 < m:
		m = l1 #"""
print m
