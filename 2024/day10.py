import sys

import numpy as np

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

map = np.array([[int(c) for c in line] for line in lines])
trailheads = np.argwhere(map == 0)
peaks = np.argwhere(map == 9)


def neighbors(rowcol):
    return [
        n
        for n in [
            (rowcol[0] + 1, rowcol[1]),
            (rowcol[0] - 1, rowcol[1]),
            (rowcol[0], rowcol[1] + 1),
            (rowcol[0], rowcol[1] - 1),
        ]
        if n[0] >= 0 and n[0] < len(map) and n[1] >= 0 and n[1] < len(map[0])
    ]


def reachable_peaks(trailhead):
    to_visit = [trailhead]
    visited = set()
    peaks = set()
    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)
        value = map[current[0], current[1]]
        if value == 9:
            peaks.add(current)
            continue
        for neighbor in neighbors(current):
            if map[neighbor[0], neighbor[1]] == value + 1:
                to_visit.append(neighbor)

    return peaks


def num_trails(current, cache):
    if (x := cache.get(current)) is not None:
        return x
    value = map[current[0], current[1]]
    if value == 9:
        return 1
    result = 0
    for neighbor in neighbors(current):
        if map[neighbor[0], neighbor[1]] == value + 1:
            result += num_trails(neighbor, cache)
    cache[current] = result
    return result


def part1():
    print(sum(len(reachable_peaks(tuple(x))) for x in trailheads))


def part2():
    cache = {}
    print(sum(num_trails(tuple(x), cache) for x in trailheads))


part1()
part2()
