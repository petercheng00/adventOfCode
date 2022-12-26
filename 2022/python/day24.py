from dataclasses import dataclass
import sys
from typing import List, Optional, Tuple

import numpy as np


@dataclass
class Blizzard:
    x: int
    y: int
    direction: str


def load_world() -> Tuple[np.ndarray, List[Blizzard]]:
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    blizzards = []
    world_map = []
    for row, l in enumerate(lines):
        world_map_row = []
        for col, c in enumerate(l):
            if c == "#":
                world_map_row.append(-1)
            elif c == ".":
                world_map_row.append(0)
            elif c == "^":
                world_map_row.append(1)
                blizzards.append(Blizzard(col, row, "N"))
            elif c == "v":
                world_map_row.append(1)
                blizzards.append(Blizzard(col, row, "S"))
            elif c == ">":
                world_map_row.append(1)
                blizzards.append(Blizzard(col, row, "E"))
            elif c == "<":
                world_map_row.append(1)
                blizzards.append(Blizzard(col, row, "W"))
        world_map.append(world_map_row)

    return np.array(world_map), blizzards


def time_step(world_map: np.ndarray, blizzards: List[Blizzard]):
    h, w = world_map.shape
    for b in blizzards:
        # Decrement world map.
        world_map[b.y, b.x] -= 1

        # Find new spot.
        if b.direction == "N":
            b.y -= 1
        elif b.direction == "S":
            b.y += 1
        elif b.direction == "E":
            b.x += 1
        elif b.direction == "W":
            b.x -= 1

        if world_map[b.y, b.x] == -1:
            # Need to wrap around.
            if b.direction == "N":
                b.y = h - 2
            elif b.direction == "S":
                b.y = 1
            elif b.direction == "E":
                b.x = 1
            elif b.direction == "W":
                b.x = w - 2

        # Increment world map.
        world_map[b.y, b.x] += 1


def get_travel_time(
    world_map: np.ndarray,
    blizzards: List[Blizzard],
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
) -> int:
    cycle_len = np.lcm(world_map.shape[0] - 2, world_map.shape[1] - 2)
    # (x, y, time % cycle_len) uniquely identifies a configuration, so skip if we've seen before.
    seen_before = set()

    current_xys = [(start_x, start_y)]
    time_so_far = 0
    while True:

        # Update the blizzards.
        time_step(world_map, blizzards)

        next_xys = []
        for current_x, current_y in current_xys:
            if (current_x, current_y, time_so_far % cycle_len) in seen_before:
                continue
            else:
                seen_before.add((current_x, current_y, time_so_far % cycle_len))
            for xy_offset in [[0, 0], [0, -1], [0, 1], [-1, 0], [1, 0]]:
                next_x = current_x + xy_offset[0]
                next_y = current_y + xy_offset[1]
                if (
                    next_x < 0
                    or next_x > world_map.shape[1] - 1
                    or next_y < 0
                    or next_y > world_map.shape[0] - 1
                ):
                    continue
                if world_map[next_y, next_x] != 0:
                    continue
                if next_x == end_x and next_y == end_y:
                    return time_so_far + 1
                next_xys.append((next_x, next_y))

        current_xys = next_xys
        time_so_far += 1


def part1():
    world_map, blizzards = load_world()

    start_y = 0
    start_x = 0
    while world_map[start_y, start_x] != 0:
        start_x += 1
    end_y = world_map.shape[0] - 1
    end_x = 0
    while world_map[end_y, end_x] != 0:
        end_x += 1

    print(get_travel_time(world_map, blizzards, start_x, start_y, end_x, end_y))


def part2():
    world_map, blizzards = load_world()

    start_y = 0
    start_x = 0
    while world_map[start_y, start_x] != 0:
        start_x += 1
    end_y = world_map.shape[0] - 1
    end_x = 0
    while world_map[end_y, end_x] != 0:
        end_x += 1

    t1 = get_travel_time(world_map, blizzards, start_x, start_y, end_x, end_y)
    t2 = get_travel_time(world_map, blizzards, end_x, end_y, start_x, start_y)
    t3 = get_travel_time(world_map, blizzards, start_x, start_y, end_x, end_y)

    print(t1 + t2 + t3)


part1()
part2()
