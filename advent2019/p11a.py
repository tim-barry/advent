
from collections import defaultdict
from intcode import Intcode, printgc, asyncio

with open('input11.txt', 'r') as f:
    r = f.read().strip()
    cc = [int(s) for s in r.split(',')]

async def run_panels(code, start=0):
    panels = defaultdict(int)
    pos = 0+0j
    panels[pos] = start
    d = 1j
    in_it = iter(lambda:panels[pos], None)
    comp = Intcode(code, input_src=in_it)
    async for color, turn in comp.async_output(2):
        panels[pos] = color
        if turn==0: d*=1j
        else: d/=1j
        pos+=d
    return panels

async def part1(code):
    print(len(await run_panels(code)))
async def part2(code):
    printgc(await run_panels(code, start=1))
asyncio.run(part1(cc))
asyncio.run(part2(cc))

