
from intcode import Intcode, asyncio

cc = list(eval(open('input.txt').read()))

comps = {i:Intcode(cc, q_in=[i], input_mode='network') for i in range(50)}
class THE_NAT(object):
    ys = set()  # y-values seen so far
    packet = None  # current packet

comps[255] = THE_NAT  # custom code in intcode class to handle sending to NAT
Intcode.network = comps

async def the_nat():
    while 1:
        await asyncio.sleep(0.1)  # <-- need timeout to be large enough
        if THE_NAT.packet and all(comp.sleep for i, comp in comps.items() if i!=255):
            x,y = THE_NAT.packet
            # print(f"NAT ys sent so far: {THE_NAT.ys}")
            # print(f"NAT sending packet since all computers are sleeping: {x,y}")
            if y in THE_NAT.ys:
                print(f"first repeated y: {y}")
                exit()
            THE_NAT.ys.add(y)
            comps[0].q_in.put_nowait(x)
            comps[0].q_in.put_nowait(y)


async def run(comps):
    await asyncio.gather(the_nat(), *[c.async_run() for i,c in comps.items() if i!=255])
asyncio.run(run(comps))

