
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

f = "input07.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

from functools import cmp_to_key

# kind of garbage

def kind(hand):
    # hand type is equivalent to most_common() and sorts the same
    return [t[1] for t in Counter(hand).most_common()]

def sort_key(handbid):
    return (kind(handbid[0]), handbid)

#rename the cards so that they sort lexicographically
hands = [(a.replace("A","~").replace("K","z").replace("Q", "y").replace("J", 'x'), int(b))
         for line in lines for a,b in [line.split()]]
shands = sorted(hands, key=sort_key)
wins = sum([(i+1)*bid for (i, (_,bid)) in enumerate(shands)])
print(wins)

def kind2(hand):
    C = Counter(hand)
    jokers = C['!']
    if jokers==5: return [5] #fivekind
    if jokers==0: return kind(hand)
    del C['!']
    mcommon = C.most_common(1)[0][0]
    C[mcommon] += jokers
    return [t[1] for t in C.most_common()]

def key2(handbid):
    return (kind2(handbid[0]), handbid)

#Again rename the cards but this time ensure 'J' < '2'
hands2 = [(a.replace("A","~").replace("K","z").replace("Q", "y").replace("J", '!'), int(b))
         for line in lines for a,b in [line.split()]]
shands2 = sorted(hands2, key=key2)
wins = sum([(i+1)*bid for (i, (_,bid)) in enumerate(shands2)])
print(wins)


