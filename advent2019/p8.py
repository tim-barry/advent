
# 14/78 -- was printing wrong image, and not visibly
with open('input8.txt') as f:
    r = f.read().strip()

ol = map(int, r)
w,h = 25,6
wh = w*h
layers = [ol[i*wh:(i+1)*wh] for i in range(len(ol)//wh)]

lay = min(layers, key=lambda ly:ly.count(0))
print(lay.count(1)*lay.count(2))  # part 1
nl = [[x for x in p if x!=2][0] for p in zip(*layers)]
img = [nl[i*w:(i+1)*w] for i in range(h)]
for row in img:
    print(''.join(' #'[i] for i in row))  # part 2
