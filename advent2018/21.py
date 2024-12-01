#from collections import defaultdict,deque
import re

def extract_ints(a_string): # h/t day 10 /u/IGChris
    return map(int, re.findall(r'-?\d+', a_string))


fn = "input21.txt"
f=open(fn,'r')
r=f.read()
f.close()
"""
#r = test

lines = r.strip().split('\n')
"""


def op(code,regs,args):
	a,b,c = args
	if code[:3] in ["add","mul","bor","ban"]:
		a = regs[a]
		if code[3]=="r":
			b = regs[b]
	elif code[:3]=="set" and code[3]=="r":
		a = regs[a]
	elif code[:2] in ['gt','eq']:
		if code[2]=='r':
			a = regs[a]
		if code[3]=='r':
			b = regs[b]
	code = code[:3]
	if code=="add":
		val=a+b
	elif code=="mul":
		val=a*b
	elif code=="bor":
		val=a|b
	elif code=="ban":
		val=a&b
	elif code=="set":
		val = a
	elif code[:2]=="gt":
		val = a>b
	elif code[:2]=="eq":
		val = a==b
	nr = regs[:]
	nr[c] = val
	return nr


opcodes = [
"addr","addi","mulr","muli","borr","bori","banr","bani",
"setr","seti","gtir","gtri","gtrr","eqir","eqri","eqrr"
]

def simulate(program,ipreg,r0):
	regs = [0]*6
	regs[0]=r0
	ip = 0
	LP = len(program)
	count=0
	p_reg=0
	seen = set()
	while 0<=ip<LP:
		line = program[ip]
		regs[ipreg]=ip
		operation = line.split()
		regs = op(operation[0], regs, map(int,operation[1:])) # from day 16
		ip = regs[ipreg]+1
		#if ip == 7: # look at what's going on
		#	#return 0
		if ip==28:
			print regs
			if regs[5] in seen:
				return p_reg
			seen|={regs[5]}
			p_reg = regs[5]
		#if count>STEPS>0:
		#	break
	return r0
	print "Final answer:", regs[0]

# following just python code of algorithm
# based on comment that there will be a cycle
# (found after ~10,000 length)
def pyf():
	r = [0]*6
	last=-1
	seen=set()
	flag8=0
	while 1:
		if not flag8:
			r[3] = r[5]|65536
			r[5] = 521363
		r[4] = r[3] & 0xff
		r[5]+= r[4]
		r[5]&= 0xffffff
		r[5]*= 65899
		r[5]&= 0xffffff
		if r[3]<256:
			if not seen:
				print r[5]
			if r[5] in seen:
				print last
				return
			else:
				last = r[5]
				seen|={last}
				flag8=0
				continue
		r[4] =0
		flag18=1
		# r[3] = r[3]//256
		while flag18: # (r[4]+1)*256 <= r[3]:
			r[2] = r[4]+1
			r[2]*= 256
			if r[2]>r[3]:
				r[3] = r[4]
				flag8=1
				break
			r[4]+=1

data = r.strip()
program = data.split('\n')
ipreg = extract_ints(program[0])[0]
program = program[1:]

#t=simulate(program,ipreg,0)
pyf()
