import re
import sys

import numpy as np


def load_data():
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    sensor_xys = []
    beacon_xys = []
    for line in lines:
        m = re.match(
            r"Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)", line
        )
        sensor_xys.append((int(m.group(1)), int(m.group(2))))
        beacon_xys.append((int(m.group(3)), int(m.group(4))))

    sensor_ranges = []
    for sensor_xy, beacon_xy in zip(sensor_xys, beacon_xys):
        sensor_ranges.append(
            abs(sensor_xy[0] - beacon_xy[0]) + abs(sensor_xy[1] - beacon_xy[1])
        )

    min_xy = np.min(np.array(sensor_xys) - np.array(sensor_ranges)[:, None], axis=0)
    max_xy = np.max(np.array(sensor_xys) + np.array(sensor_ranges)[:, None], axis=0)

    return sensor_xys, beacon_xys, sensor_ranges, min_xy, max_xy


def part1():
    # TARGET_Y = 10
    TARGET_Y = 2000000

    sensor_xys, beacon_xys, sensor_ranges, min_xy, max_xy = load_data()

    num_non_beacon = 0
    for x in range(min_xy[0], max_xy[0] + 1):
        xy = (x, TARGET_Y)
        if xy in beacon_xys:
            continue
        sensor_covers = False
        for sensor_xy, sensor_range in zip(sensor_xys, sensor_ranges):
            x_range = sensor_range - abs(sensor_xy[1] - TARGET_Y)
            if x_range < 0:
                continue
            if x >= (sensor_xy[0] - x_range) and x <= (sensor_xy[0] + x_range):
                sensor_covers = True
                break

        if sensor_covers:
            num_non_beacon += 1

    print(num_non_beacon)


def part2():
    sensor_xys, beacon_xys, sensor_ranges, min_xy, max_xy = load_data()

    MIN_X = 0
    MIN_Y = 0
    # MAX_X = 20
    # MAX_Y = 20
    MAX_X = 4000000
    MAX_Y = 4000000

    x = MIN_X
    y = MIN_X

    while True:
        sensor_covers = False
        for sensor_xy, sensor_range in zip(sensor_xys, sensor_ranges):
            x_range = sensor_range - abs(sensor_xy[1] - y)
            if x_range < 0:
                continue
            min_x_covered = sensor_xy[0] - x_range
            max_x_covered = sensor_xy[0] + x_range
            if x >= min_x_covered and x <= max_x_covered:
                sensor_covers = True
                x = max_x_covered + 1
                break

        if not sensor_covers:
            print("Found it!")
            print(x * 4000000 + y)
            return

        if x > MAX_X:
            print(y)
            x = 0
            y += 1
            if y > MAX_Y:
                print("Searched whole space")
                return


part1()
part2()
