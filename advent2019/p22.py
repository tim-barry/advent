
with open('input22.txt') as f:
    shuffle = f.read().strip().split('\n')

def part1(sz, shuf, p):
    # Find position of card p after shuffling deck of sz cards
    deck = list(range(sz))

    def cut(l, n):
        return l[n:] + l[:n]

    def deal_inc(l, inc):
        L=len(l)
        nl = [0]*L
        for i, x in enumerate(l):
            nl[(inc * i) % L] = x
        return nl

    for line in shuffle:
        if line.endswith("stack"):
            deck = deck[::-1]
            continue
        n = int(line.split()[-1])
        if line.startswith('cut'):
            deck = cut(deck, n)
        else:
            deck = deal_inc(deck, n)
    return deck.index(p)

print("Part 1:", part1(10007, shuffle, 2019))


def qemod(a, b, m):  # quick exponent a**b mod m
    if b==0: return 1
    if b%2:
        return (a*qemod((a**2)%m, b//2, m)) % m
    return qemod((a**2)%m, b//2, m)

def exeuclid(a,b):
    # d == gcd(a,b) == ax+by
    if b==0:
        return a,1,0  # a == gcd(a,0) == 1*a + 0*0
    d,x,y = exeuclid(b, a%b)
    return d, y, x - (a//b)*y

def modinv(a,b):
    # a**-1 mod b
    d,x,y = exeuclid(a,b)
    if d==1:
        return x%b
    return 0


def compute_shuffle(shuf, sz):
    p0 = 0
    p1 = 1
    for line in shuf:
        if line.endswith("stack"):
            # reverse: 0 => sz-1
            p0 = ~p0
            p1 = ~p1
            continue
        n = int(line.split()[-1])
        if line.startswith('cut'):
            p0 -= n
            p1 -= n
        else:
            p0 *= n
            p1 *= n
        p0 %= sz
        p1 %= sz
    return p0, p1


def num_at_pos(sz, reps, shuf, p):
    # return (position of p, number at position p)
    # after shuffling the deck of 'sz' cards 'reps' times (with shuf)
    # We use that both are a linear function of p (second inverse of first):
    # if p1-p0=x then position of p after 1 rep is p0 + x*p  (mod sz)
    # and number at position p is (pos-p0) * (x**-1)  (mod sz)
    # rep 2: p0*(1 + x + x**2) + (x**2)(p-p0)
    p0, p1 = compute_shuffle(shuf, sz)
    x = (p1-p0)
    # Use the identity x^n+...+x^2+x+1 = (x^(n+1)-1)//(x-1)
    x_reps = qemod(x, reps, sz)
    # x_reps = pow(x, reps, sz)
    # (x-1)**-1 == pow(x-1, sz-2, sz)  since sz is prime (fermat's little thm)
    #   p0 * (x^(n+1) -1) * ((x-1)**-1)
    dx = p0*((x_reps*x-1) * modinv(x-1, sz)) % sz
    pos_of_p = (dx + x_reps*(p-p0))
    # invert the permutation
    num_at_p = ((p-dx) * modinv(x_reps, sz) + p0)
    return pos_of_p%sz, num_at_p%sz


def num_at_pos_2(sz, reps, shuf, p):
    # based on suggestions from reddit:
    # - use builtin 3-arg form of pow()
    # - use fermat's little thm for modular inverse
    # also clean up expression
    # virtuNat: python 3.8 allows pow(x-1, -1, sz) --> pow(x-1, sz-2, sz)
    p0, p1 = compute_shuffle(shuf, sz)
    x = p1-p0
    x_reps = pow(x, reps, sz)
    dx = p0*(x_reps-1) * pow(x-1,sz-2,sz) % sz
    pos_of_p = p*x_reps + dx
    num_at_p = (p-dx)*pow(x_reps,sz-2,sz)
    return pos_of_p%sz, num_at_p%sz


print("Verify part 1:", num_at_pos(10007, 1, shuffle, 2019)[0])
print("Part 2:", num_at_pos(119315717514047, 101741582076661, shuffle, 2020)[1])

pt2 = num_at_pos(119315717514047, 101741582076661, shuffle, 2020)
pt22= num_at_pos_2(119315717514047, 101741582076661, shuffle, 2020)
assert pt2==pt22
#

