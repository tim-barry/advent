
from collections import defaultdict

with open('input.txt', 'r') as f:
    r = f.read().strip()
code = [int(s) for s in r.split(',')]
from intcode import Intcode, printgc

panels = defaultdict(int)  # b/w
painted = set()

pos = 0+0j
d = 1j  # up
out_c = 0

def in_f():
    global pos
    while 1:
        yield panels[pos]

def out_go(val):
    global d, out_c, pos
    if out_c%2==0:  # first paint
        panels[pos] = val
        painted.add(pos)
    else:  # then turn and move
        if val==0:
            d *=1j
        else:
            d /=1j
        pos += d
    out_c += 1

# inputsrc is an iterator providing input values
# output_func is called on each output
Intcode(code, input_src=in_f(), output_func=out_go).run()

print(len(painted))  # part 1

panels = defaultdict(int)
pos, d, out_c = 0+0j, 1j, 0
panels[pos] = 1
Intcode(code, input_src=in_f(), output_func=out_go).run()
printgc(panels)  # part 2

