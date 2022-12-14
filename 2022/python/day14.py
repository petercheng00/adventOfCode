import sys

import numpy as np

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

AIR = 0
ROCK = 1
SAND = 2

SAND_START_X = 500


def load_world(part2=False):

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    # Load input points.
    structures = []
    for line in lines:
        structure = []
        pts = line.split("->")
        for pt in pts:
            structure.append(np.array([int(x) for x in pt.split(",")]))
        structures.append(structure)

    # Generate world based on point extents.
    min_xy = np.min([np.min(x, axis=0) for x in structures], axis=0)
    max_xy = np.max([np.max(x, axis=0) for x in structures], axis=0)

    min_x = min_xy[0]
    max_x = max_xy[0]
    min_y = 0  # Sand always starts at y=0.
    max_y = max_xy[1]

    if part2:
        max_y += 2
        # Only need to go wide enough for a 45 degree angle.
        # This is double wide enough for some extra margin.
        min_x -= max_y
        max_x += max_y
        structures.append([[min_x, max_y], [max_x, max_y]])

    # Initialize world filled with air.
    world = np.full((max_y + 1, max_x - min_x + 1), AIR)

    # Draw the rock structures.
    for structure in structures:
        for i in range(1, len(structure)):
            x1, y1 = structure[i - 1]
            x2, y2 = structure[i]
            world[
                min(y1, y2) : max(y1, y2) + 1,
                min(x1 - min_x, x2 - min_x) : max(x1 - min_x, x2 - min_x) + 1,
            ] = ROCK

    return world, min_x


def add_sand(world, start_x):
    sand_x = start_x
    sand_y = 0
    while True:
        if sand_x < 0 or sand_x >= world.shape[1] or sand_y >= world.shape[0]:
            # Sand fell off the world.
            return False
        if world[sand_y + 1, sand_x] == AIR:
            # If empty below, fall down.
            sand_y += 1
        elif world[sand_y + 1, sand_x - 1] == AIR:
            # Elif space down left, go there.
            sand_x -= 1
            sand_y += 1
        elif world[sand_y + 1, sand_x + 1] == AIR:
            # Elif space down right, go there.
            sand_x += 1
            sand_y += 1
        else:
            world[sand_y, sand_x] = SAND
            return True


def part1():
    world, min_x = load_world()

    sand_x = SAND_START_X - min_x

    num_sand = 0
    while add_sand(world, sand_x):
        num_sand += 1

    print(num_sand)


def part2():
    world, min_x = load_world(True)

    sand_x = SAND_START_X - min_x

    num_sand = 0
    while add_sand(world, sand_x):
        num_sand += 1
        if world[0, sand_x] == SAND:
            # We're full!
            break

    print(num_sand)


part1()
part2()
