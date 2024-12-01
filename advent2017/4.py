
# (2024) moved input data (originally included as multiline string)
s=open("4.in").read().strip().split('\n')

print "part 1:",
l = lambda b: (lambda s:sorted(set(s))==sorted(s))(b.split())
l = lambda b: (lambda s:len(set(s))==len(s))(b.split())

print sum(map(l,s))


print "part 2:",

s = [[[word.count(chr(97+x)) for x in range(26)] for word in row.split()] for row in s]

l = lambda row: all(row.count(x)==1 for x in row)

print sum(map(l,s))

