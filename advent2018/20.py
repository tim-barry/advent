"""
I'm particularly proud of this solution-
although I initially tried a different solution (memoryless: 20a.py),
I had a hard time with it (since I forgot about detours)
and it didn't work for part 2.
I had already been thinking of creating the map of the facility,
but was having problems. I came back the next day and totally rewrote it
from scratch (and got it right this time).
"""

fn = "input20.txt"
f=open(fn,'r')
r=f.read()
f.close()

ex1 = "^WNE$"
ex2 = "^ENWWW(NEEE|SSE(EE|N))$"
ex3 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"

test1="""
^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
"""
test2="""
^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
"""

redd1="^" + "(N|S|E|W)"*93 + "$"

#r = redd1
data=r

from collections import defaultdict
# input in 'data'

def go_through_door(grid,p1,d):
	# compute next position from p1 in direction d
	if d=="N":
		p2 = (p1[0],p1[1]-1)
		d = 0
	elif d=="E":
		p2 = (p1[0]+1,p1[1])
		d = 1
	elif d=="S":
		p2 = (p1[0],p1[1]+1)
		d=2
	elif d=="W":
		p2 = (p1[0]-1,p1[1])
		d=3
	# make a door in the grid
	grid[p1][d] = p2
	grid[p2][2^d] = p1
	return p2

def map_facility(s,grid):
	# Create a map of the facility
	currpos = [(0,0)] # queue of starting positions
	group_end_positions = []
	group_start_positions = []
	gep = [] # stack of group end positions
	gsp = [] # stack of group start positions
	for c in s:
		if c=="(":
			# push group start and end positions
			gep.append(group_end_positions)
			gsp.append(group_start_positions)
			#save current positions as group start positions
			group_start_positions = currpos[:]
			group_end_positions = []
		elif c==")":
			# save current positions as group end positions, like |
			group_end_positions.extend(currpos)
			# set current positions to group end positions
			currpos = list(set(group_end_positions)) # remove duplicates
			# pop group start and end positions
			group_end_positions = gep.pop()
			group_start_positions = gsp.pop()
		elif c=="|":
			# save current positions as group end positions
			group_end_positions.extend(currpos)
			# reset current positions to group start positions
			currpos = group_start_positions[:]
		else:
			# update current positions
			for ti in range(len(currpos)):
				currpos[ti] = go_through_door(grid,currpos[ti],c)

def findlongestpath(grid, LIM=1000): # BFS
	q = [ (0,0) ]
	dist=0
	visited = defaultdict(int)
	visited[(0,0)] = 1
	tot=0
	while q:
		nq = []
		for p in q:
			if dist>=LIM:
				tot+=1
			for x in grid[p]: # adjacent
				if x and not visited[x]:
					visited[x]=1
					nq.append(x)
		q = nq
		dist+=1
	return (dist-1,tot)

regex = data[data.find("^")+1:data.rfind("$")]
facility = defaultdict(lambda:[()]*4)
# N,E,S,W: empty tuple if no door in that direction,
# position (E,S) of room in that direction if there is a door

map_facility(regex, facility)
result = findlongestpath(facility)
print "part 1:",result[0]
print "part 2:",result[1]

