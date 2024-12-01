
from collections import defaultdict
from intcode import Intcode, printgc

with open('input13.txt', 'r') as f:
    r = f.read().strip()
code = [int(s) for s in r.split(',')]

d = defaultdict(int)
out_c = 0
def out_go(val):
    global x, y, tileid, out_c, score #d, out_c, pos
    if out_c%3==0:
        x = val
    elif out_c%3==1:
        y = val
    else:
        if x==-1 and y==0:
            score = val
        else:
            tileid = val
            d[x+y*1j] = tileid
    out_c += 1

Intcode(code, output_func=out_go).run()

print(sum(1 for k,v in d.items() if v==2)) # blocks

print()
printgc(d)

def get(d, n):
    return [k for k,v in d.items() if v==n][0]

code[0] = 2
d = defaultdict(int)
out_c = 0
score = 0

def in_f():
    while 1:
        # move paddle towards ball (x position)
        ball = get(d, 4).real
        paddle = get(d, 3).real
        if ball<paddle:  # need to move paddle left
            yield -1
        elif ball==paddle:
            yield 0
        else:
            yield 1
Intcode(code, q_in=[], input_src=in_f(), output_func=out_go).run()

print(score)
