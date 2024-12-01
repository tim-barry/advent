
with open('input2.txt') as f:
    r = f.read().strip()

ol=eval('['+r+']')
# ol = [int(s) for s in r.split(',')]

for a in range(100):
    for b in range(100):
        l = ol[:]
        i = 0
        l[1] = a
        l[2] = b
        while 1:
            c = l[i]
            if c==1:
                t=l[l[i+1]]+l[l[i+2]]
                l[l[i+3]] = t
            elif c==2:
                t=l[l[i+1]]*l[l[i+2]]
                l[l[i+3]] = t
            elif c==99:
                break
            else:
                print("err!")
            i+=4
        if a==12 and b==2:
            print(l[0])  # part 1
        if l[0]==19690720:
            print(100*a+b)  # part 2
