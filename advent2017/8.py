#(2024) moved input data (was included as multiline string)
s=open("8.in").read().strip().split('\n')

lines = s
#lines = data.strip().split('\n')
d = {}
tmax = 0
for line in lines:
	a,b = line.split(" if ")
	b = b.split()
	if eval("d.get(b[0],0)" + b[1] + b[2]): #offload logic onto python
		a = a.split()
		if a[1]=="inc":
			d[a[0]] = d.get(a[0],0)+ int(a[2])
		else:
			d[a[0]] = d.get(a[0],0)- int(a[2])
		if d[a[0]]>tmax: # part 2
			tmax = d[a[0]]

print max(d.values())
print tmax # part 2

