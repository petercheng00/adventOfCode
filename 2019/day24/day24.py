with open('input') as f:
    world = [l.strip() for l in f.readlines()]

def getBiodiversity(w):
    bd = 0
    index = 0
    for row in w:
        for char in row:
            if char == '#':
                bd += pow(2, index)
            index += 1
    return bd

def update(w):
    new_w = []
    for y, row in enumerate(w):
        new_w.append([])
        for x, char in enumerate(row):
            num_bugs_around = 0
            if (y > 0 and w[y-1][x] == '#'):
                num_bugs_around += 1
            if (y < len(w)-1 and w[y+1][x] == '#'):
                num_bugs_around += 1
            if (x > 0 and w[y][x-1] == '#'):
                num_bugs_around += 1
            if (x < len(row)-1 and w[y][x+1] == '#'):
                num_bugs_around += 1
            if char == '#':
                if num_bugs_around == 1:
                    new_w[-1].append('#')
                else:
                    new_w[-1].append('.')
            elif char == '.':
                if num_bugs_around == 1 or num_bugs_around == 2:
                    new_w[-1].append('#')
                else:
                    new_w[-1].append('.')
            else:
                print('unexpected char')
    return [''.join(r) for r in new_w]

seen = set()
seen.add(getBiodiversity(world))
while True:
    world = update(world)
    bd = getBiodiversity(world)
    if bd in seen:
        print(bd)
        break
    seen.add(bd)
