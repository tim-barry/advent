
import string
from collections import deque,defaultdict,Counter
from functools import reduce
from itertools import batched, starmap, accumulate, pairwise
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall(r'-?\d+',s))

f = "input.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

from functools import cmp_to_key

# kind of garbage

tlines = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".split('\n')

def kind(hand):
    L = len(set(hand))
    if L==5: return 1  #high card: last
    if L==1: return 10 #five of kind
    C = Counter(hand)
    if L==2:
        if C[hand[0]] in [1,4]: # four of a kind
            return 9
        return 8  # full house
    if L==3:
        if C.most_common(1)[0][1]==2:  # only pairs
            return 3  # 2 pair
        else: # three of kind
            return 4
    else:
        return 2  #one pair: 2nd last

def betterhand(a,b):
    a,b = a[0],b[0]
    ka = kind(a)
    kb = kind(b)
    # print(ka, kb)
    if (ka == kb):
        # print("same kind:", a,b)
        return (a>b) - (a<b)
    else:
        return (ka>kb) - (ka<kb)

hands = [(a.replace("A","~").replace("K","z").replace("Q", "y").replace("J", 'x'), int(b))
         for line in lines for a,b in [line.split()]]
shands = sorted(hands, key=cmp_to_key(betterhand))
wins = sum([(i+1)*bid for (i, (_,bid)) in enumerate(shands)])
print(wins)

def kind2(hand):
    C = Counter(hand)
    jokers = C['!']
    if jokers==5: return 10 #fivekind
    if jokers==0: return kind(hand)
    del C['!']
    mcommon = C.most_common(1)[0][0]
    # 2 2 1joker : fullhouse (yes)
    # 3 1 1joker: 4 of kind
    # 3 2joker: 5
    # 2 1 2joker: 4 of kind
    #1 1 1 2joker: 3kind
    # 2 1 1 1joker : 3kind
    # 1 1 1 1 1joker: 1pair
    # 2 3joker: 4 of kind
    C[mcommon] += jokers
    if C[mcommon]==5: return 10
    if C[mcommon]==4: return 9 #fourkind
    if C[mcommon]==3:
        if len(C) == 2: return 8 #house
        return 4 #3kind
    if len(C)==3: return 3 #2pair
    return 2  #one pair: 2nd last

def betterhand2(a,b):
    a,b = a[0],b[0]
    ka = kind2(a)
    kb = kind2(b)
    if (ka == kb):
        return (a>b) - (a<b)
    else:
        return (ka>kb) - (ka<kb)

hands2 = [(a.replace("A","~").replace("K","z").replace("Q", "y").replace("J", '!'), int(b))
         for line in lines for a,b in [line.split()]]
shands2 = sorted(hands2, key=cmp_to_key(betterhand2))
print(shands2[-10:])
wins = sum([(i+1)*bid for (i, (_,bid)) in enumerate(shands2)])
print(wins)

