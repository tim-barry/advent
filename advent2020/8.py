
from collections import Counter
import math
from functools import reduce


with open("8.txt") as f:
    lines = [l.strip() for l in f]

code = [
    line.split() for line in lines
]
acc = 0
lastacc=0
def run(code, part=2):
    acc = 0
    lastacc=0
    lasti=0
    i = 0
    visited = set()
    while 0<=i<len(code):
        lastacc=acc
        lasti=i
        visited.add(i)
        if code[i][0]=="nop":
            i+=1
        elif code[i][0]=="acc":
            acc+=int(code[i][1])
            i+=1
        elif code[i][0]=="jmp":
            i+=int(code[i][1])
        if i in visited:
            if part==1:
                print(lastacc)
            return None
    if i==len(code):
        # print("done")
        print(acc)
        return acc

for i in range(len(code)):
    c = code[:]
    if c[i][0]=="nop":
        c[i] = ["jmp", c[i][1]]
    elif c[i][0]=="jmp":
        c[i] = ["nop", c[i][1]]
    else:
        continue
    if run(c): break

