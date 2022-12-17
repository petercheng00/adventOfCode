import sys

import numpy as np

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

shapes = [
    np.array([[1, 1, 1, 1]]),
    np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
    np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]]),
    np.array([[1], [1], [1], [1]]),
    np.array([[1, 1], [1, 1]]),
]


class WorldState:
    def __init__(self, jet_pattern: str):
        self.jet_pattern = jet_pattern
        self.jet_index = 0
        self.shape_index = 0
        # World will always be 100 tall, and then when we're close to filling it up, we'll just shift everything.
        self.world = np.zeros((100, 7), dtype=int)
        # Amount of spaces below the current world (stuff we've shifted out of frame).
        self.height_below = 0
        self.rocks_fallen = 0

    def get_current_height(self):
        pass

    def drop_next_rock(self):
        # find rock start position
        # while true, shift rock sideways and down
        # at each step, check if collides with existing rocks.
        # exit when sitting on something
        # throw an error/warning if hits the bottom of the world, and height_below==0.
        # update state variables
        pass

    def shift_world_if_needed(self):
        # check if current_height is near the top of the world, if so shift everything down
        pass


def part1():
    jet_pattern = lines[0]
    pass


def part2():
    pass


part1()
part2()
