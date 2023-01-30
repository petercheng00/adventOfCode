from dataclasses import dataclass
import sys
from typing import List

import numpy as np
from tqdm import tqdm


@dataclass
class Cuboid:
    is_on: bool
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int


def load_cuboids() -> List[Cuboid]:
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()
    cuboids = []
    for line in lines:
        action, cuboid = line.split()
        is_on = action == "on"
        x_part, y_part, z_part = cuboid.split(",")
        x_min, x_max = [int(i) for i in x_part.split("=")[1].split("..")]
        y_min, y_max = [int(i) for i in y_part.split("=")[1].split("..")]
        z_min, z_max = [int(i) for i in z_part.split("=")[1].split("..")]
        cuboids.append(Cuboid(is_on, x_min, x_max, y_min, y_max, z_min, z_max))
    return cuboids


def part1():
    cuboids = load_cuboids()
    volume = np.full((101, 101, 101), False)
    for c in cuboids:
        volume[
            c.x_min + 50 : c.x_max + 51,
            c.y_min + 50 : c.y_max + 51,
            c.z_min + 50 : c.z_max + 51,
        ] = (
            True if c.is_on else False
        )

    print(np.count_nonzero(volume))


def overlaps(c1: Cuboid, c2: Cuboid) -> bool:
    x_min = max(c1.x_min, c2.x_min)
    x_max = min(c1.x_max, c2.x_max)
    if x_min > x_max:
        return False
    y_min = max(c1.y_min, c2.y_min)
    y_max = min(c1.y_max, c2.y_max)
    if y_min > y_max:
        return False
    z_min = max(c1.z_min, c2.z_min)
    z_max = min(c1.z_max, c2.z_max)
    if z_min > z_max:
        return False

    return True


def remove_cube_from_volume(volume: Cuboid, cube: Cuboid) -> List[Cuboid]:
    # This function chops up volume into subvolumes, and returns only the subvolumes that don't overlap with cube.
    if not overlaps(volume, cube):
        return [volume]

    x_ranges = []
    # The part of the volume that overlaps with cube.
    x_ranges.append((max(volume.x_min, cube.x_min), min(volume.x_max, cube.x_max)))
    if volume.x_min < cube.x_min:
        # The part of the volume that has x < cube.
        x_ranges.append((volume.x_min, cube.x_min - 1))
    if volume.x_max > cube.x_max:
        # The part of the volume that has x > cube.
        x_ranges.append((cube.x_max + 1, volume.x_max))

    # Same for y
    y_ranges = []
    # The part of the volume that overlaps with cube.
    y_ranges.append((max(volume.y_min, cube.y_min), min(volume.y_max, cube.y_max)))
    if volume.y_min < cube.y_min:
        # The part of the volume that has y < cube.
        y_ranges.append((volume.y_min, cube.y_min - 1))
    if volume.y_max > cube.y_max:
        # The part of the volume that has y > cube.
        y_ranges.append((cube.y_max + 1, volume.y_max))

    # Same for z
    z_ranges = []
    # The part of the volume that overlaps with cube.
    z_ranges.append((max(volume.z_min, cube.z_min), min(volume.z_max, cube.z_max)))
    if volume.z_min < cube.z_min:
        # The part of the volume that has z < cube.
        z_ranges.append((volume.z_min, cube.z_min - 1))
    if volume.z_max > cube.z_max:
        # The part of the volume that has z > cube.
        z_ranges.append((cube.z_max + 1, volume.z_max))

    sub_volumes = []
    for x_i, (x_min, x_max) in enumerate(x_ranges):
        for y_i, (y_min, y_max) in enumerate(y_ranges):
            for z_i, (z_min, z_max) in enumerate(z_ranges):
                if x_i == 0 and y_i == 0 and z_i == 0:
                    # This part overlaps with the cube.
                    continue
                sub_volumes.append(
                    Cuboid(True, x_min, x_max, y_min, y_max, z_min, z_max)
                )
    return sub_volumes


def part2():
    cuboids = load_cuboids()

    # Plan: Track a set of on_volumes, which are cube regions that are on.
    # For each new cube, check for overlap with each on_volume. If overlap is present, chop the
    # on_volume into pieces, discarding pieces that overlap with the new cube. Then add the new
    # cube as an on_volume if it's an on cube.

    on_volumes = []
    for cuboid in tqdm(cuboids):
        # Process this cuboid, updating on_volumes.
        next_on_volumes = []
        for current_on_volume in on_volumes:
            next_on_volumes += remove_cube_from_volume(current_on_volume, cuboid)
        if cuboid.is_on:
            next_on_volumes.append(cuboid)

        on_volumes = next_on_volumes

    total_on = 0
    for v in on_volumes:
        total_on += (
            (v.x_max - v.x_min + 1) * (v.y_max - v.y_min + 1) * (v.z_max - v.z_min + 1)
        )
    print(total_on)


part1()
part2()
