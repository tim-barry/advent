
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('\d+',s))

f = "input6.txt"

with open(f) as r:
    s = r.read().strip()
    # lines = s.rstrip().split('\n')
    # lgroups = s.rstrip().split('\n\n')

for i in range(len(s)):
    if len(set(s[i:i+14]))==14:
        print(s[i:i+14])
        # print(s[i-1:i+3])
        print(i+14)
        break


print(

)
