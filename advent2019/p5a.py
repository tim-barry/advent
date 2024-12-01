
from intcode import Intcode

def day5_class(ol):
    Intcode(ol, q_in=[1], output_func=print).run()
    Intcode(ol, q_in=[5], output_func=print).run()

with open('input5.txt', 'r') as f:
    r = f.read().strip()
    code = [int(s) for s in r.split(',')]
    day5_class(code)

