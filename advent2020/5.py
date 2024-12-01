
with open("5.txt") as f:
    lines = [l.strip() for l in f]

seats = [int(l[:-3].replace("F","0").replace("B","1"), 2)*8
         + int(l[-3:].replace("R","1").replace("L","0"), 2)
         for l in lines]

print(max(seats))
print(list(set(range(min(seats),max(seats)))-set(seats))[0])

