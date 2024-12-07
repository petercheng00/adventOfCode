import sys

import numpy as np

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

start_xy = None
start_dir = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "^":
            start_xy = np.array([x, y])
            start_dir = np.array([0, -1])
assert start_xy is not None


def rotate_cw(dir):
    return np.array([-dir[1], dir[0]])


def oob(xy):
    return xy[0] < 0 or xy[0] >= len(lines[0]) or xy[1] < 0 or xy[1] >= len(lines)


def step(xy, dir, extra_obstacle=(-1, -1)):
    next_xy = xy + dir
    if oob(next_xy):
        return None, None
    if lines[next_xy[1]][next_xy[0]] == "#" or tuple(next_xy) == extra_obstacle:
        return xy, rotate_cw(dir)
    return next_xy, dir


def part1():
    xy, dir = start_xy, start_dir
    visited = set()
    while xy is not None:
        visited.add(tuple(xy))
        xy, dir = step(xy, dir)

    print(len(visited))


def would_loop(xy, dir, extra_obstacle):
    seen_states = set()
    while xy is not None:
        state = tuple(np.concatenate([xy, dir]))
        if state in seen_states:
            return True
        seen_states.add(state)
        xy, dir = step(xy, dir, extra_obstacle)
    return False


def part2():
    xy = start_xy
    dir = start_dir
    visited = set()
    loop_creation_xys = set()
    while True:
        visited.add(tuple(xy))
        next_xy = xy + dir
        if oob(next_xy):
            break
        if lines[next_xy[1]][next_xy[0]] == "#":
            dir = rotate_cw(dir)
        else:
            # Check if adding an obstacle at next_xy would create a loop.
            # Cannot add an obstacle on a spot that we would have hit previously.
            if (
                tuple(next_xy) not in loop_creation_xys
                and tuple(next_xy) not in visited
            ):
                if would_loop(xy, dir, tuple(next_xy)):
                    loop_creation_xys.add(tuple(next_xy))
            xy = next_xy

    num_answers = len(loop_creation_xys)
    if tuple(start_xy) in loop_creation_xys:
        print("removing start position")
        num_answers -= 1
    print(num_answers)


part1()
part2()
