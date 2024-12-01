
fn = "input16.txt"
f=open(fn,'r')
r=f.read()
f.close()

test1="""
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
""".strip()
#r = test1

data = r.strip()
groups = data.split('\n\n')
program = groups[-1].split('\n')
groups = groups[:-2]


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

op_list = [set(opcodes) for i in range(len(opcodes))]

tot=0
for group in groups:
	before,operation,after = group.split('\n')
	before = eval(before[8:])
	operation = map(int,operation.split())
	after = eval(after[8:])
	t={c for c in opcodes if after==op(c,before[:],operation[1:])}
	op_list[operation[0]] &= t

nop = ["" for x in range(len(op_list))]
while not all(nop):
	for i,s in enumerate(op_list):
		if len(s)==1:
			nop[i]=s.pop()
			#print "operation",i,"is",nop[i]
			op_list = [s-set(nop) for s in op_list]

#print nop
op_list = nop
regs = [0]*4
for line in program:
	operation = map(int,line.split())
	regs = op(op_list[operation[0]], regs, operation[1:])

print "part 2:", regs[0]
#print "part 1:", tot
