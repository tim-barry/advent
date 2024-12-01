
f="test25.txt"
f="input25.txt"
grid = [list(line.strip()) for line in open(f)]

W = len(grid[0])
H = len(grid)

print(f"{W=:}, {H=:}")
def step(g):
    #east
    moved=False
    for y in range(H):
        r0 = g[y][0]
        skip=False
        for x in range(W):
            if skip:
                skip=False
            elif g[y][x]==">":
                if x+1==W:
                    if r0==".":
                        g[y][0]=">"  #rotate
                        g[y][x]="."
                        moved=True
                elif g[y][x+1]==".":
                    g[y][x+1]=">"  #move
                    g[y][x]="."
                    moved=True
                    skip=True
                    #print(f"moved E at {y=:},{x=:}")
    #printg(g)
    #south
    for x in range(W):
        r0 = g[0][x]
        skip=False
        for y in range(H):
            if skip:
                skip=False
            elif g[y][x]=="v":
                if y+1==H:
                    if r0==".":
                        g[0][x]="v"  #rotate
                        g[y][x]="."
                        moved=True
                elif g[y+1][x]==".":
                    g[y+1][x]="v"  #move
                    g[y][x]="."
                    moved=True
                    skip=True
                    #print(f"moved S at {y=:},{x=:}")
    return moved

def printg(g): print('\n'.join(''.join(line) for line in g))

#printg(grid)
i = 0
while 1:
    #input()
    i+=1
    if step(grid)==False:
        print(i)
        #printg(grid)
        break
    #printg(grid)


