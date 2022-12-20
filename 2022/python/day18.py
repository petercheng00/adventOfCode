import sys
from typing import List, Set, Tuple


def get_cubes() -> List[Tuple[int, int, int]]:
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()
    cubes = []
    for line in lines:
        x, y, z = [int(x) for x in line.split(",")]
        cubes.append((x, y, z))
    return cubes


def get_neighbors(xyz: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    x, y, z = xyz
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]


def part1():
    cubes = set(get_cubes())
    surface_area = 0
    for xyz in cubes:
        for neighbor in get_neighbors(xyz):
            if neighbor not in cubes:
                surface_area += 1
    print(surface_area)


def part2():
    # Strategy - create a bounding volume for the structure, + 1 margin in each dimension.
    # Pick one corner as known exterior.
    # Repeatedly diffuse known exterior status to neighboring empty spaces.
    # Stop when converged - then we know surface area borders known exterior only.
    cubes = set(get_cubes())
    min_x = min(xyz[0] for xyz in cubes) - 1
    max_x = max(xyz[0] for xyz in cubes) + 1
    min_y = min(xyz[1] for xyz in cubes) - 1
    max_y = max(xyz[1] for xyz in cubes) + 1
    min_z = min(xyz[2] for xyz in cubes) - 1
    max_z = max(xyz[2] for xyz in cubes) + 1

    known_exterior = set([(min_x, min_y, min_z)])
    to_explore = [(min_x, min_y, min_z)]

    while to_explore:
        xyz = to_explore.pop(0)
        for neighbor in get_neighbors(xyz):
            nx, ny, nz = neighbor
            if (
                nx < min_x
                or nx > max_x
                or ny < min_y
                or ny > max_y
                or nz < min_z
                or nz > max_z
            ):
                continue
            if neighbor in known_exterior:
                continue
            if neighbor in cubes:
                continue
            known_exterior.add(neighbor)
            to_explore.append(neighbor)

    surface_area = 0
    for xyz in cubes:
        for neighbor in get_neighbors(xyz):
            if neighbor in known_exterior:
                surface_area += 1
    print(surface_area)


part1()
part2()