"""20g.py: golfed away code:
First step: remove comments, set variable names to 1 character
optimize 'defaultdict' import: use 'as'
optimize input (oneline) (file vs raw_input())
remove unnecessary args from functions (inherit global scope)
inline functions (map_facility/`M` and findlongestpath/`f`)
optimize direction picking in go_through_door/`o`:
(1) make list, use "NESW".find and index into list of position diffs
(2) use binary tricks to directly calculate position (switch to NWSE to accommodate)
switch defaultdict to set instead of lambda:[()]*4
switch to operations like += instead of .append or .extend

def o(P,d):t=d>>1 or-1;n=(P[0]+(~d&1)*t,P[1]+(d&1)*t);g[P]|={n};g[n]|={P};return n
			p[i]=o(p[i],"NWSE".find(c))
(function was inlined)

golfed size: 557 (with raw_input), 576 (open "input20.txt")
-> 540/559 by removing whitespace in if/elif
-> copied p to q (`q=p[:]` instead of `q=[(0,0)]`)
-> changed print statement (removed %formats), now 535/554
-> trimmed import by 1 char, removing 'from'
-> trimmed 6 chars by putting s,e on S,E stacks instead of separate

old code:
e,s,E,S=[],[],[],[]									# saved 6 (-6) 
for c in r:
	if"("==c:S+=[s];E+=[e];s,e=p[:],[]				# saved 8 (-8)
	elif")"==c:p,s,e=list(set(e+p)),S.pop(),E.pop()	# ==
	elif"|"==c:e+=p;p=s[:]							# lost 8  (+8)
	else:											# ==
		for i in range(len(p)):d="NWSE".find(c);P=p[i];t=d>>1 or-1;n=(P[0]+(~d&1)*t,P[1]+(d&1)*t);g[P]|={n};g[n]|={P};p[i]=n

-> saved 2 chars by assigning 2 ints t=d=0 at same time
-> saved 12 chars by using p as set. (swapped P and p). (Lin/raw: 492 )

old code:
p=q[:]												# + 2
S,E=[[]],[[]]										# + 10
for c in r:
	if"("==c:S+=[p[:]];E+=[[]]						# ==
	elif")"==c:p=list(set(E[-1]+p));S.pop();E.pop()	# - 18 (51->33)
	elif"|"==c:E[-1]+=p;p=S[-1][:]					# - 1  (34->33)
	else:											# - 19 (124 ->105); +8 +6 (2 lines)
		for i in range(len(p)):d="NWSE".find(c);P=p[i];t=d>>1 or-1;n=(P[0]+(~d&1)*t,P[1]+(d&1)*t);g[P]|={n};g[n]|={P};p[i]=n

The new code uses O as an empty set and |'s everything (even itself)
with O to create copies instead of slicing: P[:] -> P|O ; [] -> O|O
this allows removing the list(set(P)). Also, removes the range(len),
instead directly iterating through P.

-> saved 2 chars by setting O=P-P instead of set().
-> saved 6 chars, lost 2 chars (-4 total) by removing O (Lin/raw: 486)
Now all empty sets are created with P-P; full sets with P|P.
-> saved 1 char by replacing `P=S[-1]-{1}` with `P^=P^S[-1]` (485)
(still 1c worse than `P=S[-1]|O` but O not worth it anymore)
-> replace 'g' with 'M' (no code change)
-> let `q` be a set too (-3 init P, +1 `v[q[0]]=-1`, +1 `n=[]`) (484)
-> removed .strip() from both inputs. (-8 chars) (476)
-> rename n->N, x->n (no code change)
-> remove unnecessary old test (if` x and`...) (-6 chars) (470)
-> save 9 chars (93->84) by using set comprehension and then update: (461)

while q: (old code:)
	N=q-qd+=1;t+=(d>1000)*len(q)
	for p in q:
		for n in M[p]:
			if~v[n]:v[n]=-1;N|={n}
	q=N

-> save 3 chars by replacing '==' character comparisons with '>'
-> save 1 char by replacing 'd>>1' with 'd>1'   (457)
Golfed 100 chars from initial golfing!

-> -14 +2 : iterate through copy of P and update in-place with ^=  (445)
(possible issue if next `n` can come from even number of sources?)
(symmetric difference may result in deleting entries if added twice)
NO: can prove correctness.
Only way to not have new position in final set:
if new position reachable from even number of old positions.
BUT: since all positions are moving in the same direction,
any position is only reachable from exactly 1 other position.
Only place this may occur, when E/S updated, uses | (unchanged).

old code:
		N=P-P
		for p in P:d="NWSE".find(c);t=d>1 or-1;n=(p[0]+(~d&1)*t,p[1]+(d&1)*t);M[p]|={n};M[n]|={p};N|={n}
		P=N
new code:
		for p in P|P:d="NWSE".find(c);t=d>1 or-1;n=(p[0]+(~d&1)*t,p[1]+(d&1)*t);M[p]|={n};M[n]|={p};P^={n,p}
(test cases weren't working because i forgot to [1:-1]

-> -1 by replacing `t=d>1 or-1` with `t=(d&2)-1` (need brackets for precedence)
-> -1 by removing "N" from "NESW" (now [-1,2] instead of [0,3])  (443)
-> -1 by brute-force searching through expressions for t (now `d*d+~d`)
old code:
		for p in P|P:d="WSE".find(c);t=(d&2)-1;n=(p[0]+(~d&1)*t,p[1]+(d&1)*t);M[p]|={n};M[n]|={p};P^={n,p}

-> -12 by removing t entirely, using brute-force expression search
directly for the position diffs. (430)
old code: (as above, but with `t=d*d+~d`)

-> -2 by removing brackets around n assignment (tuple automatically created)

-> -9 by merging S and E stacks (assignment & appending) (419)
old code: (other lines unchanged except S<->E and -1:-2 in if"z"
S,E=[P-P],[P-P]						# -> S=[P-P,P-P]
	if")">c:S+=[P|P];E+=[P-P]		# -> S+=[P|P,P-P]

-> -1 replacing ' d-1' with '~-d' in final print statement (whitespace) (418 ?)

-> -36 (?) changing v to set of visited position instead of defaultdict (382? X)
old code: (112 -> 76)
v=D(int)
v[(0,0)]=-1
while q:
 d+=1;t+=(d>1000)*len(q);q={n for p in q for n in M[p]if~v[n]}
 for n in q:v[n]=-1

-> -4 now that there's only one D(), we don't need to assign it; (378? X)
instead directly use C.defaultdict (replace `D=C.defaultdict;M=D(set)`)

-> -16 (+12 +12 -16 -24 ) using M={} instead of defaultdict; M.get()  (362? X)
old code:
import collections as C
M=C.defaultdict(set)
		for p in P|P:d="WSE".find(c);n=p[0]+d%2*d,p[1]+~(d|-d);M[p]|={n};M[n]|={p};P^={n,p}

-> move M, rename q:Q, v:V, r:R, use Q-Q instead of P-P (faster??)
-> -1 remove trailing semicolon from while Q   (**363**)
-> use "NES" instead of "WSE" (now x,y/E,S instead of y,x)
-> -3 by using "EWS" (computed better golf for d/t) (360)
...d="NES".find(c);n=p[0]+d%2*d,p[1]+~(d|-d)		#old code
...d="EWS".find(c);n=p[0]+d/2,p[1]+1--d%3			#new code

-> -3 (+9 -12) by ensuring M[p] always exists: remove get() (**357**)
new: M={(0,0):Q-Q}

decided not to replace S with tuple: can't |= assign
(using '.update' works but loses more than gained from brackets[4]/pop removal[1])

decided not to replace M.get with something else (looks optimal)
M[n]=M.get(n,P-P)|{p}
M[n]=n in M and{p}|M[n]or{p} 

-> -2 (+6 -4 -4) by creating new local variable `t=0,0` (**355**)
-> -7 by removing S initialization, now `S=[]` (**348**)

decided not to put P in S (no character gain, incredibly slow)

-> -23 (-6 -13 -4) by using complex numbers instead of tuples (from reddit day20) (**325**)
save 6 by not assigning t=0,0 ; 13 in generating new positions
(reorder "EWS"->"ESW"); remove d since it's now only used once (-4)
old code:
		for p in P|P:d="EWS".find(c);n=p[0]+d/2,p[1]+1--d%3;M[p]|={n};M[n]=M.get(n,P-P)|{p};P^={n,p}

-> -1 by replacing '1000' with '1e3' (**324**)

decided not to use `Q=reduce(set.__or__,[M[p]for p in Q])-V`	(+7,correct)
decided not to use `Q=eval('|'.join(`M[p]`for p in Q))-V`		(+4,correct)

-> -1 by not keeping track of distance and total (d,t), (**323**)
but rather keeping a list of len(Q) (use S since it's empty.)
old code:
d=t=0
while Q:d+=1;t+=(d>1e3)*len(Q);Q={n for p in Q for n in M[p]}-V;V|=Q
print~-d,"\n",t

-> -3 (-2 -1) by removing [] when adding to S (**320**)

Linux line endings brings down to **320** bytes.
-> -4 (moving raw_input directly to loop variable)
-> -3 (removing P|= on if"*": not all input)
	elif"*">c:P|=S.pop();S.pop() -> :S.pop();S.pop()


basic Algo by /u/betaveros (seen after got 320 chars): (no read)
D={0:0}
p=0
S=[]
for c in R:
	if")">c:S+=p,
	elif"*">c:S.pop()
	elif"z"<c:p=S[-1]
	else:n=p;p+=1j**"ESW".find(c);D[p]=min(D.get(p,1e8),D[n]+1)
v=D.values()
print max(v),"\n",sum(x>999for x in v)


testing:

ex1 = "^WNE$"
# 3
ex2 = "^ENWWW(NEEE|SSE(EE|N))$"
# 10
ex3 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
# 18

test1="^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
# 23
test2="^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"
# 31

redd1="^" + "(N|S|E|W)"*90 + "$"
# 90
my1 = "^(S|E)(S|E)$"

r = [1:-1]


"""
