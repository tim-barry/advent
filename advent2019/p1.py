
with open('input1.txt') as f:
    r = f.read().strip()

l = [int(s) for s in r.split()]

mf =  sum((m//3)-2 for m in l)
print(mf)  # part 1

# part 2: need to calculate each module individually.
def tf(m):
    f = m//3 - 2
    nf = f
    while nf>=0:
        nf = nf//3 - 2
        f+= max(nf,0)
    return f
print(sum(tf(m) for m in l))