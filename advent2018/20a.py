from collections import defaultdict,deque
import re
def extract_ints(a_string): # h/t day 10 /u/IGChris
    return map(int, re.findall(r'-?\d+', a_string))


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

#r = ex3


def part1(s):
	# remove detours
	dups = ["NS","EW","SN","WE"]
	#rot = lambda s,i: s[i:] + s[:i]
	#dups+= [rot(dd,i) for dd in ["NESW","NWSE"] for i in range(4)]
	while any(dup in s for dup in dups):
		for dup in dups:
			s=s.replace(dup,"")
		while "||" in s:
			s=s.replace("||","|")
		s=s.replace("(|)","")
	LS = len(s)
	c1= s.find("(")
	l = [[0]]
	gi = [0]
	i = 0
	si = 0
	while i<LS:
		if s[i]=="(":
			l.append([0]) # group len
			gi.append(0)
			si+=1
		elif s[i]==")":
			si-=1
			gi.pop()
			l[si][gi[si]] += max(l.pop())
		elif s[i]=="|":
			l[si].append(0)
			gi[si]+=1
		else:
			l[si][gi[si]]+=1
		i+=1
	return max(l.pop())

regex = r.strip()
print "part 1:",part1(regex[1:-1])
