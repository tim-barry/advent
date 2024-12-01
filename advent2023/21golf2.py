k,N,K=202300,131,393
I={i//132*K+i%132for i,c in enumerate(open(0).read())if'$'<c}
L=1,K,-1,-K
J={t+N*u for t in I for u in L}
e=lambda t,S=I:len(eval("{p+d for p in"*t+"{25610}"+" for d in L}&S"*t))
print(e(64),~-k*(k*e(132)+k*e(N:=131)-e(65))+k*e(196,J))