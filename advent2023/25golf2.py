from random import*
g={};S=sum
for a,*B in[l.split()for l in open(0)]:
 for b in B:g[b]=g.get(b,[])+[k:=a[:3]];g[k]=g.get(k,[])+B
p={k:choices([0,1],k=9)for k in g}
for _ in'a'*99:p={k:[x+S(L)/len(L)for*L,x in zip(*[p[K]for K in g[k]+[k]])]for k in p}
L,*_,H=sorted(p.values(),key=S)
print((X:=S(S(p[k])<S(L+H)/2for k in p))*(len(p)-X))