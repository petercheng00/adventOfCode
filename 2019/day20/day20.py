with open('input') as f:
    world = [l.strip('\n') for l in f.readlines()]

rows = len(world)
cols = len(world[0])
# dictionary where each key's coordinate is a portal to its value coordinates
warp = {}
# dictionary from portal name to coordinate. used to build warp
portal_first_coord = {}
# outer portal coords are in this set
outer_coords = set()
for row, row_str in enumerate(world):
    for col, char in enumerate(row_str):
        if not char.isupper():
            continue
        # find the coordinate by finding another capital letter followed by a . in a direction
        name = None
        coord = None
        if row >= 2 and world[row-1][col].isupper() and world[row-2][col] == '.':
            name = world[row-1][col] + char
            coord = (row-2, col)
        elif row < rows-2 and world[row+1][col].isupper() and world[row+2][col] == '.':
            name = char + world[row+1][col]
            coord = (row+2, col)
        elif col >= 2 and world[row][col-1].isupper() and world[row][col-2] == '.':
            name = world[row][col-1] + char
            coord = (row, col-2)
        elif col < cols-2 and world[row][col+1].isupper() and world[row][col+2] == '.':
            name = char + world[row][col+1]
            coord = (row, col+2)
        if name is not None:
            if name == 'AA':
                start = coord
            elif name == 'ZZ':
                end = coord
            else:
                if row == 0 or col == 0 or row == rows-1 or col == cols-1:
                    outer_coords.add(coord)
                if name not in portal_first_coord:
                    portal_first_coord[name] = coord
                else:
                    warp[coord] = portal_first_coord[name]
                    warp[portal_first_coord[name]] = coord
visit_queue = [(start, 0)]
visited = set()
while len(visit_queue) > 0:
    pos, steps = visit_queue.pop(0)
    if pos in visited:
        continue
    visited.add(pos)
    if pos == end:
        print(f'done in {steps} steps')
        break
    # options are move to any adjacent dot or take a teleport
    row, col = pos
    if row > 0 and world[row-1][col] == '.':
        visit_queue.append(((row-1, col), steps+1))
    if row < rows-1 and world[row+1][col] == '.':
        visit_queue.append(((row+1, col), steps+1))
    if col > 0 and world[row][col-1] == '.':
        visit_queue.append(((row, col-1), steps+1))
    if col < cols-1 and world[row][col+1] == '.':
        visit_queue.append(((row, col+1), steps+1))
    if pos in warp:
        visit_queue.append((warp[pos], steps+1))

print('now for the recursive version')
visit_queue = [(start, 0, 0)]
visited = set()
while len(visit_queue) > 0:
    pos, level, steps = visit_queue.pop(0)
    if (pos, level) in visited:
        continue
    visited.add((pos, level))
    if pos == end and level == 0:
        print(f'done in {steps} steps')
        break
    # options are move to any adjacent dot or take a teleport
    row, col = pos
    if row > 0 and world[row-1][col] == '.':
        visit_queue.append(((row-1, col), level, steps+1))
    if row < rows-1 and world[row+1][col] == '.':
        visit_queue.append(((row+1, col), level, steps+1))
    if col > 0 and world[row][col-1] == '.':
        visit_queue.append(((row, col-1), level, steps+1))
    if col < cols-1 and world[row][col+1] == '.':
        visit_queue.append(((row, col+1), level, steps+1))
    if pos in warp:
        if pos in outer_coords:
            if level > 0:
                visit_queue.append((warp[pos], level-1, steps+1))
        else:
            visit_queue.append((warp[pos], level+1, steps+1))
