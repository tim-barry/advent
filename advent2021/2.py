
f = "input2.txt"

with open(f) as r:
    lines = r.readlines()

def move(pos,action):
    if action[0]=="forward":
        return pos[0]+int(action[1]), pos[1]
    if action[0]=="down":
        return pos[0], pos[1]+int(action[1])
    if action[0]=="up":
        return pos[0], pos[1]-int(action[1])
    else:
        raise RuntimeError("bad action: " + action[0])

def move2(pos, action):
    i = int(action[1])
    if action[0]=="forward":
        return pos[0]+i, pos[1]+i*pos[2], pos[2]
    if action[0]=="down":
        return pos[0], pos[1], pos[2]+i
    if action[0]=="up":
        return pos[0], pos[1], pos[2]-i
    else:
        raise RuntimeError("bad action: " + action[0])

def moves(pos,actions, mover):
    for act in actions:
        pos = mover(pos,act)
        #print(pos)
    return pos

allmoves = [line.strip().split() for line in lines]

pos = 0,0
end = moves(pos, allmoves, move)
print(end[0]*end[1])

pos = 0,0,0
end = moves(pos, allmoves, move2)
print(end[0]*end[1])

