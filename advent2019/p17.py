
from intcode import Intcode

with open('input.txt', 'r') as f:
    r = f.read().strip()
    code = eval('[' + r + ']')

comp = Intcode(code)
comp.run()
out = ''.join(map(chr, comp.q_out))
grid = out.strip().split('\n')
# print(out)

# ints = [(x,y) for y in range(1, len(grid)-1) for x in range(1, len(grid[0])-1)
#         if grid[y-1][x]==grid[y+1][x]==grid[y][x-1]==grid[y][x+1]==grid[y][x]=='#'
#         ]
# print("part 1:", sum(x*y for x,y in ints))

# using editor duplicate-line to type faster:
print(sum(x*y for y in range(1, len(grid)-1) for x in range(1, len(grid[0])-1)
          if '#'
          == grid[y][x]
          == grid[y-1][x]
          == grid[y+1][x]
          == grid[y][x-1]
          == grid[y][x+1]
          ))
# Part 2
# Solved manually / By inspection (tracing from the starting point and looking for patterns):
# L, 12, R, 4, R, 4,  A
# R, 12, R, 4, L, 12, B
# R, 12, R, 4, L, 12, B
# R, 12, R, 4, L, 6, L, 8, L, 8, C
# R, 12, R, 4, L, 6, L, 8, L, 8, C
# L, 12, R, 4, R, 4, A
# L, 12, R, 4, R, 4, A
# R, 12, R, 4, L, 12, B
# R, 12, R, 4, L, 12, B
# R, 12, R, 4, L, 6, L, 8, L, 8 C
#
# Note this will only work for my input
ascii_in = b"""A,B,B,C,C,A,A,B,B,C
L,12,R,4,R,4
R,12,R,4,L,12
R,12,R,4,L,6,L,8,L,8
n
"""
def in_f():
    # yield from ascii_in
    for i in ascii_in:
        print(chr(i), end='')  # give the semblance of interactivity
        yield i
code[0] = 2
comp = Intcode(code, input_src=in_f(), output_func=lambda i:print(chr(i), end='') if i < 256 else print(i))
comp.run()
print("^^^^^^ Part 2")
