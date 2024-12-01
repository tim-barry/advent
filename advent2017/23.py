from collections import defaultdict


with open("23.in",'r') as f:
	instr=[line.split() for line in f.read().strip().split("\n")]

i = 0
tot = 0

d = defaultdict(int)

def get(s):
	try:
		return int(s)
	except:
		return d[s]
	#if s in "qwertyuiopasdfghjklzxcvbnm":
	#	return d[s]
	#return int(s)

d["a"]=0 # nope

while 0<=i<len(instr):
	if instr[i][0]=="snd": # send
		#if pr==1: # count how many times program 1 sends
		#	tot+=1
		snd[pr].append(get(instr[i][1]))
		#print "program",pr,"sending",instr[i][1],"(",get(instr[i][1]),")"
	elif instr[i][0]=="set":
		d[instr[i][1]] = get(instr[i][2])
	elif instr[i][0]=="add":
		d[instr[i][1]] += get(instr[i][2])
	elif instr[i][0]=="sub":
		d[instr[i][1]] -= get(instr[i][2])
	elif instr[i][0]=="mul":
		tot+=1
		d[instr[i][1]] *= get(instr[i][2])
	elif instr[i][0]=="mod":
		d[instr[i][1]] %= get(instr[i][2])
	elif instr[i][0]=="rcv":
		if snd[1-pr]: # other program has sent data
			state[pr] = "ok"
			d[instr[i][1]] = snd[1-pr].pop(0) # get data
		else: # wait: switch to other prog
			if state[1-pr]=="done":
				break # will never recv: deadlock
			if len(snd[pr])==0 and state[1-pr]=="r":
				break # this one hasn't sent anything, other is recving: deadlock
			ind[pr] = i   # save instruction index
			state[pr]="r" # save state
			print snd[pr][:10]
			pr = 1 - pr   # change program
			i = ind[pr]-1 # (will be incremented back)
			print "{",' '.join(["%s:%d"%(k,d[k]) for k in sorted(d.keys())]),"}"
			d = ds[pr]    # change registers
	elif instr[i][0]=="jnz":
		if get(instr[i][1]) != 0:
			i+=get(instr[i][2])-1
	i+=1
	print "{",
	for k in d.keys():
		print k,":",d[k],
	print "}"
	raw_input()


print d["h"]

