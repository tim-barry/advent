from collections import deque

"""
# old debugging function
def printl(l,cur):
	print (" " + "  ".join(map(str,l)) + " ").replace(" %d "%l[cur],"(%d)"%l[cur])
"""

# rewritten code
# eventually gave up on part 2 and checked reddit:
# first answer used deque.rotate - immediately facepalmed
# otherwise basically same solution (only direction of rotates different)

def place_marble(l,marble): # return score
	if marble%23==0:
		l.rotate(-7)
		return marble + l.pop()
	l.rotate(2)
	l.append(marble)
	return 0

def game(players,last_marble):
	scores = [0]*players
	circle = deque([0])
	for marble in xrange(1,last_marble+1):
		scores[marble%players] += place_marble(circle,marble)
	return max(scores)

# for part 2, was absolutely destroyed by O(N^2) time complexity
# and I didn't know deque had a 'rotate' function (hhhhhh)
# which basically makes the problem trivial

print game(1,40) # 32
print game(10,1618) # 8317
print game(13,7999) # 146373
print game(462,71938) # part 1
print game(462,7193800) # part 2 - need deque for O(1) insert/remove
