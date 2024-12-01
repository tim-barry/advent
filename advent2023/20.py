import itertools
import string
from collections import deque,defaultdict,Counter
from functools import reduce
from itertools import batched, starmap, accumulate, pairwise
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall(r'-?\d+',s))

f = "input.txt"

# Hang glider time?

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

# i'm feeling a 2D grid problem coming...
#g = defaultdict(int, {x+y*1j: (c) for y,line in enumerate(lines) for x,c in enumerate(line)})

test1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""".split('\n')
test2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".split('\n')
# lines = test2

g = {a[1:]:(a[0],b.split(', ')) for line in lines for a,b in [line.split(' -> ')]}
# g2 = {a:}

# starts %: flipflop : starts off/low;  on receiving LOW, flips
#starts &: remember (default low) :  NAND
#broadcaster: repeats
#button: sends 1xlow to broadcaster
state = {k:{src:0 for src in g.keys() if k in g[src][1]} if g[k][0]=='&'
            else 0  # flipflop/broadcaster
            for k in g.keys()}

# & sends LOW when all are HIGH

#&kz->rx   receives LOW when kz sends LOW
#&sj, &qq, &ls, &bg -> kz      kz sends LOW when all are HIGH -> when all [hb,hf,dl,lq] are LOW
 #&hb -> sj   sends HIGH when hb is LOW
 #&hf -> qq
 #&dl -> ls
 #&lq -> bg
#

keys = 'sj','qq','ls','bg'  # must all be HIGH

# determine preconditions?

# hb: [mr, pd, rj, bm, xg, zq, fl, vk, fx]  ALL flipflops: needs to send Low, ie all flipflops must be High
# feeds back into mr, rz, qg, pr
# if &hb sends Low: %mr was high; it will toggle %mr, back to low; then send a high (not affecting mr)
# %fl -> hb, rj ;; %rj -> hb      rj must send high: receive low from fl (and toggles) then fl must be toggled again
# seq [fl,rj,hb]:  [0,0,0] -> [1,0,1][0,1,1][1,1,*hb sends 0*]
# so fl must receive 3 (mod 4) low signals

#broadcaster ->
# %mr -> bm,hb    # 1 mod 2
# %bm -> pd,hb    # 1 mod 4
# %pd -> hb,xg    # 1 mod 8   # diff order?
# %xg -> rz,hb    # 1 mod 16
# %rz->pr         # any mod 32
# %pr->zq         # any mod 64
# %zq->hb,qg      # 1 mod 128
# %qg->vk         #any
# %vk->fx,hb
# %fx->fl,hb
# %fl->hb,rj
# %rj->hb
# 111101001110 -> 111101001111 (hb turns on); mr hit (hb turns off again immediately)... ->
# 12 bits: on 2^12-1 activation, will trigger mr->hb low
# suppose rj..mr are 11..0; then pressing button(toggling mr) sends high to bm(nothing) and high to hb(will send low)
# some toggles are hit: mr,rz,qg,pr  (+1, +2^4, +2^7, +2^5 = 0b11010001)    (still on 2^12-1 button press)
# all 4 need to hit on same button push (LCM)
# hb on at step: 111101001111,   111101001111+ (111100101111 = cycle length)
#
# WRONG the input is nice

#graphviz: (all cycles len 12)
#hf:  12:  111110100011,   111110100011+  0 (cycle length = start
#lq:  1110_1001_1011
#dl: 1110_1101_0101


# hb -> mr, rz, qg, pr    default sends High (does not affect flipflops) to
# but if it becomes set Low it will toggle those...

# mr toggles, sends High  (bm ignores, hb sends High=does nothing)
# mr toggles, sends Low (bm toggles, sends High; hb sends high; pd does nothing; hb sends high)

big_keys = [next(iter(state[k].keys())) for k in keys]  # hb,...
#assume all predecessors are flipflops and are in a line
seqs = [set(state[k].keys()) for k in big_keys]  # flipflops required
s2 = [s.copy() for s in seqs]
changed = True
while changed:
    changed = False
    for ffs in s2:
        prereqs = {k for k,(_,ch) in g.items() if any(f in ch for f in ffs)} - {'roadcaster'}
        if not (prereqs <= ffs):
            ffs.update(prereqs)
            changed = True
print(seqs[0])
print(s2[0])
print(s2[0]-seqs[0])  # ignored by hb

exit()

# 4 calculators; split at broadcaster

cycle = []

low_sent = 0
high_sent = 0
for button_presses in itertools.count(1):
    cycle.append([])
    #push the button
    #low_sent +=1  # adding to q
    q = [('roadcaster',0,'button')]  #dst,pulse,src
    while q:
        nq = []
        for dst,pulse,src in q:
            if pulse==0: low_sent += 1
            else: high_sent += 1
            if dst=='rx' and pulse==0:
                print(button_presses)
                break
            if dst=='output' or dst not in g: continue  #ignore
            send = None
            if g[dst][0]=='b': #roadcaster
                send=pulse
            if g[dst][0]=='%':  # flipflop
                if pulse==0:
                    state[dst] = 1^state[dst]  #flip
                    send = state[dst]
            if g[dst][0]=='&':
                #update memory
                state[dst][src] = pulse
                if all(state[dst].values()): #all high
                    send = 0 #low
                else:
                    send = 1 #high
                if dst=='sj':
                    cycle[-1].append(tuple(int(not all(state[k].values())) for k in keys))
            if send is not None:
                for n in g[dst][1]:
                    nq.append((n, send, dst))
        q = nq
    print(cycle[-1])

# print(low_sent,high_sent)
# print(low_sent*high_sent)