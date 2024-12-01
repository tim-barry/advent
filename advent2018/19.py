#from collections import defaultdict,deque
import re

def extract_ints(a_string): # h/t day 10 /u/IGChris
    return map(int, re.findall(r'-?\d+', a_string))


fn = "input19.txt"
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

def simulate(program,ipreg,r0,DEBUG = True):
	regs = [0]*6
	ip = 0
	LP = len(program)
	while 0<=ip<LP:
		line = program[ip]
		regs[ipreg]=ip
		operation = line.split()
		regs = op(operation[0], regs, map(int,operation[1:])) # from day 16
		ip = regs[ipreg]+1
		if DEBUG and ip == 2: # look at what's going on
			print regs
	print "Final answer:", regs[0]

def pyf(N):
	tot = 0
	for x in xrange(1,N+1):
		if N%x==0:
			tot+=x
	return tot

data = r.strip()
program = data.split('\n')
ipreg = extract_ints(program[0])[0]
program = program[1:]

print "part 1 (simulation):"
simulate(program,ipreg,0)
print "part 1:", pyf(973)
print "part 2:", pyf( 973 + 10550400 )
"""
Python 2, #9/40. First part I just slightly modified the Day 16 code,
while for the second part I used some output from the first part
(the state of the registers at when the IP was 2) to figure out what was going on.
This problem was very similar to problem 23 from last year, which was a big help for me.
Embarrassingly, not only did I forget that the number itself was included in its factors,
I forgot that the part after the "jump if not 1" was *added* instead of assigned.
"""
