*S,e=open(0).read()+999*'$'
i=A=B=0
f=8645,
while f:
 *f,s=f,;i+=1;t=i>66;T=202301^i&1
 for k in s:
  if e<S[k]:S[k]=e;A+=t<i&1;B+=T*(T^t);f+=k+132,k-132,k+1,k-1
print(A,B)