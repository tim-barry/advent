"""
Descriptions

Day 1 - "inverse captcha"	(sum of next/halfway digits)
2 - "corruption checksum"
3 - "Spiral Memory"
4 - "High-entropy passphrases" (no duplicates or acronyms)
5 - "jump offsets"
6 - "memory reallocation"	(how many cycles)
7 - "Recursive Circus"		(balance tree with weight)
8 - "I heard you like Registers" (simulating)
9 - "Stream Processing"		(string processing)
10- "Knot Hash"
11- "Hex Ed"				(hex grid)
12- "Digital Plumber"		(graph search)
13- "Packet Scanners"		(modulus/Chinese Remainder)
14- "Disk Defragmentation"
15- "Dueling Generators"	(pseudorandom generators)
16- "Permutation Promenade"
17- "Spinlock"
18- "Duet"					(assembly/interpreting, multithreading?)
19- "A Series of Tubes"
20- "Particle Swarm"		(3D collisions, Manhattan distance)
21- "Fractal Art"
22- "Sporifica Virus"		(Langford's ant, infinite grid movement)
23- ""
24- ""
25- "" (Turing Machine simulation)

"""


tape = [0]
cursor = 0 # right: +1, left: -1
states = {
	'a':[[1,+1,'b'],[0,-1,'c']],
	'b':[[1,-1,'a'],[1,+1,'d']],
	'c':[[1,+1,'a'],[0,-1,'e']],
	'd':[[1,+1,'a'],[0,+1,'b']],
	'e':[[1,-1,'f'],[1,-1,'c']],
	'f':[[1,+1,'d'],[1,+1,'a']]
}

step_limit = 12173597
s = 'a'
for i in xrange(step_limit):
	tape[cursor],dc,s = states[s][tape[cursor]]
	#tape[cursor]=nv
	#s = ns
	cursor+=dc
	if cursor==-1:
		cursor=0
		tape.insert(0,0)
	elif cursor==len(tape):
		tape.append(0)

print sum(tape)

