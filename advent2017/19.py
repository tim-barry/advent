
f=open("19.in",'r')
s=f.read().split("\n")
f.close()


def getnx(d,x,y):
	if d=="d":
		y+=1
	elif d=="u":
		y-=1
	elif d=="l":
		x-=1
	elif d=="r":
		x+=1
	return x,y

y = 0
x = s[0].find("|")

letters=""
d = "d"
steps = 0
while True:
	steps+=1
	curr_c = s[y][x]
	if curr_c not in "|+-":
		letters += curr_c
	if curr_c=="+": #assume always turn
		for poss_d in "dulr":
			if d!="dulr"["dulr".find(poss_d)^1]: # if not back same way
				t_x,t_y = getnx(poss_d,x,y)
				if s[t_y][t_x]!=" ": #continues in this direction
					d = poss_d
					break
	x,y = getnx(d,x,y)
	if s[y][x]==" ": #end
		break

print letters
print steps
