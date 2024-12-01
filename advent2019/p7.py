
from intcode2 import *

with open('input.txt', 'r') as f:
    r = f.read().strip()

ol=eval('['+r+']')
# ol=[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
# 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
# ol = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
# 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
# TODO:
#  - rewrite in generator-chaining style?
#  - rewrite in continuation-passing style?
#  - rewrite in OOP style?


from itertools import permutations
import itertools

m=-1e100
for perm in permutations(range(5,10)):
    inps = [[phase] for phase in perm]  # each ampl first gets its phase
    inps[0].append(0)  # input for first is 0
    # each ampl's output goes to input of the next one
    # output for last goes to first -> first halts
    ampls = [gen_intcode(ol, inputs=inps[i], output=inps[(i+1)%5], num=i) for i in range(5)]
    # run ampls
    while 1:
        print("Starting cycle")
        for num, ampl in enumerate(ampls):
            try:
                print("running ampl %d" % num)
                res = next(ampl)
                print("main loop: inps are:")
                for inp in inps:
                    print inp
            except StopIteration: # halted
                break
        else:
            continue
        # print("Exiting ")
        break
    # for phase in perm:
    #     # send the ampliphier the phase, followed by input
    #     out = []
    #     run_intcode(ol[:], inputs=[phase]+inp, output=out.append)
    #     # outputs to out
    #     inp = out
    #     # send output to next amplifier and clear out
    # get output of last amplifier (to thurster)
    # res = out[0]

    if res>m:
        # print(m)
        # print(perm)
        m=res
        rp = perm
print m
print(rp)
# print ol



