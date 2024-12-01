import sys
from math import prod


lines = [line.strip() for line in sys.stdin]
w = len(lines[0])

trees = [sum(line[(d*i)%w]=="#" for i,line in enumerate(lines))
         for d in [1,3,5,7,]]
trees.append(sum(line[(i//2)%w]=="#" for i,line in enumerate(lines) if i%2==0))
print(trees[1])
print(prod(trees))
