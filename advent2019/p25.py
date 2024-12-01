
# manually solved


from intcode import Intcode, AsciiIntcode, asyncio

with open('input.txt') as f:
    r = f.read().strip()
#
# t0 = """
# """
# t1="""
# """

cc = eval('['+r+']')

# need to avoid (hardcoded):
avoid = [
    "molten lava",
    "escape pod",
    "infinite loop",
    "photons",
    "electromagnet",
]
# explore and take all other items
# go to detector
# 2**8 choices (assume)
# do SAT or ? to determine ordering?
# eg {abc} > tot, {abd} < tot:
# c > d
# do multiple times and then do alternating-low-high search?
# or just immediately start with alternating-low-high-search?

def try_enter(items):
    pass
from itertools import combinations
def alternate_low_high(items):
    curr = frozenset()
    vis = {}  # items: low, exact, high (-1/0/1)
    # eliminate heavy items
    # for c in combinations(items):
    for item in items.copy():
        st = curr|{item}
        val = vis[st] = try_enter(st)
        if val==0:
            return {item}
        elif val>0:
            # too heavy, ignore this
            items-={item}
    #


commands = b"""
...
take monolith
...
take mug
...
take cake
...
take coin
...
"""

AsciiIntcode(cc, inp=commands).run()


