#
# from math import ceil, floor
# from collections import Counter
# def mul(C, n):
#     return Counter({k: v * n for k, v in C.items()})
#
# from pprint import pprint
#
# t0 = """
# 9 ORE => 2 A
# 8 ORE => 3 B
# 7 ORE => 5 C
# 3 A, 4 B => 1 AB
# 5 B, 7 C => 1 BC
# 4 C, 1 A => 1 CA
# 2 AB, 3 BC, 4 CA => 1 FUEL""".strip().split('\n')
# t1 = """
# 157 ORE => 5 NZVS
# 165 ORE => 6 DCFZ
# 44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
# 12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
# 179 ORE => 7 PSHF
# 177 ORE => 5 HKGWZ
# 7 DCFZ, 7 PSHF => 2 XJWVT
# 165 ORE => 2 GPVTF
# 3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
# """.strip().split('\n')
# t2="""
# 2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
# 17 NVRVD, 3 JNWZP => 8 VPVL
# 53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
# 22 VJHF, 37 MNCFX => 5 FWMGM
# 139 ORE => 4 NVRVD
# 144 ORE => 7 JNWZP
# 5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
# 5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
# 145 ORE => 6 MNCFX
# 1 NVRVD => 8 CXFTF
# 1 VJHF, 6 MNCFX => 4 RFSQX
# 176 ORE => 6 VJHF""".strip().split('\n')
# t3="""
# 171 ORE => 8 CNZTR
# 7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
# 114 ORE => 4 BHXH
# 14 VRPVC => 6 BMBT
# 6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
# 6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
# 15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
# 13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
# 5 BMBT => 4 WPTQ
# 189 ORE => 9 KTJDG
# 1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
# 12 VRPVC, 27 CNZTR => 2 XDBXC
# 15 KTJDG, 12 BHXH => 5 XCVML
# 3 BHXH, 2 VRPVC => 7 MZWV
# 121 ORE => 7 VRPVC
# 7 XCVML => 6 RJRHP
# 5 BHXH, 4 VRPVC => 5 LTCX""".strip().split('\n')
#
# cost = {}  # type: dict[str, (int, Counter)]
# with open('input14.txt') as f:
#     lines = f
#     for line in lines:
#         a_cost, b = line.split('=>')
#         num_prod,prod_ingr = b.strip().split()
#         assert prod_ingr not in cost  # only 1 way to produce this ingredient
#         ctr = Counter({name:int(val)
#                        for ingr in a_cost.strip().split(',')
#                        for val,name in [ingr.strip().split()]})
#         cost[prod_ingr] = [int(num_prod), ctr]
#
# # Part 1: how much ore for 1 fuel
# # Part 2: how much fuel for 10e12 ore
# # Part 3: how much fuel for (avogadro)*10e12, with no byproducts
#
# # generate toposort-order
# tc = {'ORE':set()}
# while not 'FUEL' in tc:
#     for k in cost:
#         res = cost[k][1]
#         if res.keys() <= tc.keys():
#             tc[k] = res.keys()
#             for tk in tc[k]:
#                 tc[k] |= tc[tk]
# order = sorted(tc, key=tc.__getitem__)
# assert order[0]=='ORE' and order[-1]=='FUEL'
#
# def part1_orig():
#     # order, cost
#     curr = Counter(FUEL=1)
#     extra = Counter()
#
#     while 1:
#         ks = [k for k in order if k!='ORE' and curr.get(k)]
#         if not ks:
#             break
#         for k in ks:
#             need = curr[k]
#             prod, res = cost[k]
#             get = int(ceil(need/prod))
#             extra[k] += get*prod - need
#             curr += mul(res, get) #({k:get*res[k] for k in res})
#             curr[k] -= get * prod
#
#     print(extra)
#     orig_extra = extra.copy()
#     while 1:
#         ks = [k for k in order if k != 'ORE' and extra.get(k,0)>=cost[k][0]]
#         if not ks:
#             break
#         for k in ks:
#             prod, res = cost[k]
#             ex = extra[k]//prod
#             extra += mul(res, ex)
#             extra[k] -= ex*prod
#
#     print(curr)
#     print(extra)
#     ore_for_one_fuel = curr['ORE'] - extra['ORE']
#     print(ore_for_one_fuel)
#     print()
#
#
# def ore_for_fuel(fuel, calc=ceil):
#     # reduce fuel back to ore -- correct solution
#     curr = Counter(FUEL=fuel)
#     # extra = Counter()
#     for ingr in order[:0:-1]:
#         prod, icost = cost[ingr]
#         # print(f"ingr: {ingr}, produce {prod} with: {icost}")
#         # times we need to produce(reduce) this
#         times_needed = calc(curr[ingr] / prod)
#         # print(f"we need to produce {times_needed} times")
#         # extra[ingr] = (times_needed * prod) - curr[ingr]
#         # if extra[ingr]:
#         #     print(f"  we have {extra[ingr]} extra {ingr} left")
#         curr += mul(icost, times_needed)
#         # don't remove since we never
#         # print(f"Current stuff: {curr}")
#     return curr['ORE']
#
# print(ore_for_fuel(1))
#
# def part2():
#     # have 1e12 ore: how much fuel?
#     # -- do binary search on fuel?
#     # (inspired by/taken from virtuNat, hs discord)
#     L = int(1e12/ore_for_fuel(1))
#     M = int(1e12/ore_for_fuel(1, calc=floor))
#     # binary search
#     F = (L+M)//2
#     D = F//2
#     while D:
#         ore = ore_for_fuel(F)
#         if ore<1e12:  # increase fuel
#             F+=D
#         else:
#             F-=D
#         if D==1: done=True
#         D//=2
#     # correct for bad binary search
#     F+=1
#     while ore_for_fuel(F)>1e12: F-=1
#     # assert ore_for_fuel(F+1) > 1e12
#     print(F)
#
# part2()
#
# # finished part 2 on 2019-12-22 evening
# # (followed by part 3 a few hours later)
#
# def gcd(a, b):
#     if b==0: return a
#     return gcd(b, a%b)
#
# def part3(how_much_ore):
#     # how much Fuel without any left over stuff
#     # First, find amount of ore that gives fuel w/o leftovers.
#     # order into levels --
#     # ORE, stuff that only needs ORE, ..., FUEL (level n)
#     # Then:
#     # take 1 fuel
#     # will use eg 2A 3B  but produce 1ORE->3A, 1ORE->2B
#     # -> need to produce 6 fuel to use (3|)12A, (2|)18B
#     ## LCM
#     # cx = curr['XXX']
#     # px = cost['XXX'][0]
#     # C = mul(C, px/gcd(cx,px))
#     # Then we can replace all level n-1 products with their ingredients
#     # and repeat until our counter only contains FUEL and ORE
#     curr = {"ORE"}
#     levels = [["ORE"]]
#     while "FUEL" not in levels[-1]:
#         next_level = [k for k in cost.keys()-curr
#                       if cost[k][1].keys()<=curr]
#         levels.append(next_level)
#         curr.update(next_level)
#     curr = Counter(FUEL=1)
#     for lvl in levels[:0:-1]:
#         for ingr in lvl:
#             prod, icost = cost[ingr]
#             need = curr[ingr]
#             g = gcd(prod, need)  # use for lcm
#             times_prod = need//g  # times we ran this reaction
#             times_used = prod//g  # multiplier for total FUEL we make
#             curr = mul(curr, times_used)
#             curr += mul(icost, times_prod)
#     tot_ore = curr["ORE"]
#     tot_fuel = curr["FUEL"]
#     print(f"{tot_ore} ORE => {tot_fuel} FUEL")
#     return (how_much_ore//tot_ore) * tot_fuel, how_much_ore%tot_ore
#
# p3ore = 602_214_076_000_000_000_000_000_000_000_000_000
# # p3ore = 10**8
# fuel, ore_left = part3(p3ore)
# print(f"Produced {fuel} FUEL, with {ore_left} leftover ORE")


