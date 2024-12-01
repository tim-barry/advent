
# 19/18

def valid(x):
    x=str(x)
    # part 1:
    # return list(x)==sorted(x) and any(x[i]==x[i+1] for i in range(5))
    # part 2:
    return list(x)==sorted(x) and any(x[i]==x[i+1] and (i==0 or x[i-1]!=x[i]) and (i==4 or x[i+2]!=x[i]) for i in range(5))

a,b = 356261,846303
print sum(1 for x in range(a,b) if valid(x))

