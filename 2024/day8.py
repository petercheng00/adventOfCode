from collections import defaultdict
import sys

import numpy as np


with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

frequency_locations = defaultdict(list)
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c != ".":
            frequency_locations[c].append(np.array([x, y]))

height = len(lines)
width = len(lines[0])


def part1():
    antinode_positions = set()
    for locations in frequency_locations.values():
        for a in locations:
            for b in locations:
                if (a != b).any():
                    c = a + a - b
                    if c[0] >= 0 and c[0] < width and c[1] >= 0 and c[1] < height:
                        antinode_positions.add(tuple(c))
    print(len(antinode_positions))


def part2():
    antinode_positions = set()
    for locations in frequency_locations.values():
        for a in locations:
            for b in locations:
                if (a != b).any():
                    step = 0
                    while True:
                        c = a + step * (a - b)
                        if c[0] >= 0 and c[0] < width and c[1] >= 0 and c[1] < height:
                            antinode_positions.add(tuple(c))
                            step += 1
                        else:
                            break
    print(len(antinode_positions))


part1()
part2()
