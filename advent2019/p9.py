
from intcode import Intcode, asyncio

with open('input9.txt', 'r') as f:
    r = f.read().strip()

ol=eval('['+r+']')

Intcode(ol, q_in=[1], output_func=print).run()
Intcode(ol, q_in=[2], output_func=print).run()
# print(comp.q_out[0]==comp.code[1])