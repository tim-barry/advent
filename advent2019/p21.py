
from intcode import AsciiIntcode
import sys

with open("input21.txt") as f:
    r = f.read().strip('\n')
cc = eval('['+r+']')


def in_f(part):
    if part==1:
        yield from b"""\
NOT A J
NOT C T
AND D T
OR T J
WALK
"""
        """
Explanation: We jump when
 - we must (.xxx), or
 - we can jump over a gap like xx.# 
        """
    else:
        # part 2
        yield from b"""\
NOT A J
NOT C T
NOT T T
AND B T
NOT T T
AND D T
AND H T
OR T J
RUN
"""
        """Explanation
Same as part 1, but:
Also jump across #.## gaps
Only jump across a #??# gap if we can jump again immediately
If we can't jump again (no H) then E must be walkable
so we can just continue and jump at the next position."""
    while 1:
        yield from input().encode('ascii')
        yield 10

AsciiIntcode(cc, in_f(1)).run()
AsciiIntcode(cc, in_f(2)).run()
