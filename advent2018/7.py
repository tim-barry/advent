
from collections import defaultdict
# from math import *

fn = "input.txt"
f=open(fn,'r')
r=f.read()
r=r.strip()
f.close()

test = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip()

#r = test

lines = r.split('\n')
l = [(s[5],s[-12]) for s in lines] # pairs of (before,after)
tl = sorted(set(sum(l,()))) # list of all steps
prereqs = defaultdict(list) # step:[prereqs...]
for b,a in l:
	prereqs[a].append(b)
ctime = defaultdict(int) # step: completion time

def add_candidates(cand,done):
	for step in tl:
		if step not in done and step not in cand: # don't double-count
			if all(pr in done for pr in prereqs[step]):
				cand.append(step)

def steptime(c,test=0):
	return ord(c)-64 + (test==0)*60

for part in [1,2]:
	cand = []
	done = ""
	wk = [0]*5 # workers (part 2)
	while len(done)<len(tl):
		add_candidates(cand,done)
		if part==1:
			cand.sort() # alphabetic sort (otherwise, prereq sort)
		step = cand.pop(0) # first candidate by time or prereqs
		done += step
		ctime[step]=max([min(wk)]+[ctime[pr] for pr in prereqs[step]]) + steptime(step)
		# total time: (available worker & all prereqs done) + step time
		wk[wk.index(min(wk))] = ctime[step] # update the worker who did it
	if part==1:
		print done
	if part==2:
		print max(ctime.values()) # completion time of last step

