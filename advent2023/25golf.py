from collections import*
from random import*
g=defaultdict(list)
for a,*l in[l.replace(*": ").split()for l in open(0)]:
 g[a]+=l
 for t in l:g[t]+=[a]
p={k:choices([0,1],k=9)for k in g}
for _ in 'a'*30:p={k:[x/5+.8*sum(L)/len(L)for x,*L in zip(p[k],*[p[K]for K in g[k]])]for k in p}
L,*_,H=sorted(p.values(),key=sum)
print((X:=sum(sum(p[k])<sum(L+H)/2for k in p))*(len(p)-X))
