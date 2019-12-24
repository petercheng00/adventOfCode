import copy

with open('input') as f:
    middle_layer = [l.strip() for l in f.readlines()]

    for i in range(len(middle_layer)):
        middle_layer[i] = [c for c in middle_layer[i]]

rows = len(middle_layer)
cols = len(middle_layer[0])
# below we'll also just hardcode that layers are 5x5 so middle is index 2

empty_layer = []
for row in range(rows):
    empty_layer.append(['.'] * cols)

# we are running for 200 minutes, so let's just hardcode that the world is 401 layers

world = []
for layer in range(401):
    world.append(copy.deepcopy(empty_layer))

world[201] = middle_layer

def update(w):
    new_w = []
    for layer in range(len(world)):
        new_w.append([])
        for y in range(rows):
            new_w[-1].append([])
            for x in range(cols):
                # this spot doesn't exist
                if x == 2 and y == 2:
                    new_w[-1][-1].append('.')
                    continue
                num_bugs_around = 0


                # check up direction
                if y == 0:
                    # we are on top border, so go one layer up
                    if layer > 0 and w[layer-1][1][2] == '#':
                        num_bugs_around += 1
                elif y == 3 and x == 2:
                    if layer < len(world)-1:
                        # we are below the middle, so go one layer down
                        for char in w[layer+1][-1]:
                            if char == '#':
                                num_bugs_around += 1
                else:
                    # just normal above
                    if w[layer][y-1][x] == '#':
                        num_bugs_around += 1



                # now down direction
                if y == rows-1:
                    # we are on bottom border
                    if layer > 0 and w[layer-1][3][2] == '#':
                        num_bugs_around += 1
                elif y == 1 and x == 2:
                    if layer < len(world)-1:
                        # above the middle, so go one layer down
                        for char in w[layer+1][0]:
                            if char == '#':
                                num_bugs_around += 1
                else:
                    # normal down
                    if w[layer][y+1][x] == '#':
                        num_bugs_around += 1



                # left direction
                if x == 0:
                    # left border, so go one layer up
                    if layer > 0 and w[layer-1][2][1] == '#':
                        num_bugs_around += 1
                elif y == 2 and x == 3:
                    if layer < len(world)-1:
                        # right of middle
                        for r in range(rows):
                            if w[layer+1][r][-1] == '#':
                                num_bugs_around += 1
                else:
                    # normal left
                    if w[layer][y][x-1] == '#':
                        num_bugs_around += 1


                # right direction
                if x == cols-1:
                    if layer > 0 and w[layer-1][2][3] == '#':
                        num_bugs_around += 1
                elif y == 2 and x == 1:
                    if layer < len(world)-1:
                        for r in range(rows):
                            if w[layer+1][r][0] == '#':
                                num_bugs_around += 1
                else:
                    if w[layer][y][x+1] == '#':
                        num_bugs_around += 1

                char = w[layer][y][x]
                if char == '#':
                    if num_bugs_around == 1:
                        new_w[-1][-1].append('#')
                    else:
                        new_w[-1][-1].append('.')
                elif char == '.':
                    if num_bugs_around == 1 or num_bugs_around == 2:
                        new_w[-1][-1].append('#')
                    else:
                        new_w[-1][-1].append('.')
                else:
                    print('unexpected char')
    return new_w

for i in range(200):
    world = update(world)
total = 0
for layer in world:
    for row in layer:
        for char in row:
            if char == '#':
                total += 1
print(total)
