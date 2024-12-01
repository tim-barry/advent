
from primes import prim
from useful import *

with open('input.txt', 'r') as f:
    r = f.read().strip()

r = "5943571655648637331395381559791724443436335867388925683726951302202302448296707281824627883652587591895151146520202915947156731269525052688688951210692755104519205311077806015879429049592307429433197838571453340798614712386254484228245786635600107659671434157785254574887157782553755026098152635765535694368649159699236535557335973703371173007489145600480067251480860801630780758315373127122712125781364233918740150157480467799557630740651634899325891411539693725259628209598281541449857977926160408141226354442876304962826650124954572237190081283658696763142542435115169525207465007492571984653479367401049372561267691711439095339200719030377476414"
# dist = 100
l = list(map(int, r))
offset = int(r[:7])

print("offset:", offset)
print("total length:", len(r)*10000)
wo_off = len(r)*10000 - offset
print("length without offset:", wo_off)

dist = 287029238942
print("truncating primes to sqrt(length without offset)")
print("any factors greater than %d treated as prime" % int(sqrt(wo_off)))
print("since they cannot occur in the denominator (??)")
print("this will significantly speed up checking")
# lim = sqrt(dist + offset+1)
# while prim[-1] < lim:
#     nextpr(prim)
while not prim[-2]<=sqrt(wo_off):
    prim.pop()
print("done. last prime: %s" % prim[-1])
print("last prime squared / length:", (prim[-1]**2, wo_off))

pat = [0, -1, 0, 1]

def get_pat_i(out_pos, it):
    val = (it+1)//(out_pos+1)  # repeat out_pos times
    return pat[val%4]
def get_tens(n):  # -17 => 7
    return abs(n)%10

def part1(l):
    # 100 * O(n^2)
    for t in range(100):
        l = [get_tens(sum(l[i] * get_pat_i(out_i, i) for i in range(len(l))))
            for out_i in range(len(l))]
    print("part 1:")
    print(''.join(map(str, l[:8])))

# print("running part 1...")
# part1(l)

# part 2: repeat input list 10000 times
# input is way too big for the same O(n^2) algorithm.
# Note that the pattern is always the same for any given output position.
# Note that all the ones before the output position are 0.
# By inspection, offset > total length / 2, so the following 1's of the pattern
# extend all the way to the end; therefore we use the simpler algorithm
# of ignoring the first part of the list and just accumulating backwards.

def part2(l, offset):
    l = (l*10000)[offset:]  # ignore all before the offset
    # 100 * O(n), for n~500,000
    for x in range(100):
        # accumulate backwards
        rev_partial_sum = l[-1:]
        for x in l[-2::-1]:
        # for x in reversed(l[:-1]):
            rev_partial_sum.append(rev_partial_sum[-1]+x)
        l = [get_tens(x) for x in reversed(rev_partial_sum)]
    print("Done:")
    print(''.join(map(str, l[:8])))

# part2(l, offset)

def a_plus_b_choose_b_mod_10(a, b):
    # 1, a+1, (a+1)(a+2)/2, (a+1)(a+2)(a+3)/6...
    # 1, 1/1, 1/3/2 //2,  1/6/13/6 //6,
    # (a+1)(a+2)(a+3)/6 == ((a+1)(a+2)/2)(a/3+1)
    # -- but (a/3+1) not an integer, so can't mod
    # 1, 2, 2*3/2, 2*3*4/6
    pass

from collections import Counter  # count the factors
def pfactorsC(n, ps):
    pi = 0
    res = Counter()
    while pi<len(ps) and ps[pi]**2 <= n:
        while n % ps[pi] == 0:  # ps[pi] is factor
            n //= ps[pi]
            res[ps[pi]]+=1
        pi += 1
    if n > 1:
        if n<ps[-1]**2:  # it's a prime we can't mod by 10
            res[n]+=1
        else:  # treat remainder as prime (greater than max(ps)**2)
            res[n%10] += 1# should be == 1,3,7,9 (mod 10)
        # and only counting it mod 10 to save space -- doesn't work. why? ^
    return res


def generate_multipliers(dd, lenl, prim=prim):
    # takes about a minute for dd=100
    # (dd + i choose i) % 10 for i in 0..lenl-1
    # factorize before multiplying (as counter)
    print("generating multipliers")
    print("partially factorizing all the numbers from %d to %d..." % (dd, dd+lenl))
    print("this will take about an hour")
    # we can't store 500,000 counters (factorizations) ;
    # so we need to compute as we go along
    # so we can discard factorizations and avoid thrashing.
    multipliers_factor = Counter()  # n-1 choose t-1
    multipliers = [1]
    for t in range(1,lenl):
        n = dd+t
        n_factors = pfactorsC(n, prim)
        t_factors = pfactorsC(t, prim)
        # print("t, n =", (t, n))
        # print("nfactors:", n_factors)
        # print("tfactors:", t_factors)
        # multiply by n, divide by t  to get n choose t
        multipliers_factor += n_factors
        multipliers_factor -= t_factors
        # find the mod 10
        val_mod_10 = 1
        for c, ct in multipliers_factor.items():
            val_mod_10 *= (c%10)**ct
            val_mod_10 %= 10
            if val_mod_10==0:break
        multipliers.append(val_mod_10)
        if t%10000==0:
            print(t,'/',lenl)
    print("Generated multipliers")
    return multipliers

from math import log10
def part2b(n):
    offset = int(n[:7])
    l = list(map(int, n))
    l = (l*10000)[offset:]
    lenl = len(l)
    dd= dist-1
    # t=0:          1a,        1b,    1c, 1d
    # t=1: 1a+1b+1c+1d,  1b+1c+1d, 1c+1d, 1d
    # t=2: 1a+2b+3c+4d,  1b+2c+3d, 1c+2d, 1d
    # t=3:1a+3b+6c+10d,  1b+3c+6d, 1c+3d, 1d
    # t=100:
    #   1a+(100c1)b + (101c2)c + (102c3)d, ...
    multipliers = generate_multipliers(dd, lenl)
    # generate (99+i choose i)  for reverse cumulative sum
    res = [sum(x*m for x, m in zip(l[i:], multipliers))%10 for i in range(8)]
    print("Final result:")
    print(''.join(map(str, res)))

part2b(r)
"""
Python, 25/5

This was a fun problem -- after part 1 took over 10 seconds to run,
it was obvious I needed to find a faster algorithm for part 2.
(Python 3 runs both parts in ~10s, Pypy 2 runs the same code in 1-2s.)
"""