from math import ceil, floor
from collections import Counter
def mul(C, n):
    return Counter({k: v * n for k, v in C.items()})

def gcd(a, b):
    if b==0: return a
    return gcd(b, a%b)


cost = {}  # type: dict[str, (int, Counter)]
with open('input14.txt') as f:
    for line in f:
        a_cost, b = line.split('=>')
        num_prod, prod_ingr = b.strip().split()
        assert prod_ingr not in cost  # only 1 way to produce this ingredient
        ctr = Counter({name:int(val)
                       for ingr in a_cost.strip().split(',')
                       for val,name in [ingr.strip().split()]})
        cost[prod_ingr] = [int(num_prod), ctr]

def part3(how_much_ore):
    # how much Fuel without any left over stuff
    # First, find smallest amount of ore that gives fuel w/o leftovers.
    # order into levels --
    # ORE, stuff that only needs ORE, ..., FUEL (level n)
    # Then: start with 1 fuel
    # If we have 2A,3B=>1FUEL  and 1ORE=>3A and 1ORE=>2B
    # -> need to produce fuel 6 times to use (3|)12A, (2|)18B
    ## LCM by decreasing level
    # repeat until our counter only contains FUEL and ORE
    curr = {"ORE"}
    levels = [["ORE"]]
    while "FUEL" not in levels[-1]:
        next_level = [k for k in cost.keys()-curr
                      if cost[k][1].keys()<=curr]
        levels.append(next_level)
        curr.update(next_level)
    curr = Counter(FUEL=1)
    for lvl in levels[:0:-1]:
        for ingr in lvl:
            prod, icost = cost[ingr]
            need = curr[ingr]
            g = gcd(prod, need)  # use for lcm
            times_prod = need//g  # times we ran this reaction
            times_used = prod//g  # multiplier for total FUEL we make
            curr = mul(curr, times_used)
            curr += mul(icost, times_prod)
    tot_ore = curr["ORE"]
    tot_fuel = curr["FUEL"]
    print(f"{tot_ore} ORE => {tot_fuel} FUEL")
    return (how_much_ore//tot_ore) * tot_fuel, how_much_ore%tot_ore

p3ore = 602_214_076_000_000_000_000_000_000_000_000_000
# p3ore = 10**8
fuel, ore_left = part3(p3ore)
print(f"Produced {fuel} FUEL, with {ore_left} leftover ORE")
