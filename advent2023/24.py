
import string
from collections import deque,defaultdict,Counter
from functools import reduce
from itertools import batched, starmap, accumulate, pairwise
import re
def lmap(f,l): return list(map(f,l))
# tbl_digits = str.maketrans(string.punctuation, ' '*len(string.punctuation))
# tbl_signed = str.maketrans(string.punctuation.replace('-',' '), ' '*len(string.punctuation))
# def ints2(s: str): return lmap(int, s.translate(tbl_digits).split())
def ints(s: str): return lmap(int,re.findall(r'-?\d+',s))

f = "input.txt"

with open(f) as r:
    s = r.read() .rstrip()
    lines = s.split('\n')
    lgroups = s.split('\n\n')

test = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

#pxyz, vxyz
test_area = 200000000000000, 400000000000000

# lines = test.split('\n')
# test_area = 7,27

st = lmap(ints, lines)

from math  import *
PI = pi

parallel = None
total = 0
for i in range(len(st)):
    vi = st[i][3:5]
    pi = st[i][:2]
    for j in range(i+1,len(st)):
        vj = st[j][3:5]
        pj = st[j][:2]
        # print(i,j,pi,pj,vi,vj)
        ai = atan2(vi[1],vi[0])
        aj = atan2(vj[1],vj[0])
        if ai<0: ai += PI
        if aj<0: aj += PI
        if ai==aj:
            parallel = (i,j)
            # print(i,j,vi,vj,"parallel")
            pass
        else:
            # if st[i][3]/st[i][5]==st[j][3]/st[j][5]:
            #     print(i, j, st[i], st[j], "parallel x/z")
            # if st[i][4]/st[i][5]==st[j][4]/st[j][5]:
            #     print(i, j, st[i], st[j], "parallel y/z")
            if not all(vi+vj): # one is vertical
                print("Axis!")
            #for particles 0,1 should obtain: t=2.333,  u = 3.666
            # at time t, particle 0 is at position t*vi + pi
            # t*vi.y + pi.y = u*vj.y + pj.y
            # t = (u*vjy + pjy - piy) / viy
            # ((u*vjy + pjy - piy) / viy) * vi.x + pi.x = u*vj.x + pj.x
            # u*  ( (vjy/viy)*vi.x -vj.x ) = pj.x - pi.x - (pjy - piy)/viy*vi.x
            u_denom = (vj[1]*vi[0]/vi[1]) - vj[0]
            u_num = pj[0] - pi[0] - (pj[1] - pi[1])*vi[0]/vi[1]
            u = u_num / u_denom
            t = (vj[1]*u + pj[1]-pi[1]) /vi[1]
            # print(i,j,f"{t=},{u=}")
            x = vj[0]*u + pj[0]
            y = vj[1]*u + pj[1]
            # print(x,y)
            if test_area[0]<=x<=test_area[1] and test_area[0]<=y<=test_area[1]:
                if t>=0 and u>=0:
                    total += 1
            else:
                pass

print(total)

# there is a parallel pair in (x,y) [not in z], but they go opposite directions
#

# use 3 particles to determine path?
# hit particle a at time t, b at time u, c at time w
# va*t + pa = V*t + P
# vb*(t+du) + pb = V*du + va*t + pa
# t*(vb-va) + du(vb-V) = pa-pb

# (va-V)*t = P-pa

# (va-V)*t = P - pa
# (vb-V)*u = P - pb
# (vc-V)*w = P - pc

from sympy import solve
# velocity, intersection times, position
from sympy.abc import a,b,c, t,u,v,w, x,y,z
syms = [a,b,c,t,u,v,x,y,z]
eqs = [
    st[0][0] + st[0][3] * t - a * t - x,  # px0 + vx0*t = Vx*t + Px
    st[0][1] + st[0][4] * t - b * t - y,
    st[0][2] + st[0][5] * t - c * t - z,
    st[1][0] + st[1][3] * u - a * u - x,
    st[1][1] + st[1][4] * u - b * u - y,
    st[1][2] + st[1][5] * u - c * u - z,
    st[2][0] + st[2][3] * v - a * v - x,
    st[2][1] + st[2][4] * v - b * v - y,
    st[2][2] + st[2][5] * v - c * v - z,
    # st[3][0] + st[3][3] * w - a * w - x,
    # st[3][1] + st[3][4] * w - b * w - y,
    # st[3][2] + st[3][5] * w - c * w - z,
]
results = solve(eqs, syms, dict=True)
print(results)
result = results[0]
print(result[x]+result[y]+result[z])
# exit()

# (va-V)*t + (V-vb)*u = pb - pa
# (va-V)*t + (V-vc)*u = pc - pa
# va*t - vc*u + du*V = pc-pa
#

# (va*t - vb*u + pa-pb)/(t-u)= V
# (va*t - vc*w + pa-pc)/(t-w)= V
# t = (P-pa)/(va-V)
# (vb-V)*u +pb-pa = (va-V)*t


def lines_intersect(a,b):
    #at what time do the x coords intersect
    # t = pb-pa/(va- vb)
    dxv = a[3]-b[3]
    if dxv==0: return None
    t = (b[0]-a[0])/dxv
    if t*a[4] + a[1] == t*b[4]+b[1] and t*a[5]+a[2]==t*b[5]+b[2]:
        return t
    return None

# sort lines by slope in each dimension and then ...?

from pprint import pprint

coord_limits = []
for i in range(3):
    # pmin,pmax, vmin,vmax
    rg = [((-1e20,+1e20),(-1e7,+1e7))]
    for particle in st:
        p,v = particle[i::3]
        # split range into low and high based on starting position
        # all P(in range)<p must have V>v
        nrs = []
        for pr,vr in rg:
            if pr[1]<p: # all positions in range < p : set min_V to at least v
                lo = (pr, (max(v,vr[0]),vr[1]))
                if lo[1][0]<=lo[1][1]: # non-empty velocity range
                    nrs.append(lo)
            elif pr[0]>p:
                hi = (pr, (vr[0],min(v,vr[1])))
                if hi[1][0]<=hi[1][1]: # non-empty velocity range
                    nrs.append(hi)
            else:
                # split the range
                #positions < p: velocity at least v
                lo = ((pr[0],p), (max(v,vr[0]),vr[1]))
                hi = ((p,pr[1]), (vr[0], min(v, vr[1])))
                if lo[1][0]<=lo[1][1]: # non-empty velocity range
                    nrs.append(lo)
                if hi[1][0]<=hi[1][1]: # non-empty velocity range
                    nrs.append(hi)
        # if P<p: V>v
        rg = nrs
    # rg = sorted(rg)
    # rg = rg[1:-1]
    v_rg = sorted(sum([r[1] for r in rg],()))
    _,vmin,*_,vmax,_ = v_rg
    pprint(rg)
    print(vmin,vmax)
    coord_limits.append(rg)

# seems this approach (reducing the velocity search space to 17*20*17) might have worked
# since the result does start on boundaries in both y and z
# and is within a range for x.
# However it starts outside ranges for the test input

# position+velocity can be uniquely determined from the time it hits A and B


