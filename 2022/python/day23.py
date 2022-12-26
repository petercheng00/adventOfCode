from collections import defaultdict
import sys
from typing import List, Tuple

import numpy as np

ALL_NEIGHBORS = [
    np.array(x)
    for x in [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
]

N_NEIGHBORS = [np.array(x) for x in [[-1, -1], [0, -1], [1, -1]]]
S_NEIGHBORS = [np.array(x) for x in [[-1, 1], [0, 1], [1, 1]]]
W_NEIGHBORS = [np.array(x) for x in [[-1, -1], [-1, 0], [-1, 1]]]
E_NEIGHBORS = [np.array(x) for x in [[1, -1], [1, 0], [1, 1]]]

DIR_NEIGHBORS = {"N": N_NEIGHBORS, "S": S_NEIGHBORS, "W": W_NEIGHBORS, "E": E_NEIGHBORS}

DIR_STEP = {
    "N": np.array([0, -1]),
    "S": np.array([0, 1]),
    "W": np.array([-1, 0]),
    "E": np.array([1, 0]),
}


def load_elf_positions() -> List[Tuple[int, int]]:
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()
    elf_xys = []

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                elf_xys.append((x, y))

    return elf_xys


def process_round(
    elf_xys: List[Tuple[int, int]], dir_order: List[str]
) -> Tuple[List[Tuple[int, int]], bool]:
    elf_xys_set = set(elf_xys)
    proposed_xys = []
    proposed_xy_counts = defaultdict(int)

    for elf_xy in elf_xys:
        elf_xy = np.array(elf_xy)

        # If there is no neighboring elf in 8-adjacency, do nothing
        have_any_neighbor = False
        for n in ALL_NEIGHBORS:
            nxy = elf_xy + n
            if (nxy[0], nxy[1]) in elf_xys_set:
                have_any_neighbor = True
                break
        if not have_any_neighbor:
            proposed_xy = elf_xy
        else:
            # Determine movement direction
            dir_to_move = ""
            for d in dir_order:
                have_neighbor_in_direction = False
                for n in DIR_NEIGHBORS[d]:
                    nxy = elf_xy + n
                    if (nxy[0], nxy[1]) in elf_xys_set:
                        have_neighbor_in_direction = True
                        break
                if not have_neighbor_in_direction:
                    dir_to_move = d
                    break

            if not dir_to_move:
                proposed_xy = elf_xy
            else:
                proposed_xy = elf_xy + DIR_STEP[dir_to_move]

        proposed_xys.append((proposed_xy[0], proposed_xy[1]))
        proposed_xy_counts[(proposed_xy[0], proposed_xy[1])] += 1

    # Make the moves, though ignore  if there's multiple moving there.
    any_moved = False
    for i, proposed_xy in enumerate(proposed_xys):
        if proposed_xy_counts[proposed_xy] == 1:
            if elf_xys[i] != proposed_xy:
                any_moved = True
            elf_xys[i] = proposed_xy

    return elf_xys, any_moved


def part1():
    elf_xys = load_elf_positions()

    dir_order = ["N", "S", "W", "E"]

    ROUNDS = 10
    for _ in range(ROUNDS):
        elf_xys, any_changed = process_round(elf_xys, dir_order)

        dir_order.append(dir_order.pop(0))

    elf_xys_np = np.array(elf_xys)
    min_x, min_y = np.amin(elf_xys_np, axis=0)
    max_x, max_y = np.amax(elf_xys_np, axis=0)

    num_empty = 0
    elf_xys_set = set(elf_xys)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) not in elf_xys_set:
                num_empty += 1
    print(num_empty)


def part2():
    elf_xys = load_elf_positions()

    dir_order = ["N", "S", "W", "E"]

    rounds = 0
    while True:
        elf_xys, any_changed = process_round(elf_xys, dir_order)
        dir_order.append(dir_order.pop(0))
        if not any_changed:
            print(rounds + 1)
            break
        rounds += 1


part1()
part2()
