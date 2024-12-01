
from intcode import Intcode
from itertools import permutations

def day7_class(code):
    def run_comps(perm):
        inps = [[phase] for phase in perm]
        inps[0].append(0)
        comps = [Intcode(code, q_in=inp) for inp in inps]
        for i in range(5): comps[i].input = comps[i-1]
        comps[-1].run()
        return comps[-1].q_out[-1]
    print(max(run_comps(perm) for perm in permutations(range(5))))
    print(max(run_comps(perm) for perm in permutations(range(5,10))))

with open('input7.txt', 'r') as f:
    r = f.read().strip()
    code = [int(s) for s in r.split(',')]
    day7_class(code)

