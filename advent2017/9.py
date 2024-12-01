

f=open("9.in",'r')
s=f.read().strip()
f.close()


i = 0
garbage = False
gchar = 0            #part 2
group_sum = 0
current_group_num = 0
while i<len(s):
	if s[i]=="!":
		i+=1 #skip next
	elif garbage:
		if s[i]==">":
			garbage = False
		else:
			gchar+=1 #part 2
	elif s[i]=="{":
		current_group_num+=1
		group_sum+=current_group_num
	elif s[i]=="}":
		current_group_num-=1
	elif s[i]=="<":
		garbage = True
	i+=1

print group_sum #part 1
print gchar     #part 2

