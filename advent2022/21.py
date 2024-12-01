
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input21.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

def mint(b):
    try:
        return int(b)
    except:
        return b.replace('/','//').split()

monkeys = {a:mint(b) for line in lines
            for a,b in [line.split(": ")] }

# print(monkeys['root'])

def ok(monkeys, key):
    return key in monkeys and type(monkeys[key]) is int

#part 2
del monkeys['humn']

changed = 1
while changed:
    changed = 0
    for k,v in list(monkeys.items()):
        if type(v) is int:continue
        if ok(monkeys,v[0]) and ok(monkeys, v[2]):
            changed = 1
            monkeys[k] = eval(f"{monkeys[v[0]]}{v[1]}{monkeys[v[2]]}")

#part 1:
#print(monkeys['root'])

div = lambda x,y:x//y
mul = lambda x,y:x*y
add = lambda x,y:x+y
sub = lambda x,y:x-y

def normal_inv(op):
    if op=="*": return div
    if op=="//": return mul
    if op=="-": return add
    if op=="+": return sub

def alt_inv(op):
    if op=="//": raise Exception("unexpected")
    if op=="-": return lambda x,y: y-x
    return normal_inv(op)

state = ['wrvq', 94625185243550]
while state[0]!='humn':
    mk = monkeys[state[0]]
    if ok(monkeys,mk[2]):
        state[0] = mk[0]
        state[1] = normal_inv(mk[1])(state[1], monkeys[mk[2]])
    else:
        state[0] = mk[2]
        state[1] = alt_inv(mk[1])(state[1], monkeys[mk[0]])
print("part 2:",state[1])
