import heapq

with open('input') as f:
    world = [l.strip() for l in f.readlines()]

# world = ['#########',
         # '#b.A.@.a#',
         # '#########']

# world = ['########################',
         # '#f.D.E.e.C.b.A.@.a.B.c.#',
         # '######################.#',
         # '#d.....................#',
         # '########################']

# world = ['#################',
         # '#i.G..c...e..H.p#',
         # '########.########',
         # '#j.A..b...f..D.o#',
         # '########@########',
         # '#k.E..a...g..B.n#',
         # '########.########',
         # '#l.F..d...h..C.m#',
         # '#################']

# world = ['########################',
         # '#@..............ac.GI.b#',
         # '###d#e#f################',
         # '###A#B#C################',
         # '###g#h#i################',
         # '########################']

rows = len(world)
cols = len(world[0])

num_keys_per_row = [(sum(c.islower() for c in world[row])) for row in range(len(world))]
num_keys = sum(num_keys_per_row)
print(f'{num_keys=}')

key_positions = {}
for row in range(rows):
    for col in range(cols):
        if world[row][col] == '@':
            initial_at = (row, col)
        if world[row][col].islower():
            key_positions[world[row][col]] = (row, col)

# here's the plan:
# first, find out all the reachable keys, and min number of steps to reach each key
# then, iterate through each reachable key, and repeat branching from there

# this is all tooooo slow


# # returns a map of new_key: steps to reach
# def explore(start_pos, keys):
#     new_keys_min_steps = {}
#     visited = set()
#     visit_queue = [(start_pos, 0)]
#     while len(visit_queue) > 0:
#         pos, steps = visit_queue.pop(0)
#         if pos in visited:
#             continue
#         visited.add(pos)
#         row, col = pos
#         if row < 0 or row >= rows or col < 0 or col >= cols:
#             continue
#         char = world[row][col]
#         if char == '#':
#             continue
#         if char.isupper() and char.lower() not in keys: # at a door we can't unlock
#             continue
#         if char.islower() and char not in keys and char not in new_keys_min_steps:
#             new_keys_min_steps[char] = steps
#         visit_queue.append(((row-1, col), steps+1))
#         visit_queue.append(((row+1, col), steps+1))
#         visit_queue.append(((row, col-1), steps+1))
#         visit_queue.append(((row, col+1), steps+1))
#     return new_keys_min_steps

# configurations = [(0, [], initial_at)]

# while len(configurations) > 0:
#     steps_so_far, keys, start_pos = heapq.heappop(configurations)
#     print(steps_so_far)
#     if len(keys) == num_keys:
#         print(f'finished with {steps_so_far} steps')
#         break
#     key_steps = explore(start_pos, keys)
#     for key, steps in key_steps.items():
#         new_keys = keys.copy()
#         new_keys.append(key)
#         new_steps = steps_so_far + steps
#         new_config = (new_steps, new_keys, key_positions[key])
#         heapq.heappush(configurations, new_config)

# new plan. just do a single bfs, where each position is ((row, col), frozenset(keys in possession]))
# each position also stores number of steps so far for convenience
visit_queue = [(initial_at, frozenset([]), 0)]
visited = set()
while len(visit_queue) > 0:
    pos, keys, steps = visit_queue.pop(0)
    if (pos, keys) in visited:
        continue
    visited.add((pos, keys))
    row, col = pos
    if row < 0 or row >= rows or col < 0 or col >= cols:
        continue
    char = world[row][col]
    if char == '#':
        continue
    if char.isupper() and char.lower() not in keys: # at a door we can't unlock
        continue
    if char.islower() and char not in keys:
        new_keys = frozenset(list(keys) + [char])
        if len(new_keys) == num_keys:
            print(f'{steps=}')
            break
    else:
        new_keys = keys
    visit_queue.append(((row-1, col), new_keys, steps+1))
    visit_queue.append(((row+1, col), new_keys, steps+1))
    visit_queue.append(((row, col-1), new_keys, steps+1))
    visit_queue.append(((row, col+1), new_keys, steps+1))
