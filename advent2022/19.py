import math
import string
from collections import deque,defaultdict,Counter
from functools import reduce
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall('-?\d+',s))

f = "input19.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

data = lmap(ints, lines)


# ore,clay,obsidian,geode
# robots = [1,0,0,0]

# data = [
#     [1,4,2,3,14,2,7],
#     [2,2,3,3,8,3,12]
# ]

#collect 1/min
#takes 1m to build a robot
#opened geodes after 24 mins
def tplus(a,b): return tuple(x+y for x,y in zip(a,b))

def quality(bp):
    return open_geodes(bp) * bp[0]

def open_geodes(bp, mins=24):
    #State: Ro,Rc,Rb,Rg; o,c,bb,g; t
    start = (1,0,0,0,0,0,0,0,1)
    No, ore_cost_1, ore_cost_2, ore_cost_3, clay_cost_3, ore_cost_4, obby_cost_4 = bp
    # BFS with trimming
    ore_costs = [ore_cost_1,ore_cost_2,ore_cost_3,ore_cost_4]
    clay_costs = [0,0,clay_cost_3,0]
    obby_costs = [0,0,0,obby_cost_4]
    max_ore_cost = max(ore_costs)
    q = [start]
    mGeodes = 0
    while q:
        nq = []
        for st in q:
            steps_to_end = mins + 1 - st[-1]
            # ex. at start of minute 22:
            # steps_to_end = 3 (will produce 3 more time);
            #  robot built this minute produces 2x  (next minute 1x next 0x)
            endGeodes = st[7] + st[3] * steps_to_end
            possGeodes = endGeodes + (steps_to_end * (steps_to_end - 1)) // 2
            if possGeodes <= mGeodes:
                continue  # no way to beat current maximum, even if constantly building geode robots
            if st[-1]==mins: # at last timestep: can't build more robots (steps_to_end = 1 since we still produce 1x)
                if endGeodes > mGeodes:
                    mGeodes = endGeodes
                    # print(f"new max geodes: {mGeodes}")
                continue
            # Advance to next robot built
            for i in range(4):
                if i==0 and st[0]>=max_ore_cost: continue # dont build more if have enough to build one every turn
                if i==1 and st[1]>=clay_cost_3: continue
                if i==2 and st[2]>=obby_cost_4:
                    if st[0]>=ore_costs[-1]: #can continuously build geode robots
                        mGeodes = possGeodes
                        break
                    continue
                if (obby_costs[i]>0 and st[2]==0) or (clay_costs[i]>0 and st[1]==0): continue #can't build - div.by 0
                ore_time = max(0,int(math.ceil((ore_costs[i]-st[4])/st[0])))
                clay_time = max(0,int(math.ceil((clay_costs[i]-st[5])/st[1]))) if st[1]>0 else 0
                obby_time = max(0,int(math.ceil((obby_costs[i]-st[6])/st[2]))) if st[2]>0 else 0
                dt = 1+max(ore_time,clay_time,obby_time)  # time until we produce the robot (at least 1 turn)
                next_time = st[-1]+dt
                if next_time>mins: # last robot will not contribute: calculate ending geodes and break
                    if endGeodes > mGeodes:
                        mGeodes = endGeodes
                        # print(f"new max geodes: {mGeodes}")
                    continue
                next_st = list(st)
                for ti in range(4):
                    next_st[ti+4]+=next_st[ti]*dt  # produce for N turns
                #build robot: pay costs
                next_st[4]-=ore_costs[i]
                next_st[5]-=clay_costs[i]
                next_st[6]-=obby_costs[i]
                next_st[i] += 1 # extra robot of this type
                next_st[-1] = next_time
                nq.append(tuple(next_st))
        q = nq
    return mGeodes


print(sum(map(quality,data)))

data2 = data[:3]
print([open_geodes(bp, 32) for bp in data2])
