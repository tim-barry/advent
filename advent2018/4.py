from collections import defaultdict
# from math import *

#"""
fn = "input4.txt"
f=open(fn,'r')
r=f.read().strip()
f.close()
#"""

test = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""".strip()
#r = test
l = r.split('\n')
l = sorted(l)

#l = sorted(lines)
guards = defaultdict(lambda:[0 for x in range(60)])
for s in l:
	if s[25]=="#":
		g=s.split()[3]
	elif s[25]=="a":
		st=int(s[15:17])
	else: # wake up
		t=int(s[15:17])
		for x in range(st,t):
			guards[g][x]+=1

""" original algo
# part 1
g1 = sorted(guards.keys(), key=lambda g:-sum(guards[g]))[0]
# part 2
g2 = sorted(guards.keys(), key=lambda g:-max(guards[g]))[0]
"""
# h/t sciyoshi for max() with key
g1 = max(guards.keys(),key=lambda g:sum(guards[g]))
g2 = max(guards.keys(),key=lambda g:max(guards[g]))

for g in [g1,g2]:
	gh = guards[g]
	minute = gh.index(max(gh))
	print int(g[1:])*minute

