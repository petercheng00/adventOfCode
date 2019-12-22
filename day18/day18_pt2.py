with open('input_pt2') as f:
    world = [l.strip() for l in f.readlines()]

# world = ['#######',
         # '#a.#Cd#',
         # '##@#@##',
         # '#######',
         # '##@#@##',
         # '#cB#Ab#',
         # '#######']

# world = ['#############',
         # '#g#f.D#..h#l#',
         # '#F###e#E###.#',
         # '#dCba@#@BcIJ#',
         # '#############',
         # '#nK.L@#@G...#',
         # '#M###N#H###.#',
         # '#o#m..#i#jk.#',
         # '#############']


rows = len(world)
cols = len(world[0])

num_keys_per_row = [(sum(c.islower() for c in world[row])) for row in range(len(world))]
num_keys = sum(num_keys_per_row)
print(f'{num_keys=}')

initial_positions = []
for row in range(rows):
    for col in range(cols):
        if world[row][col] == '@':
            initial_positions.append((row, col))

# first lets just try the naive thing of part 1, but 4 positions
# this was wayyy too slow. idea from reddit is to only have one "active" robot at a time, so let's do that
visit_queue = [(tuple(initial_positions), frozenset([]), 0, 0)]
visited = set()
printed = set()
while len(visit_queue) > 0:
    # active is the robot that moved last
    poses, keys, active, steps = visit_queue.pop(0)
    if steps % 100 == 0 and steps not in printed:
        print(steps)
        printed.add(steps)
    if (poses, keys) in visited:
        continue
    visited.add((poses, keys))

    new_keys = list(keys)
    row, col = poses[active]
    if row < 0 or row >= rows or col < 0 or col >= cols:
        continue
    char = world[row][col]
    if char == '#':
        continue
    if char.isupper() and char.lower() not in keys: # at a door we can't unlock
        continue
    if char.islower() and char not in keys:
        new_keys.append(char)

    if len(new_keys) == num_keys:
        print(f'{steps=}')
        break

    picked_up_key = len(new_keys) > len(keys)

    # if we picked up a key, any robot can move. otherwise keep moving same robot
    for i, pos in enumerate(poses):
        if i == active or picked_up_key:
            row, col = pos
            poses_list = list(poses)
            poses_list[i] = (row-1, col)
            visit_queue.append((tuple(poses_list), frozenset(new_keys), i, steps+1))
            poses_list[i] = (row+1, col)
            visit_queue.append((tuple(poses_list), frozenset(new_keys), i, steps+1))
            poses_list[i] = (row, col-1)
            visit_queue.append((tuple(poses_list), frozenset(new_keys), i, steps+1))
            poses_list[i] = (row, col+1)
            visit_queue.append((tuple(poses_list), frozenset(new_keys), i, steps+1))
