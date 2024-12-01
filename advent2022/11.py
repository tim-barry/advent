import copy
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('\d+',s))

f = "input11.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

#v2
def parse(monkey):
    lines = monkey.split('\n')
    #monkey index = lines[0]
    monkey_items = ints(lines[1])
    op = eval("lambda old:"+lines[2].split('=')[1])
    div = ints(lines[3])[0]
    true = ints(lines[4])[0]
    false = ints(lines[5])[0]
    move_f = eval(f"lambda x: {true} if x%{div}==0 else {false}")
    return [monkey_items, op, move_f]
monkies = lmap(parse, lgroups)

def loop(rounds, mks, div=True):
    mks = copy.deepcopy(mks)
    inspected = [0] * len(mks)
    for r in range(rounds):
        for mi, (it, op, mv) in enumerate(mks):
            for i in it:
                i = op(i)
                if div:
                    i//=3
                else:
                    i%=M
                dst = mv(i)
                mks[dst][0].append(i)
                inspected[mi] += 1
            mks[mi][0] = []
    times = sorted(inspected)
    return times[-1] * times[-2]

M = 17*3*11*7*5*13*2*19

print(loop(20,monkies))
print(loop(10000,monkies,False))

#items: worry lvl in order
#inspect -> change worry
#after inspect but before worry test:
# //3

#each monkey takes a turn
#and throws all its items

#original solution:
rounds = 10000

add = lambda x:lambda y:(x+y)%M
mul = lambda x:lambda y:(x*y)%M
move = lambda a,b,c:lambda x:b if x%a==0 else c

inspected = [0]*8
monkeys = [
[[71, 86],mul(13),move(19,6,7)],
[[66, 50, 90, 53, 88, 85],add(3),move(2,5,4)],
[[97, 54, 89, 62, 84, 80, 63],add(6),move(13,4,1)],
[[82, 97, 56, 92], add(2), move(5,6,0)],
[[50, 99, 67, 61, 86], lambda x:(x*x)%M, move(7,5,3)],
[[61, 66, 72, 55, 64, 53, 72, 63],add(4),move(11,3,0)],
[[59, 79, 63],mul(7),move(17,2,7)],
[[55],add(7),move(3,2,1)],
]

for r in range(10000):
    for mi,(it, op, mv) in enumerate(monkeys):
        for i in it:
            i = op(i)#//3
            dst = mv(i)
            monkeys[dst][0].append(i)
            try:
                inspected[mi]+=1
            except:
                #pprint(monkeys[0])
                print(mi)
        monkeys[mi][0] = []

times = sorted(inspected)
mb = times[-1]*times[-2]
print(mb)


