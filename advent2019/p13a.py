
# Alternate day 13 -- without globals
from collections import defaultdict
from intcode import Intcode, asyncio, printgi

with open('input13.txt', 'r') as f:
    r = f.read().strip()
    cc = [int(s) for s in r.split(',')]

# 0 space 1 wall 2 block 3 paddle 4 ball

async def part1(code):
    d = defaultdict(int)
    comp = Intcode(code)  # no input
    async for x, y, tile in comp.async_output(3):
        d[x,y] = tile
    # number of blocks
    print(sum(v==2 for v in d.values()))
    # printgi(d)

async def part2(code):
    code[0] = 2
    d = defaultdict(int)
    def in_f():
        while 1:  # get ball and paddle position
            ball = [x for (x,y),v in d.items() if v==4][0]
            padl = [x for (x,y),v in d.items() if v==3][0]
            # move paddle towards ball -- yield cmp(ball, padl)
            yield (ball > padl) - (ball < padl)
    comp = Intcode(code, input_src=in_f())
    async for x, y, tile in comp.async_output(3):
        d[x,y] = tile
    print(d[-1,0])  # score

asyncio.run(part1(cc))
asyncio.run(part2(cc))
