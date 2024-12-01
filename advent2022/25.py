
f = "input25.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

def snafu(n):
    if n==0: return ''
    dig = n%5
    res = n//5
    c = "012=-"[dig]
    if dig>2:
        res+=1
    return snafu(res)+c

def unsnafu(s):
    if len(s)==0: return 0
    return 5*unsnafu(s[:-1]) + "=-012".find(s[-1])-2

res = sum(map(unsnafu, lines))
print(snafu(res))


