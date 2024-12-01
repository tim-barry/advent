from collections import defaultdict,deque

#"""
fn = "input24.txt"
f=open(fn,'r')
r=f.read()
f.close()

test1="""
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
"""

#r=test1
DEBUG=0

r=r.strip()
lines=r.split('\n')
#"""

# units, hitpoints, weaklist, immunelist, atkdam,atktype, initiative
def parse_group(line):
	w = line.replace("; ",") (").split()
	units = int(w[0])
	HP = int(w[4])
	weaklist = []
	if "(weak" in w:
		i=w.index("(weak")+2
		while w[i][-1]==",":
			weaklist.append(w[i][:-1])
			i+=1
		weaklist.append(w[i][:-1])
	immunelist = []
	if "(immune" in w:
		i=w.index("(immune")+2
		while w[i][-1]==",":
			immunelist.append(w[i][:-1])
			i+=1
		immunelist.append(w[i][:-1])
	try:
		d = w.index("damage")
	except:
		print w
		raise
	atkdam = int(w[d-2])
	atktype = w[d-1]
	initiative = int(w[-1])
	effective_power = atkdam * units
	group=[effective_power,initiative,units,HP,weaklist,immunelist,atkdam,atktype,]
	return group

# eff_power, init, units, hitpoints, weaklist, immunelist, atkdam,atktype
#  0			1	2		3			4		5			6		7

i = lines.index('') # empty line
immune_groups = map(parse_group,lines[1:i])
infect_groups = map(parse_group,lines[i+2:])

# team
for group in immune_groups:
	group.append(1)
for group in infect_groups:
	group.append(0)


orig_groups = immune_groups+infect_groups

def naive_damage(g1,g2):
	try:
		# if g2 weak to g1:
		if g1[7] in g2[4]: # weak: double
			return g1[0]*2
		elif g1[7] in g2[5]: # immune: zero
			return 0
		# no bonuses:
		return g1[0]
	except:
		print g1
		print g2
		raise

def receive_damage(group,dam):
	# 10 units 10 hp each 75 dam: -7 (75//HP) units
	group[2]-= dam//group[3]
	group[0]=group[2]*group[6]

def select_target(g1,groups,targeted):
	valid_targets = [g for i,g in enumerate(groups) if g[-1]!=g1[-1] and not targeted[i]]
	if not valid_targets:
		return None
	best = max(valid_targets, key=lambda g:(naive_damage(g1,g),g))
	if naive_damage(g1,best)==0: # can't do any damage (all immune)
		return None
	if DEBUG:
		print "would deal",naive_damage(g1,best),"damage"
	targeted[groups.index(best)]=1
	return best

# eff_power, init, units, hitpoints, weaklist, immunelist, atkdam,atktype, immune?
#  0			1	2		3			4		5			6		7

boost = 30
#db=2**20
while 1:
	all_groups = [g[:]for g in orig_groups]
	for g in all_groups:
		if g[-1]: # immune
			g[6]+=boost # increase attack power
			g[0]=g[6]*g[2] # recalc effective power
	done=0
	while not done:
		assert all(g[2]>0 for g in all_groups)
		#select targets
		target_select = sorted(all_groups,reverse=True) #target selection order
		targeted = [0]*len(all_groups)
		targets=[]
		for group in target_select:
			if DEBUG:
				print `group`
			#if group[2]>0: # positive HP
			targets.append(select_target(group,all_groups,targeted))
		if DEBUG:
			print ''
		# attack
		remove_list = []
		cont=0
		for group,target in sorted(zip(target_select,targets),key=lambda(g,t):-g[1]):
			# decreasing initiative
			if group[2]>0 and target is not None: # dead units can't attack
				# deal damage to target
				dam = naive_damage(group,target)
				if group[-1]: # an immune group did damage
					cont=1
				if DEBUG:
					L = [["infect",infect_groups],["immune",immune_groups]]
					gname,ig = L[group[-1]]
					tname,it = L[1-group[-1]]
					print gname,"group",1+ig.index(group),"attacks",
					print tname,"group",1+it.index(target),"for",dam,"damage",
					print "killing",dam//target[3],"units"
					u1 = target[2]
				receive_damage(target,dam)
				#u2 = target[2]
				#print "actual loss:",u2-u1,"units"
				# if died
				if target[2]<=0:
					remove_list.append(target)
		if not cont: # no immune groups will do any more damage
			done=1
		if DEBUG:
			print "\n"
		for r in remove_list:
			all_groups.remove(r)
		teams = zip(*all_groups)[-1]
		print len(all_groups),"groups left:",sum(teams),"immune"
		if len(teams)-sum(teams)==1:
			for group in all_groups:
				print group
		done = (not any(teams)) or (all(teams)) # all same
	# we want immune left alive
	if all(teams):
		break
		if db==0:
			break
		boost-=db
		db/=2
	else:
		boost+=1
		print boost
		continue
		if db==0:
			boost+=1
		boost+=db
		db/=2
	print boost,db
print "part 2:", sum(g[2] for g in all_groups) # total units

# 6614 is too low
