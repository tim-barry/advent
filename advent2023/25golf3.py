g={};L=len
for l in open(0):
 for b in l[4:].split():exec("b,l=l[:3],b;V=P={b};g[l]=g.get(l,P)|P;"*2)
while L(P:=(P|g[b])-V)>3:V|={b:=max((L(g[c]&V),c)for c in P)[1]}

# P-{b}  ^ g[b]-P - V
exit()

while 1:
    P={a for v in V for a in g[v]}-V
    O={(v,a)for v in V for a in g[v] if{a}-V}
    if len(O)==3:break
    choices = {a for v,a in O}
    cost = 500
    ch = None
    for c in P:
        dout = len(g[c]) - 2*len([v for v in g[c] if v in V])
        nout = len(O) + dout
        if nout < cost:
            ch = c
            cost = nout
    V|={ch}
print(len(V)*(len(g)-len(V)))
