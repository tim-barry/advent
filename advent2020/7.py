
from collections import Counter

test="""
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".strip()


with open("7.txt") as f:
    lines = [l.strip() for l in f]

d = {}
for line in lines:
    line = line.rstrip('.')
    x, conts = line.split(" bags contain ")
    conts = [ct.rstrip('bags').strip() for ct in conts.split(", ")]
    if conts[0]=="no other":
        conts = Counter()
    else:
        conts = Counter({' '.join(ct.split()[1:]):int(ct.split()[0]) for ct in conts})
    d[x] = conts

# from pprint import pprint
# pprint(d)

goal = "shiny gold"
s = set()
ps = None
while s!=ps:
    ps = s
    s = s | {x for x in d if any(t in d[x] for t in s|{goal})}
print(len(s))

def tot(b):
    c = d[b]
    return sum(tot(bb)*c[bb] for bb in c)+1
print(tot("shiny gold")-1)

