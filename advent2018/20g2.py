P={0};M={0:P-P};S=[]
for c in raw_input()[1:-1]:exec['S+=P|P,P-P','P|=S.pop();S.pop()','S[-1]|=P;P^=P^S[-2]',
'for p in P|P:n=p+1j**"ESW".find(c);M[p]|={n};M[n]=M.get(n,P-P)|{p};P^={n,p}']["()|".find(c)]
Q={0};V={0}
while Q:Q={n for p in Q for n in M[p]}-V;V|=Q;S+=len(Q),
print~-len(S),"\n",sum(S[999:])

I had a lot of fun golfing and then forgot to submit it... Python 2 and solved the general case in 320 bytes (no exec, 303 using betaveros's exec trick).

Before I thought of complex numbers I wrote a program that would search all possible arithmetic/logical expressions to find one that could convert a direction (NESW, 0 to 3 or as I ended up using, -1 to 2) into dx/dy components. (the expressions were 'd/2' and '1-d%-3')

I keep a dictionary of which other positions are reachable from this position. First I build the map M (in the for loop) using a stack S (for groups), then find the number of rooms at increasing distances (and add that to a list S.)
There are a bunch of tricks using sets, like using P-P to create a new empty set
and P|P to create a copy of P, and general abuse of set operations;
using the fact that str.find returns -1 if not found to cut a character out of NESW,
being able to remove a space by writing ~-len(S) instead of len(S)-1.
In general removing whitespace was very valuable.
Removing the defaultdict import also saved quite a bit of space.
