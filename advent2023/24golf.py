from sympy import*
E=[[t:=var(str(c),positive=1),c+f*t,a+d*t,b+e*t]for a,b,c,d,e,f in[eval(l.replace(*'@,'))for l in open(0)]]
P=var(":6")
print(sum(a.subs(S)//2e14==b.subs(S)//2e14==1for*_,a,b in E for*_,c,d in E if(S:=solve([a-c,b-d])))//2,sum(map(solve(p+v*t-x for t,*e in E[:3]for p,v,x in zip(p,p[3:],e))[0].get,p[:3]))