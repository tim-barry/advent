
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('\d+',s))

f = "input10.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')


ins = [line.split() for line in lines]

cycls = [20,60,100,140,180,220]

arr = [[' ']*40 for tt in range(6)]

x=1
c = 1
tot=0
for i in ins:
    y = (c-1)//40
    xp = (c-1)%40
    arr[y][xp] = '#' if x-1<=xp<=x+1 else ' '
    if c%40==20 and c<230:
        tot += c*x
    if i[0]=='noop':
        c+=1
    else:
        t = int(i[1])
        c+=1
        y = (c - 1) // 40
        xp = (c - 1) % 40
        arr[y][xp] = '#' if x-1 <= xp <= x+1 else ' '
        if c % 40 == 20 and c < 230:
            tot += c * x
        c+=1
        x += t



print(tot)
for line in arr:
    print(''.join(line))
