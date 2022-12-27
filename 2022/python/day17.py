import sys
from typing import Tuple

import numpy as np
from tqdm import tqdm

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

shapes = [
    np.array([[1, 1, 1, 1]]),
    np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
    np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]]),
    np.array([[1], [1], [1], [1]]),
    np.array([[1, 1], [1, 1]]),
]

WORLD_HEIGHT = 1000000


class WorldState:
    def __init__(self, jet_pattern: str):
        self.jet_pattern = jet_pattern
        self.jet_index = 0
        self.shape_index = 0
        self.world = np.zeros((WORLD_HEIGHT, 7), dtype=int)
        self.rocks_fallen = 0
        self.tower_height = 0

    def test_rock_position(self, rock_shape: np.ndarray, x: int, y: int):
        rock_h, rock_w = rock_shape.shape
        world_h, world_w = self.world.shape
        # First a bounds check
        if x < 0 or x + rock_w - 1 >= world_w:
            return False
        if y + rock_h - 1 >= world_h:
            return False

        # We are inbounds, check for overlap against existing rocks
        world_crop = self.world[y : y + rock_h, x : x + rock_w]
        return not np.any(rock_shape & world_crop)

    def add_rock(self, rock_shape: np.ndarray, x: int, y: int):
        rock_h, rock_w = rock_shape.shape
        self.world[y : y + rock_h, x : x + rock_w] += rock_shape
        self.tower_height = max(self.world.shape[0] - y, self.tower_height)

    def drop_next_rock(self):
        shape = shapes[self.shape_index]
        self.shape_index = (self.shape_index + 1) % len(shapes)
        rock_height, rock_width = shape.shape
        # Find rock start position
        rock_x = 2
        rock_y = (self.world.shape[0] - self.tower_height) - 4 - (rock_height - 1)
        while True:
            # Try to shift the rock sideways
            jet_direction = self.jet_pattern[self.jet_index]
            self.jet_index = (self.jet_index + 1) % len(self.jet_pattern)
            x_shift = 1 if jet_direction == ">" else -1
            if self.test_rock_position(shape, rock_x + x_shift, rock_y):
                # We're able to move sideways, so move sideways.
                rock_x += x_shift
            # Try to move the rock down
            if self.test_rock_position(shape, rock_x, rock_y + 1):
                # We're able to move down, so move down.
                rock_y += 1
            else:
                # We weren't able to move down, so rock position is finalized.
                self.add_rock(shape, rock_x, rock_y)
                break

    def print_world(self):
        print(self.world[-10:])

    def get_state(self, num_rows: int) -> Tuple:
        data = [self.jet_index, self.shape_index]
        for row in range(
            self.world.shape[0] - self.tower_height,
            self.world.shape[0] - self.tower_height + num_rows,
        ):
            data += self.world[row].tolist()
        return tuple(data)


def part1():
    jet_pattern = lines[0]
    world = WorldState(jet_pattern)
    for i in range(2022):
        world.drop_next_rock()

    print(world.tower_height)


def part2():
    state_rows = 10
    state_to_rocks_and_height = {}
    jet_pattern = lines[0]
    world = WorldState(jet_pattern)
    for i in range(10000):
        world.drop_next_rock()
        if world.tower_height < state_rows:
            continue
        state = world.get_state(10)
        if state in state_to_rocks_and_height:
            first_rocks, first_height = state_to_rocks_and_height[state]
            second_rocks = i + 1
            second_height = world.tower_height
            break
        state_to_rocks_and_height[state] = [i + 1, world.tower_height]

    cycle_len = second_rocks - first_rocks
    cycle_height_change = second_height - first_height

    target_num_rocks = 1000000000000
    remaining_rocks = target_num_rocks - first_rocks
    remaining_rocks_modulo = remaining_rocks % cycle_len
    skipped_height = (remaining_rocks // cycle_len) * cycle_height_change

    world2 = WorldState(jet_pattern)
    for i in range(first_rocks + remaining_rocks_modulo):
        world2.drop_next_rock()

    print(world2.tower_height + skipped_height)


part1()
part2()
