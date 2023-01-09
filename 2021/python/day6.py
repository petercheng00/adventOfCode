import sys

from collections import defaultdict
from typing import DefaultDict

RESET_TIMER_VALUE = 6
NEW_TIMER_VALUE = 8

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def update_timers(timers: DefaultDict[int, int]) -> DefaultDict[int, int]:
    new_timers = defaultdict(int)
    for k, v in timers.items():
        if k > 0:
            new_timers[k - 1] += v
        else:
            new_timers[RESET_TIMER_VALUE] += v
            new_timers[NEW_TIMER_VALUE] += v
    return new_timers


def part1():
    # Store a dictionary where key is timer values, value is number of fish with that timer value.
    timers = defaultdict(int)
    for x in [int(y) for y in lines[0].split(",")]:
        timers[x] += 1

    for _ in range(80):
        timers = update_timers(timers)

    print(sum(timers.values()))


def part2():
    # Store a dictionary where key is timer values, value is number of fish with that timer value.
    timers = defaultdict(int)
    for x in [int(y) for y in lines[0].split(",")]:
        timers[x] += 1

    for _ in range(256):
        timers = update_timers(timers)

    print(sum(timers.values()))


part1()
part2()
