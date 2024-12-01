
t1 = """
....#
#..#.
#..##
..#..
#....
""".strip()

"""
My optimized Python solution: [paste](https://topaz.github.io/paste/#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),
and [port to zig 0.4.0 (tio.run)]()

Storing each layer as 75 bits instead of 25 bits allows us to simply sum the neighbour count in-place,
saving a for loop with some bit twiddling.

"""

# use 75-bit integers to store state (3 bits per cell)
# so that we can replace a for loop with some adds/shifts/masks
# you may encounter problems shifting by > 31 using some languages
# make sure your intermediate types are wide enough!

left_mask  = sum(1<<(i*15) for i in range(5))
right_mask = left_mask<<12
high_mask  = sum(1<<(i*3) for i in range(5))
low_mask   = high_mask<<60
bug_mask   = high_mask * left_mask

the_middle = 1<<(12*3)
mids       = [7*3, 11*3, 13*3, 17*3]
masks      = [high_mask, left_mask, right_mask, low_mask]
mask_mid   = list(zip(masks, mids))

# compress cell width from 3 to 1 -- implement the select operator (bi~bug_mask)
def b3_to_biodiversity(bi): return sum((bi>>(3*i) & 1)<<i for i in range(25))
def popcnt(x): return bin(x).count('1')
def countbugsb(b): return sum(popcnt(bi) for bi in b)

# Debug
def printbi(bn):
    print("\n".join(''.join('.#'[bn>>(3*i) & 1]
                            for i in range(t,t+5))
                    for t in range(0,25,5)))
def printbn(bn):  # debug: print neighbour count
    print("\n".join(''.join(str(bn>>(3*i) & 0b111)
                            for i in range(t,t+5))
                    for t in range(0,25,5)))
def printb(b):
    for l in sorted(b.keys()):
        print(f"Level {l}:")
        printbi(b[l])
        print()


def neighbours(layer):
    # shift down/left/right/up (with masks to avoid wrapping) for same-level adjacency
    shu = layer>>15
    shl = (layer&~left_mask)>>3
    shr = (layer&~right_mask)<<3
    shd = (layer&~low_mask)<<15
    return shu+shl+shr+shd

def next_state(layer, neigh):
    count1 = neigh & ~neigh>>1 & ~neigh>>2 & bug_mask  # cell == 001
    count2 = ~neigh & neigh>>1 & ~neigh>>2 & bug_mask  # cell == 010
    return count1 | (count2 & ~layer)

def next_state2(layer, neigh):  # 30% faster version (timeit), equivalent (de morgan)
    t = ~neigh>>1
    return (~neigh>>2 & bug_mask) & ((neigh&t)|~(neigh|t|layer))

def advance_layer_part1(layer):
    return next_state(layer, neighbours(layer))

def advance_layer_part2(layer, inner, outer):
    # get from inner (+1) and outer (-1) levels
    in_out = sum((popcnt(inner & mask)<<mid)
                 + mask*(outer>>mid & 1)
                 for mask, mid in mask_mid)
    # avoid 3-bit overflow in cells next to inner by setting cell = min(cell, 3)
    in_out |= ((in_out>>2)&bug_mask)*0b11
    in_out &= bug_mask|bug_mask<<1
    total_neighbours = neighbours(layer) + in_out  # add w/o overflow
    new_bugs = next_state(layer, total_neighbours) & ~the_middle
    return new_bugs

def advance_state_part2(b):
    lo, hi = min(b)-1, max(b)+1
    nb = {i: advance_layer_part2(b.get(i,0), b.get(i+1,0), b.get(i-1,0))
          for i in range(lo,hi+1)}
    if not nb[lo]: del nb[lo]  # ignore zeros
    if not nb[hi]: del nb[hi]
    return nb

def part1(start):
    cur = start
    seen = set()
    mins = 0
    while cur not in seen:
        seen.add(cur)
        cur = advance_layer_part1(cur)
        mins+=1
    return b3_to_biodiversity(cur), mins

def part2(start, minutes=200):
    bg = {0: start}
    for t in range(minutes):
        bg = advance_state_part2(bg)
    return countbugsb(bg.values())

if __name__ == '__main__':
    with open("input24.txt") as f:
        r = f.read().strip()

    start_state = sum((c=='#')<<(3*i)
                      for i, c in enumerate(c for c in r if c in '#.'))
    repeated, mins = part1(start_state)
    print(f"Part 1: repeated biodiversity is {repeated} after {mins} minutes")
    print(f"Part 2: number of bugs is {part2(start_state)} after 200 minutes")


# Can't do part 3 with current implementation
# O(n) in number of levels to calculate next state
# --> O(n^2) in total number of minutes
# even O(n) likely too long for 525948766245 (500 billion)

def part3():
    seen = []
    bg = {0: start_state}
    mins = 0
    # -7: 24,25,22,27,24,29,22,31  starting at 30=22,31=31,32=24...
    # -8: 28,29,30,31,32,33,34,35  28-35
    # -9: 32-39
    # -10:  36-43 except 45 instead of 37
    # -11:  40-47 except 49 instead of 41
    # -12:  46-53
    # -13:  48-55 except 57 instead of 49
    # basic idea:
    # as they expand away they become periodic so
    # we add them to the running total and then stop keeping track of them.
    # only update the centre ~50 ish?
    # can obtain ~linear time to look for patterns in the centre
    while mins<100:
        check_i = (mins//2) - 13
        if bg.get(check_i,0) in seen:
            print(f"minute {mins} is a repeat"
                  f" of minute {seen.index(bg.get(check_i,0))}")
        seen.append(bg.get(check_i,0))
        bg = advance_state_part2(bg)
        mins+=1
    # print(f"repeated after {mins} minutes")
    tbg = {k:bg[k] for k in [-1,0,1]}
    printb(tbg)
    # print(countbugsb(bg))

