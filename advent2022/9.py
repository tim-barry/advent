
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('\d+',s))

f = "input9.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

dirs = {"U":-1j,"L":-1,"R":1,"D":1j}
moves = [[dirs[a],int(b)] for line in lines for a,b in [line.split()]]

def diagof(i):
    return i.real/abs(i.real)  + (i.imag/abs(i.imag))*1j

def moveTail(tp,hp):
    dp = hp-tp # from tail to head
    x,y = dp.real,dp.imag
    if abs(x)>1 or abs(y)>1:
        if x==0 or y==0:  # orthogonal 2 spaces away
            return tp+dp/2
        else: # diagonal 1,2
            return tp+ diagof(dp)
    else:
        return tp

h=0
t=0
s = {t}
tl=[0]*10
sl={0}
for move in moves:
    for mi in range(move[1]):
        h+=move[0]
        t = moveTail(t,h)
        s.add(t)
        tl[0]+=move[0]
        for ii in range(1,10):
            tl[ii] = moveTail(tl[ii],tl[ii-1])
        sl.add(tl[-1])
print(len(s))
print(len(sl))





