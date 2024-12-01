import sys

lines = sys.stdin
pspw = [l.split(": ") for l in lines]
def match(t):
    ps, pw=t
    ct, c = ps.split(' ')
    m, M = map(int, ct.split('-'))
    # return m<=pw.count(c)<=M  # part 1
    return (pw[m-1]==c) ^ (pw[M-1]==c)  # part 2

match_cnt = sum(map(match, pspw))
print(match_cnt)
