import asyncio
Queue = asyncio.Queue
from collections import defaultdict
# from typing import List, Union, Iterator, Callable
    #, Literal

class Intcode(object):
    Halt = object()  # truthy
    # _imode_type = Literal['list', 'queue']
    inst = 0
    debug = 1
    _debug_op = None
    # q_in:  Union[List[int], Queue[int]]
    # q_out: Union[List[int], Queue[int]]
    network = None  # type: list[Intcode]
    def __init__(self, code, name=None, q_in=None,
                 input_src=None,
                 output_func=None, input_mode='list'):
        self.code = defaultdict(int, enumerate(code))
        self.i = 0
        self.step_counter = 0
        self.halted = False
        self.name = name or Intcode.inst
        Intcode.inst += 1
        self.rel_base = 0
        # input
        self.input_mode = input_mode
        self.input = input_src or (lambda:int(input("input to %s:" % self.name)))
        if input_mode == 'list':
            self.q_in = q_in or []
        else:
            self.q_in = asyncio.Queue()
            if q_in:  # populate queue start
                for x in q_in: self.q_in.put_nowait(x)
        self.input_i = -1  # last input gotten from q_in
        self.next_io = 0  # next input to get to q_in from inputsrc.q_out
        self.sleep = False
        # output
        self.q_out = []
        self.shared_output_i = 0
        self.sent_output = False
        self.output_func = output_func

    def halt(self):
        self.halted = True

    def get_iter_input(self):
        return next(self.input)

    async def get_list_input(self):
        while len(self.q_in) <= self.input_i:
            # get input from self.input
            # wait for input to arrive in queue
            if isinstance(self.input, Intcode):
                if self.debug > 1:
                    print(f"{'':11}...from Intcode {self.input.name}")
                if len(self.input.q_out) <= self.next_io:
                    # wait for more output from intcode
                    await self.input.run_output()
                    if self.debug > 1:
                        print(f"Intcode {self.name}: wait for {self.input.name} done")
                self.q_in.append(self.input.q_out[self.next_io])
                self.next_io += 1
            else:  # it's an iterator
                self.q_in.append(self.get_iter_input())
        return self.q_in[self.input_i]

    async def get_queue_input(self):
        return await self.q_in.get()

    async def get_input(self):
        if self.debug>1:
            print(f"Intcode {self.name} getting input...")
        self.input_i += 1
        if isinstance(self.q_in, list):
            val = await self.get_list_input()
        elif self.input_mode == 'network':
            if self.q_in.empty():
                self.sleep = True
                await asyncio.sleep(0)
                self.sleep = False
                val = -1
            else:
                val = self.q_in.get_nowait()
        else:
            val = await self.get_queue_input()
        if self.debug>1:
            print(f"Intcode {self.name}: got input: {val}")
        return val

    def send_output(self, out):
        if self.debug>1:
            print(f"Intcode {self.name}: sending output: {out}")
        if isinstance(self.q_out, list):
            self.q_out.append(out)
        else:
            self.q_out.put_nowait(out)
        if self.input_mode=='network':
            if len(self.q_out)%3==0:
                addr, x, y = self.q_out[-3:]
                print(f"{self.name} sending packet to {addr}")
                if addr==255:
                    # send to NAT
                    NAT = self.network[255]
                    NAT.packet = (x,y)
                    print(f"THE_NAT: {NAT} // {NAT.packet}")
                else:
                    self.network[addr].q_in.put_nowait(x)
                    self.network[addr].q_in.put_nowait(y)
        self.sent_output = True
        if self.output_func:  # eg print
            self.output_func(out)

    op_p = {
        # params map: 0 read, 1 write (evaluated later)
        1: [0, 0, 1], # +
        2: [0, 0, 1], # *
        3: [1],  # input
        4: [0],  # output
        5: [0, 0],  # jnz
        6: [0, 0],  # jez
        7: [0, 0, 1],  # <
        8: [0, 0, 1],  # =
        9: [0],  # inc rel base
        99: [],
    }
    def get_op(self):
        opcode = self.code[self.i]
        op, params = opcode%100, opcode//100
        # get params
        iparams = [int(c) for c in '%03d' % params][::-1]
        # a: is write addr?
        iparams = [[b, 1|b][a]
                    for a,b in zip(self.op_p[op], iparams)]
        opvals = [self.code[v] if mode == 0 else
                  v if mode == 1 else
                  self.code[v+self.rel_base] if mode==2 else
                  v+self.rel_base if mode==3 else None  # Error if none
                     for mode, v in zip(iparams, [self.code[self.i+d] for d in range(1,4)])]
        self._debug_op = op, opvals, iparams
        return op, opvals

    async def step(self):
        """Return whether produced output or halted"""
        if self.halted: return Intcode.Halt
        self.step_counter += 1
        self.sent_output = False
        op, p = self.get_op()
        if op==99:
            self.halted = True
            return Intcode.Halt
        elif op==1: self.code[p[2]] = p[0]+p[1]
        elif op==2: self.code[p[2]] = p[0]*p[1]
        elif op==3: self.code[p[0]] = await self.get_input()
        elif op==4: self.send_output(p[0])
        elif op==5 and p[0]!=0: self.i = p[1]-1-len(p)
        elif op==6 and p[0]==0: self.i = p[1]-1-len(p)
        elif op==7: self.code[p[2]] = int(p[0]<p[1])
        elif op==8: self.code[p[2]] = int(p[0]==p[1])
        elif op==9: self.rel_base += p[0]

        self.i += 1 + len(p)
        return self.sent_output

    async def async_run(self):
        try:
            while await self.step() is not Intcode.Halt: pass
        except:
            if self.debug>1:
                print(f"Intcode {self.name} at {self.i}: {self.code}")
                print(f"Intcode {self.name}: op was: {self._debug_op}")
            raise

    def run(self):
        asyncio.run(self.async_run())
        return self.q_out[-1]

    async def run_output(self, err=True):
        """Return whether an output was produced"""
        while not await self.step(): pass
        if self.halted and err:
            raise RuntimeError(f"Intcode {self.name}: Halted before output was produced")
        return not self.halted  # true if halted before producing output

    async def async_output(self, n=1):
        i = 0
        while 1:
            while i+n > len(self.q_out) and await self.run_output(err=False): pass
            if self.halted: break
            if self.debug>1:
                print(f"Intcode {self.name}.async_out({n})) yielding: {self.q_out[i:i+n]}")
            yield self.q_out[i:i+n]
            i += n
        rest = self.q_out[i:]
        if self.debug>1:
            print(f"Intcode {self.name}.async_out({n})) remaining is: {rest}")


