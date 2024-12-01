from __future__ import print_function
from intcode2 import *

with open('input5.txt', 'r') as f:
    r = f.read().strip()

ol=eval('['+r+']')
# ol = [int(s) for s in r.split(',')]

def day5(ol):
    print("Day 5 part 1:")
    run_intcode(ol, inputs=[1])
    print("Day 5 part 2:")
    run_intcode(ol, inputs=[5])

day5(ol)

# original code
if 1+-1:
# for a in range(100):
#     for b in range(100):
        l = ol[:]
        i = 0
        # l[1] = a
        # l[2] = b
        while 1:
            dd=0
            c = l[i]
            params = map(int,('%03d'% (c//100)))[::-1]
            c = c%100
            if c==1:
                a,b=l[i+1:i+3]
                if params[0]==0:
                    a = l[a]
                if params[1]==0:
                    b = l[b]
                t = a+b
                l[l[i+3]] = t  # never immediate
                dd=4
            elif c==2:
                a,b=l[i+1:i+3]
                if params[0]==0:
                    a = l[a]
                if params[1]==0:
                    b = l[b]
                t=a*b
                l[l[i+3]] = t
                dd=4
            elif c==3:
                l[l[i+1]] = 5 #int(input())
                dd=2
            elif c==4:
                a = l[i+1]
                if params[0]==0:
                    a = l[a]
                print(a)
                dd=2
            elif c==5:
                a,b = l[i+1:i+3]
                if params[0]==0: a = l[a]
                if params[1]==0: b = l[b]
                if a!=0:
                    i = b
                else:
                    dd=3
            elif c==6:
                a,b = l[i+1:i+3]
                if params[0]==0: a = l[a]
                if params[1]==0: b = l[b]
                if a==0:
                    i = b
                else:
                    dd=3
            elif c==7:
                a,b = l[i+1:i+3]
                if params[0]==0: a = l[a]
                if params[1]==0: b = l[b]
                t = int(a<b)
                l[l[i+3]] = t
                dd=4
            elif c==8:
                a,b = l[i+1:i+3]
                if params[0]==0: a = l[a]
                if params[1]==0: b = l[b]
                t = int(a==b)
                l[l[i+3]] = t
                dd=4

            elif c==99:
                break
            else:
                print("err!")
                print(l[i])
                print(l)
            i+=dd
            # print(i,l)
        # if a==12 and b==2:
        #     print(l[0])  # part 1
        # if l[0]==19690720:
        #     print(100*a+b)  # part 2
