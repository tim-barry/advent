

r = "5943571655648637331395381559791724443436335867388925683726951302202302448296707281824627883652587591895151146520202915947156731269525052688688951210692755104519205311077806015879429049592307429433197838571453340798614712386254484228245786635600107659671434157785254574887157782553755026098152635765535694368649159699236535557335973703371173007489145600480067251480860801630780758315373127122712125781364233918740150157480467799557630740651634899325891411539693725259628209598281541449857977926160408141226354442876304962826650124954572237190081283658696763142542435115169525207465007492571984653479367401049372561267691711439095339200719030377476414"
l = list(map(int, r))
offset = int(r[:7])

# dist = 100
dist = 287029238942

l = (l*10000)[offset:]
woff = len(l)  # 546,000

pass
# Use modular inverses

from collections import Counter
def dfactor(n):
    count_2 = 0
    count_5 = 0
    while n%2==0:
        count_2+=1
        n//=2
    while n%5==0:
        count_5+=1
        n//=5
    return [count_2, count_5], n%10

def generate_multipliers(dd, lenl):
    # takes time linear in lenl
    # (dd + i choose i) % 10 for i in 0..lenl-1
    print("generating multipliers")
    print("partially factorizing all the numbers from %d to %d..." % (dd, dd+lenl))
    print("this may take a few seconds")
    # Combinations are integers -- no factor will ever drop below 0
    # store the current factor of 2 and 5 as a counter
    # store all other odd factors as single integer
    # compute inverse mod 10 to divide
    twos_fives = [0, 0]  # n-1 choose t-1
    odd = 1
    multipliers = [1]
    for t in range(1,lenl):
        n = dd+t
        tf_n, odd_n = dfactor(n)
        tf_t, odd_t = dfactor(t)
        # modular inverse of odd_t
        twos_fives[0] += tf_n[0] - tf_t[0]
        twos_fives[1] += tf_n[1] - tf_t[1]
        v = ((2**twos_fives[0]) * (5 if twos_fives[1] else 1))%10
        # 5**k == 5 mod 10
        # Now the odd part mod 10:
        odd *= odd_n * (10-odd_t if odd_t==3 or odd_t==7 else odd_t)
        odd %= 10
        multipliers.append((v*odd)%10)
        if t%10000==0:
            print(t,'/',lenl)
    print("Generated multipliers")
    return multipliers

def part2b(l):
    lenl = len(l)
    dd= dist-1
    multipliers = generate_multipliers(dd, lenl)
    # generate (99+i choose i)  for reverse cumulative sum
    res = [sum(x*m for x, m in zip(l[i:], multipliers))%10 for i in range(8)]
    print("Final result:")
    print(''.join(map(str, res)))

def generate_e(r):
    pi= list(map(int, "31415926"))
    e = list(map(int, "27182818"))
    # diff we want:
    # + 16777992
    offset = int(r[:7])
    orig_lenl = len(r)
    orig_l = list(map(int, r))
    lenl = (orig_lenl * 10000) - offset
    dd = dist-1
    multipliers = generate_multipliers(dd, lenl)
    assert len(multipliers) == lenl > orig_lenl
    # we want to find some positions in our input
    # that we can influence, so that we can change
    # the value of our result.
    # taking lenl, dd, multipliers as constant:
    # the influence is (should be) only based on multipliers.
    # increasing orig_l[-1] by 1:
    # increases l[-1] by 1, l[-1-orig_lenl] by 1...  (period is orig_lenl)
    # increases res[-1] by multipliers[0]
    # increases res[-2] by multipliers[1]
    # increases res[-1-orig_lenl] by multipliers[0]+multipliers[orig_lenl]
    # increases res[-orig_lenl] by multipliers[orig_lenl-1]
    # increases res[~x] by sum(multipliers[x%orig_lenl:x+1:orig_lenl])
    # increasing orig_l[-2] by 1
    # if orig_l is [1,2,3,4]
    # rep is 4: l = [0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3]
    # offset is 9: l = [1,2,3,0,1,2,3]
    # multipliers are [a,b,c,d,e,f,g]
    # our results are:
    # a+2b+3c+0d+...
    #   2a+3b+0c+...
    #      3a+0b+...
    #              3a
    # we expect adding 1 to l[1]==1 will increase res[0] by a+e
    # and it will increase res[1] by d, res[2] by c, res[3] by b, res[4] by a, others by 0
    pass
    mul2 = multipliers[:]
    np = orig_lenl  # wrap multipliers
    while np < lenl:
        nmul = [0]*np + mul2[:-np]
        mul2 = [(a+b)%10 for a,b in zip(mul2, nmul)]
        np *= 2
    print(mul2[:16])
    print(mul2[-16:])
    # l = (orig_l*10000)[offset:]
    # # quadratic in lenl
    # res0 = [sum(x*m for x, m in zip(l[i:], multipliers)) % 10 for i in range(lenl)]
    # print("check res0: first 8 are:", ''.join(map(str, res0[:8])))
    # diff_guess = [sum(multipliers[x%orig_lenl:x+1:orig_lenl])%10 for x in range(lenl)][::-1]
    # print(diff_guess[:16])
    # print(diff_guess[-16:])
    excl = {}
    for i in [6]: #range(8, orig_lenl):  # don't modify our offset (-> lenl)
        l = orig_l[:]
        l[i]+=1 # l[i] TODO
        l = (l*10000)[offset:]
        # if
        res = [sum(x*m for x, m in zip(l[i:], multipliers)) % 10 for i in range(8)]
        print("position %5d:  res %s" % (i, res))
        # full res has length: lenl
        diff = [(a-b)%10 for a,b in zip(res, pi)]  # the difference it made
        print("position %5d: diff %s" % (i, diff[::-1]))
        # res[0-lenl], res[1-lenl],...
        # guess = [sum(multipliers[~i::-orig_lenl]) for i in range(8)]
        # print("guess:   %5s       %s" % ('',guess))
        # excl[i] = res2



class my_counter(Counter):
    def __mul__(self, i):
        return my_counter({k: v*i for k, v in self.items() if i})
    def __add__(self, other):
        return my_counter(Counter.__add__(self, other))
    def __mod__(self, other):
        # clear the ones that are 0
        return my_counter({k: v%other for k, v in self.items() if v%other})

# cl = ([my_counter({i:1}) for i in range(len(r))]*10000)[offset:]
# part2b(l)
generate_e(r)