import sys

import numpy as np

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
    list_of_lists = [[int(x) for x in line] for line in lines]
    grid = np.array(list_of_lists)

def part1():
    visible = np.full(grid.shape, False)
    rows, cols = grid.shape
    for row in range(rows):
        # traverse L->R
        tallest = -1
        for col in range(cols):
            if grid[row, col] > tallest:
                visible[row, col] = True
                tallest = max(grid[row, col], tallest)
        # traverse R->L
        tallest = -1
        for col in reversed(range(cols)):
            if grid[row, col] > tallest:
                visible[row, col] = True
                tallest = max(grid[row, col], tallest)
    for col in range(cols):
        # traverse T->B
        tallest = -1
        for row in range(rows):
            if grid[row, col] > tallest:
                visible[row, col] = True
                tallest = max(grid[row, col], tallest)
        # traverse B->T
        tallest = -1
        for row in reversed(range(rows)):
            if grid[row, col] > tallest:
                visible[row, col] = True
                tallest = max(grid[row, col], tallest)
    print(np.count_nonzero(visible))

def part2():
    rows, cols = grid.shape

    look_left_score = np.full(grid.shape, 0)
    for row in range(rows):
        height_occluded_pos = [0] * 10
        for col in range(cols):
            height = grid[row, col]
            look_left_score[row, col] = col - height_occluded_pos[height]
            for h in range(0, height+1):
                height_occluded_pos[h] = col

    look_right_score = np.full(grid.shape, 0)
    for row in range(rows):
        height_occluded_pos = [cols-1] * 10
        for col in reversed(range(cols)):
            height = grid[row, col]
            look_right_score[row, col] = height_occluded_pos[height] - col
            for h in range(0, height+1):
                height_occluded_pos[h] = col

    look_up_score = np.full(grid.shape, 0)
    for col in range(cols):
        height_occluded_pos = [0] * 10
        for row in range(rows):
            height = grid[row, col]
            look_up_score[row, col] = row - height_occluded_pos[height]
            for h in range(0, height+1):
                height_occluded_pos[h] = row

    look_down_score = np.full(grid.shape, 0)
    for col in range(cols):
        height_occluded_pos = [rows-1] * 10
        for row in reversed(range(rows)):
            height = grid[row, col]
            look_down_score[row, col] = height_occluded_pos[height] - row
            for h in range(0, height+1):
                height_occluded_pos[h] = row


    score = np.multiply(look_left_score, np.multiply(look_right_score, np.multiply(look_up_score, look_down_score)))
    print(np.max(score))


part1()
part2()
