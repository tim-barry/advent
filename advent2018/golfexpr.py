
import itertools as it
cr = it.combinations_with_replacement
p = lambda t:(''.join(s) for s in set(it.permutations(t)))

L1 = [1,0,-1,0] # best 6: d%2*-d / d%-2*d / -d&d-2
L2 = [0,1,0,-1] # best 7: d-3&1-d
L3 = [-1,0,1,0] # best 5: d%2*d
L4 = [0,-1,0,1] # best 6(7): ~d&~-d / ~d&d-1, using ~(d|-d) because it already has parens

L1 = [1,-1,0,0] # best 7: d/2^~-d / -d^~d/2 / d/2^d-1
L2 = [-1,1,0,0] # best 7: d^d/2+1 / d^1+d/2
L3 = [0,0,1,-1]
L4 = [0,0,-1,1]

L1 = [0,1,-1,0] # best 6: 1--d%3 / 1+d%-3 / d%~2+1
L2 = [1,0,0,-1] # best 5: 0-d/2
L3 = [-1,0,0,1] # best 3: d/2
L4 = [0,-1,1,0] # best 6: -d%3-1

Ls = [L1,L2,L3,L4]
chars = " d&^|~()-+*/%<>012345"
max_expr_len = 7
m=[max_expr_len+1]*4
best=[['_'*max_expr_len] for _t in range(4)]
pspc = -1
for t in cr(chars,max_expr_len):
	spc = t.count(" ")
	#if spc==0: # combinations are ordered: no more will contain spaces
	#	break
	if spc!=pspc:
		if all(_m<max_expr_len+1 for _m in m): # found best for all
			break
		print "now considering expressions of length",max_expr_len-spc
	pspc=spc
	if 'd' in t and t.count("(")==t.count(")")<2 and len([x for x in t if x in '012345'])<3:
		for s in p([c for c in t if c!=' ']):
			if s.find("(")<=s.find(")"):
				try:
					La = [eval(s) for d in range(-1,3)]
					#La = [eval(s) for d in range(4)] # not as good
					for i,L in enumerate(Ls):
						if La==L:
							x=len(s)
							if x<m[i]:
								best[i]=[s]
								m[i]=x
							elif x==m[i]:
								best[i].append(s)
							print s,"L%d"%(i+1)," ",
							for i,L in enumerate(Ls):
								print "L%d best(%d): %s "%(i+1,m[i],best[i][0]),
							print ''
				except KeyboardInterrupt:
					print ''
					for i,L in enumerate(Ls):
						print "best for L%d:"%(i+1)
						for s in best[i]:
							print s
						print ''
					print ''
					raise
				except:
					pass
print ''
for i,L in enumerate(Ls):
	print "best for L%d:"%(i+1)
	for s in best[i]:
		print s
	print ''

