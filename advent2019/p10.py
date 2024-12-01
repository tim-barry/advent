
import cmath

with open('input10.txt', 'r') as f:
    r = f.read().strip()

l = r.split()

# pos: is ast
a2 = {x+y*1j:c in 'X#' for y,row in enumerate(l) for x,c in enumerate(row)}

asts = {a for a,is_ast in a2.items() if is_ast}
# print(f'{len(asts)} asteroids total')

point_angles = lambda p:sorted(cmath.phase(c-p) for c in asts if c-p)
def distinct(l, d=1e-9):
    # would use a set() if not for floating point differences...
    n = [l[0]]
    for x in l:
        if n and not abs(x-n[-1])<d:
            n.append(x)
    return n
def distinct2(l):
    # inspired by /u/jeroenheijmans
    # https://old.reddit.com/r/adventofcode/comments/e8m1z3/2019_day_10_solutions/fadaq9z/
    return {int(n*1e9) for n in l}
can_see_points = lambda p:len(distinct2(point_angles(p)))
best_pt = max(asts, key=can_see_points)

# print(best_pt)
print('part 1:', can_see_points(best_pt))

pt = best_pt
ast_angle_dist = sorted([(k, int(cmath.phase((k-pt)/1j)*1e9), abs(k-pt)) for k in asts if k-pt],
                        key=lambda t: t[1:])
i = 0
last_angle = -1e99
nremoved = 0
while nremoved<200:
    if not ast_angle_dist:
        raise RuntimeError("fewer than 200 asteroids")
    if ast_angle_dist[i][1] == last_angle:
        i += 1
    else:
        ast, last_angle, dist = ast_angle_dist.pop(i)
        nremoved+=1
    if i==len(ast_angle_dist):  # full rotation
        i=0
        last_angle = -1e99

print(int(ast.real*100+ast.imag))
