
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')
    # ii = ints(s)
    tot = 0
    for i in range(len(lines)):
        digs = list(enumerate(["zero","one","two","three","four","five","six","seven","eight","nine"])) + [(x,str(x)) for x in range(10)]
        first_dig = min((lines[i].find(d),x) for x,d in digs if d in lines[i])
        last_dig = max((lines[i].rfind(d),x) for x,d in digs if d in lines[i])
        tot += 10*first_dig[1]+last_dig[1]

        # lines[i] = lines[i].replace(b,str(a))
    # try: li = lmap(ints, lines)  # 2D
    # except: pass
    # try: gi = lmap(ints, lgroups)  # 2D
    # except: pass

# res = [str(l[0])[0]+str(l[-1])[-1] for l in li]
# print(sum(lmap(int,res)))
print(tot)
