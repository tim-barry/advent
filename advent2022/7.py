
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('\d+',s))

f = "input7.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')


test = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".strip()
# lines = test.split('\n')

ss = defaultdict(int)
dd = defaultdict(set)  #subdirs
dirs=[]
child_dirs = set()
sz = 0
wasLS = 0
for line in lines:
    path = '/'.join(dirs)
    if line.startswith("$ cd"):
        if wasLS:
            #print(path,": child dirs:", child_dirs)
            dd[path] = child_dirs
            child_dirs = set()
            ss[path] = sz
            sz = 0
        wasLS = 0
        nd = line.split()[-1]
        if nd=='..':
            dirs.pop()
        elif nd=='/':
            dirs = []
        else:
            dirs.append(nd)
    elif line.startswith("$ ls"):
        wasLS = 1
    elif line.startswith("dir"):
        child_dir = line.split()[-1]
        child_dirs.add('/'.join(dirs+[child_dir]))
    else:
        try:
            sz += int(line.split()[0])
        except:
            print(line)

#get last directory
path = '/'.join(dirs)
if wasLS:
    print(path,": child dirs:", child_dirs)
    dd[path] = child_dirs
    child_dirs = set()
    ss[path] = sz
    sz = 0

# print(ss.keys())
# print(dd.keys())
ts = {}
while len(ss.keys()) > 1+len(ts.keys()):
    for k in ss.keys():
        if k in ts.keys():
            continue
        if set(dd[k])<=ts.keys(): # computed total size of all subdirs
            ts[k] = ss[k] + sum(ts[kk] for kk in dd[k])  # local + subdirs

k=''
ts[k] = ss[k] + sum(ts[kk] for kk in dd[k])  # local + subdirs

print(ts.keys()-ss.keys())
print(ts.values())
print(sum(v for v in ts.values() if v<=100000))

TOTAL_SPACE = 70000000
MIN_UNUSED =  30000000
MAX_USED =    40000000
overbudget = ts[''] - MAX_USED
print(min(v for v in ts.values() if v>=overbudget))
