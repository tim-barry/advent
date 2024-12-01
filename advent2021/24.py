
lines = [line for line in open("input24.txt")]


def red(i):
    l = []
    while i>=26:
        l.append(i%26)
        i//=26
    l.append(i)
    return l[::-1]

def res(s,debug=False):
    reg={"x":0, "y":0, "z":0,"w":0}
    i=0 #input index
    #print("s is:",s)
    for line in lines:
        if line[:3] in {"inp", "mul", "add", "div", "mod", "eql"}:
            l = line.strip().split()
            if l[0]=="inp":
                reg[l[1]]=int(s[i])
                i+=1
                if debug: print(red(reg['z']))
            elif l[0]=="mul":
                reg[l[1]]*= reg.get(l[2], int(l[2]) if l[2] not in "wxyz" else None)
            elif l[0]=="add":
                reg[l[1]]+= reg.get(l[2], int(l[2]) if l[2] not in "wxyz" else None)
            elif l[0]=="div":
                reg[l[1]]//= reg.get(l[2], int(l[2]) if l[2] not in "wxyz" else None)
            elif l[0]=="mod":
                reg[l[1]]%= reg.get(l[2], int(l[2]) if l[2] not in "wxyz" else None)
            elif l[0]=="eql":
                reg[l[1]]= reg[l[1]]==reg.get(l[2], int(l[2]) if l[2] not in "wxyz" else None)
    return reg['z']


def zero_in(r):
    return [i for i in r if "0" not in str(i) and res(str(i))==0]



