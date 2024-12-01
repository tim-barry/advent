
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('\d+',s))

f = "input13.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')




data = [lmap(eval,g.split('\n')) for g in lgroups]
data2 = sum(data,[])

#print(data[0][)
def cmp(a,b):
    return (a>b) - (a<b)

cmpand = lambda a,b:[b,a][a]

def listcmp(p1,p2):
    return cmpand(reduce(cmpand, map(multicmp,zip(p1, p2)), 0), cmp(len(p1),len(p2)))

def multicmp(p1p2):
    p1, p2 = p1p2
    t1, t2 = type(p1), type(p2)
    if t1 is t2 is int:
        return cmp(p1,p2)
    elif t1 is t2 is list: return listcmp(p1,p2)
    elif t1 is list:
        return listcmp(p1,[p2])
    else:
        return listcmp([p1],p2)


print(sum((multicmp(d)==-1)*(i+1) for i,d in enumerate(data)))
#print([(multicmp(d)==-1)*(i+1) for i,d in enumerate(data)])

divs = [
    [[2]],
    [[6]]
]
res = data2 + divs
from functools import cmp_to_key
res = sorted(res, key=cmp_to_key(lambda x,y:multicmp((x,y))))
print((res.index(divs[0])+1) * (res.index(divs[1])+1))



class mylist(list): #incorrect
    def convert(self):
        for i,item in enumerate(self):
            if type(item) is list:
                self[i]=mylist(item)
                self[i].convert()
    def __lt__(self,other):
        if type(other) is int:
            return super().__lt__([other])
        return super().__lt__(other)
    def __gt__(self,other):
        if type(other) is int:
            return super().__gt__([other])
        return super().__gt__(other)
    def __eq__(self, other):
        if type(other) is int:
            return self.__eq__([other])
        return super().__eq__(other)
    def __str__(self):
        return "("+super().__str__()+")"
    def __repr__(self):
        return "("+super().__repr__()+")"

data3 = mylist(data)
data3.convert()
print([(d[0]<d[1])*(i+1) for i,d in enumerate(data3)])
print(sum((d[0]<d[1])*(i+1) for i,d in enumerate(data3)))
data4 = mylist(data2 + divs)
data4.convert()
dv1,dv2 = data4[-2:]
res2 = sorted(data4)
print((res2.index(dv1)+1) * (res2.index(dv2)+1))
