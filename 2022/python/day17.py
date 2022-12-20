import sys

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

WORLD_HEIGHT = 5000
SHIFT_THRESHOLD = 10


class WorldState:
    def __init__(self, jet_pattern: str):
        self.jet_pattern = jet_pattern
        self.jet_index = 0
        self.shape_index = 0
        # World will always be a fixed height, and then when we're close to filling it up, we'll just shift everything.
        self.world = np.zeros((WORLD_HEIGHT, 7), dtype=int)
        # Amount of spaces below the current world (stuff we've shifted out of frame).
        self.height_below = 0
        self.rocks_fallen = 0

    def first_nonzero_row(self) -> int:
        if not np.any(self.world):
            return self.world.shape[0]
        return np.nonzero(self.world)[0][0]

    def total_height(self):
        return self.height_below + self.world.shape[0] - self.first_nonzero_row()

    def test_rock_position(self, rock_shape: np.ndarray, x: int, y: int):
        rock_h, rock_w = rock_shape.shape
        world_h, world_w = self.world.shape
        # First a bounds check
        if x < 0 or x + rock_w - 1 >= world_w:
            return False
        if y + rock_h - 1 >= world_h:
            if self.height_below > 0:
                raise Exception(
                    "Fell through floor when there is height below! Increase world height."
                )
            return False

        # We are inbounds, check for overlap against existing rocks
        world_crop = self.world[y : y + rock_h, x : x + rock_w]
        return not np.any(rock_shape & world_crop)

    def add_rock(self, rock_shape: np.ndarray, x: int, y: int):
        rock_h, rock_w = rock_shape.shape
        self.world[y : y + rock_h, x : x + rock_w] += rock_shape

    def drop_next_rock(self):
        shape = shapes[self.shape_index]
        self.shape_index = (self.shape_index + 1) % len(shapes)
        rock_height, rock_width = shape.shape
        # Find rock start position
        rock_x = 2
        rock_y = self.first_nonzero_row() - 4 - (rock_height - 1)
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

    def shift_world_if_needed(self):
        if self.first_nonzero_row() < SHIFT_THRESHOLD:
            new_world = np.zeros((WORLD_HEIGHT, 7), dtype=int)
            new_world[WORLD_HEIGHT // 2 :] = self.world[: WORLD_HEIGHT // 2]
            self.world = new_world
            self.height_below += WORLD_HEIGHT // 2

    def print_world(self):
        print(self.world[-10:])


def part1():
    jet_pattern = lines[0]
    world = WorldState(jet_pattern)
    for i in range(2022):
        world.drop_next_rock()
        world.shift_world_if_needed()

    print(world.total_height())


def part2():
    pass


part1()
part2()
