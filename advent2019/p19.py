
from intcode import Intcode

with open('input.txt', 'r') as f:
    r = f.read().strip()
    cc = eval('['+r+']')

def is_pull(p):
    return Intcode(cc, q_in=list(p)).run()

test="""
#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########""".strip().split('\n')
# def is_pull(p):
#     return test[p[1]][p[0]]!='.'
# square_size = 9
# ^ test for part 2

# part 1:
# print(sum(is_pull([x,y]) for x in range(50) for y in range(50)))

# grid = [[0]*y+[is_pull([x,y]) for x in range(y, int(y*1.3)+5)] for y in range(200)]
# for row in grid:
#     print(''.join(" #"[v] for v in row))

p = [800,800]  # estimate
# p is upper left (lower left) corner of square (on edge of beam with higher y position)
# move p to the tractor beam
while not is_pull(p):
    p[0]+=1  # by inspection, x>y for points on the tractor beam

square_size = 99  # it's inclusive!!!!!! <this was the hardest part
def makes_square(p, d=square_size):
    return is_pull([p[0] + d, p[1] - d])

# track along the higher(y) edge
while not makes_square(p):
    # move p out of beam(maybe) (up, +y) and then back into beam(right, +x)
    p[1]+=1
    while not is_pull(p): p[0]+=1
print(p[0] * 10000 + p[1] - square_size)
