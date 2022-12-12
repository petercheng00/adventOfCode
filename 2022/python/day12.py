import sys
from typing import Dict, List, Tuple

def load_heightmap() -> Tuple[List[str], Tuple[int, int], Tuple[int, int]]:
    with open(sys.argv[1]) as f:
        heightmap = f.read().splitlines()

    start_pos = (-1, -1)
    end_pos = (-1, -1)
    for i in range(len(heightmap)):
        if (start_j:=heightmap[i].find("S")) != -1:
            start_pos = (i, start_j)
            heightmap[i] = heightmap[i].replace("S", "a")
        if (end_j:=heightmap[i].find("E")) != -1:
            end_pos = (i, end_j)
            heightmap[i] = heightmap[i].replace("E", "z")

    return heightmap, start_pos, end_pos


def part1():
    heightmap, start_pos, end_pos = load_heightmap()
    dist_from_start = {start_pos: 0}
    to_explore = [start_pos]

    while to_explore:
        pos = to_explore.pop(0)
        dist_to_pos = dist_from_start[pos]
        if pos == end_pos:
            print(dist_to_pos)
            return

        my_height = heightmap[pos[0]][pos[1]]

        for neighbor_step in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_pos = (pos[0] + neighbor_step[0], pos[1] + neighbor_step[1])
            if neighbor_pos[0] < 0 or neighbor_pos[0] >= len(heightmap) or neighbor_pos[1] < 0 or neighbor_pos[1] >= len(heightmap[0]):
                # Off the map!
                continue
            if neighbor_pos in dist_from_start:
                # Already visited before.
                continue

            neighbor_height = heightmap[neighbor_pos[0]][neighbor_pos[1]]

            if ord(neighbor_height) - ord(my_height) > 1:
                # Too high.
                continue

            dist_from_start[neighbor_pos] = dist_to_pos + 1
            to_explore.append(neighbor_pos)

    print("Finished without finding the end?")



def part2():
    heightmap, _, end_pos = load_heightmap()
    dist_from_end = {end_pos: 0}
    to_explore = [end_pos]

    while to_explore:
        pos = to_explore.pop(0)
        dist_to_pos = dist_from_end[pos]
        my_height = heightmap[pos[0]][pos[1]]

        if my_height == "a":
            print(dist_to_pos)
            return

        for neighbor_step in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_pos = (pos[0] + neighbor_step[0], pos[1] + neighbor_step[1])
            if neighbor_pos[0] < 0 or neighbor_pos[0] >= len(heightmap) or neighbor_pos[1] < 0 or neighbor_pos[1] >= len(heightmap[0]):
                # Off the map!
                continue
            if neighbor_pos in dist_from_end:
                # Already visited before.
                continue

            neighbor_height = heightmap[neighbor_pos[0]][neighbor_pos[1]]

            if ord(my_height) - ord(neighbor_height) > 1:
                # Too high.
                continue

            dist_from_end[neighbor_pos] = dist_to_pos + 1
            to_explore.append(neighbor_pos)

    print("Finished without finding the end?")


part1()
part2()