def day2_class(ol):
    for a in range(100):
        for b in range(100):
            comp = Intcode([ol[0], a, b] + ol[3:])
            comp.run()
            if a==12 and b==2: print("part 1:",comp.code[0])
            if comp.code[0]==19690720: print("part 2:",100*a+b)


async def collect(n, agen):
    # collect into groups of n. superseded.
    g = []
    async for out in agen:
        g.append(out)
        if len(g)==n:
            yield g
            g = []
    if g:
        yield g


def to_p(c): return [int(c.real), int(c.imag)]
def printgc(d, rev=1):
    rev = [lambda x:x, reversed][rev]
    xs, ys = zip(*[to_p(k) for k in d.keys()])
    for y in rev(range(min(ys), max(ys)+1)):  # make sure to reverse ys
        print(''.join(['  ','##','[]','--','()'][d[x+y*1j]] for x in range(min(xs), max(xs)+1)))

def printgi(d, rev=1):
    rev = [lambda x:x, reversed][rev]
    xs, ys = zip(*d.keys())
    for y in rev(range(min(ys), max(ys)+1)):  # make sure to reverse ys
        print(''.join(['  ','##','[]','--','()'][d[x,y]] for x in range(min(xs), max(xs)+1)))


def console_ascii_input():
    while 1:
        yield from input().encode('ascii')
        yield 10

def AsciiIntcode(code, inp):
    return Intcode(code, input_src=inp,
                   output_func=lambda i:print(chr(i),end='') if i<128 else print(i))

if __name__ == '__main__':
    # Ascii intcode interpreter
    import sys
    doc = f"""{sys.argv[0]} program
    Run the ASCII Intcode program, taking ascii input from stdin
    and printing output as ASCII (if in range) to stdout.
    """
    if len(sys.argv)==1:
        print(doc)
    else:
        prog = sys.argv[1]
        with open(prog) as f:
            ic = [int(i) for i in f.read().strip().split(',')]
        AsciiIntcode(ic, inp=console_ascii_input()).run()