from __future__ import print_function
# Intcode interpreter (original / py2)
ops = {
    # not included: 99 halt
    # (in, write, func)
    1: [2, 1, lambda a,b:a+b],  # Add
    2: [2, 1, lambda a,b:a*b],  # Mul
    3: [0, 1, input],  # input (default)
    4: [1, 0, print],  # output
    5: [1,-1, lambda a:a!=0],  # jnz
    6: [1,-1, lambda a:a==0],  # jez
    7: [2, 1, lambda a,b:a<b],  # < lt
    8: [2, 1, lambda a,b:a==b],  # == equal

    # 1: [2, 1, int.__add__],  # Add
    # 2: [2, 1, int.__mul__],  # Mul
    # 3: [0, 1, input],  # input (default)
    # 4: [1, 0, print],  # output
    # 5: [1,-1, int.__nonzero__],  # jnz
    # 6: [1,-1, (0).__eq__],  # jez
    # 7: [2, 1, int.__lt__],  # < lt
    # 8: [2, 1, int.__eq__],  # == equal
}
glob_ops = ops

def step(l, i, _ops=None):
    if _ops is not None:
        ops = _ops
    else:
        ops = glob_ops
    c = l[i]
    opcode = c%100
    if opcode==99:
        return None  # halt
    num_inputs, write_kind, func = ops[opcode]
    # get vals based on params
    iparams = map(int, ('%03d'%(c//100)))[::-1]
    params = iparams[:num_inputs +(write_kind==-1)]
    vals = [l[v] if mode==0 else v if mode==1 else None
            for mode, v in zip(params, l[i+1:])]
    if write_kind==-1:
        jloc = vals[-1]
        vals = vals[:-1]
    # execute op
    res = int(func(*vals) or 0)  # may be None (print)
    # write/jump
    if write_kind==1:  # write to address as extra param
        l[l[i+num_inputs+1]] = int(res)
        i += num_inputs + 2  # this and write
    elif write_kind==-1:  # jump if res true
        if res:
            i = jloc
        else:
            i += num_inputs + 2  # this and next ip
    elif write_kind==0:
        # does not write
        i += num_inputs + 1
    # return new inst pointer
    return i

def run_intcode(l, inputs=None, output=print):
    l = l[:]
    print("l:",l)
    print("inputs:",inputs)
    # Day 5
    if inputs is not None:  # iterable
        ops[3][2] = lambda it=iter(inputs):next(it)  # change input instr
    ops[4][2] = output
    #

    i = 0
    while 1:
        try:
            i = step(l, i)
        except:
            print(i, l)
            raise
        if i is None:
            break  # done
    return l

def gen_intcode(l, inputs=None, output=None, num=None):
    l = l[:]
    # print("l:",l)
    # print("inputs:",inputs)
    # Day 5
    local_ops = ops.copy()
    if inputs is not None:  # iterable
        def get_inp(i=[0]):
            try:
                print('ampl %s: getting input %d' % (num, i[0]))
                val = inputs[i[0]]
                print('-> got %s' % val)
                i[0]+=1
                return val
            except IndexError:
                print("ampl %s: get_inp inputs are:" % num, inputs)
                raise
        local_ops[3] = ops[3][:]
        local_ops[3][2] = get_inp #iter(inputs).next  # change input instr
    local_ops[4] = ops[4][:]
    local_ops[4][2] = output.append
    #

    i = 0
    while 1:
        try:
            L = len(output)
            i = step(l, i, local_ops)
            if len(output)>L:
                print("ampl %s yielding %d" % (num, output[-1]))
                yield output[-1] # send to next / wait for input

        except (StopIteration, IndexError):
            print("ampl %s could not get next from inputs:"%num, inputs)
            raise #yield None
        except:
            print(i, l)
            raise
        if i is None:
            break  # done
    # return l


def day2(ol):
    for a in range(100):
        for b in range(100):
            nl = ol[:]
            nl[1:3] = a,b
            res = run_intcode(ol)
            if a==12 and b==2:
                print(res[0])  # part 1
            if nl[0]==19690720:
                print(100*a+b)  # part 2

def day5(ol):
    print("Day 5 part 1:")
    run_intcode(ol, inputs=[1])
    print("Day 5 part 2:")
    run_intcode(ol, inputs=[5])

