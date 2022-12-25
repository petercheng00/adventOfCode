import sys
from typing import Dict, List, Tuple

import numpy as np

OPEN = "."
WALL = "#"
EMPTY = " "

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
CLOCKWISE_DIRS = [RIGHT, DOWN, LEFT, UP]
DIR_VECTORS = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]


def load_data() -> Tuple[np.ndarray, str]:
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()
    board = lines[:-2]
    path = lines[-1]

    # Pad out trailing spaces so each board row is same length.
    max_board_row_len = max(len(x) for x in board)
    board = [x.ljust(max_board_row_len) for x in board]

    # Convert board to numpy ndarray.
    board = np.array([list(x) for x in board])
    return board, path


def find_minmax_rowcol(
    board: np.ndarray,
) -> Tuple[List[int], List[int], List[int], List[int]]:
    # Find min/max rows/cols to speed up wrapping.
    # Could do some numpy trickery to do this faster, but this works.
    rows, cols = board.shape
    min_col_per_row = [0] * rows
    max_col_per_row = [0] * rows
    for row in range(rows):
        for col in range(cols):
            if board[row, col] != EMPTY:
                min_col_per_row[row] = col
                break
        for col in reversed(range(cols)):
            if board[row, col] != EMPTY:
                max_col_per_row[row] = col
                break
    min_row_per_col = [0] * cols
    max_row_per_col = [0] * cols
    for col in range(cols):
        for row in range(rows):
            if board[row, col] != EMPTY:
                min_row_per_col[col] = row
                break
        for row in reversed(range(rows)):
            if board[row, col] != EMPTY:
                max_row_per_col[col] = row
                break

    return min_col_per_row, max_col_per_row, min_row_per_col, max_row_per_col


def go_forward(
    board: np.ndarray,
    xy: np.ndarray,
    direction: int,
    steps: int,
    min_col_per_row: List[int],
    max_col_per_row: List[int],
    min_row_per_col: List[int],
    max_row_per_col: List[int],
) -> np.ndarray:
    for _ in range(steps):
        next_xy = xy + DIR_VECTORS[direction]
        if (
            next_xy[0] < 0
            or next_xy[0] >= board.shape[1]
            or next_xy[1] < 0
            or next_xy[1] >= board.shape[0]
            or board[next_xy[1], next_xy[0]] == EMPTY
        ):
            # Wrap around.
            if direction == LEFT:
                next_xy[0] = max_col_per_row[next_xy[1]]
            elif direction == RIGHT:
                next_xy[0] = min_col_per_row[next_xy[1]]
            elif direction == UP:
                next_xy[1] = max_row_per_col[next_xy[0]]
            elif direction == DOWN:
                next_xy[1] = min_row_per_col[next_xy[0]]

        if board[next_xy[1], next_xy[0]] == WALL:
            # Hit a wall. Can't go any further.
            break
        xy = next_xy
    return xy


def turn_left(direction: int) -> int:
    return (direction - 1) % 4


def turn_right(direction: int) -> int:
    return (direction + 1) % 4


def part1():
    board, path = load_data()

    (
        min_col_per_row,
        max_col_per_row,
        min_row_per_col,
        max_row_per_col,
    ) = find_minmax_rowcol(board)

    # Find start position
    start_row = 0
    start_col = min_col_per_row[start_row]
    while board[start_row, start_col] != OPEN:
        start_col += 1

    start_direction = RIGHT

    current_xy = np.array([start_col, start_row])
    current_direction = start_direction

    remaining_path = path

    while remaining_path:
        num_numeric = 0
        while remaining_path[: num_numeric + 1].isnumeric() and num_numeric <= len(
            remaining_path
        ):
            num_numeric += 1
        if num_numeric > 0:
            forward_steps = int(remaining_path[:num_numeric])
            current_xy = go_forward(
                board,
                current_xy,
                current_direction,
                forward_steps,
                min_col_per_row,
                max_col_per_row,
                min_row_per_col,
                max_row_per_col,
            )
            remaining_path = remaining_path[num_numeric:]

        else:
            turn_direction = remaining_path[0]
            if turn_direction == "L":
                current_direction = turn_left(current_direction)
            else:
                current_direction = turn_right(current_direction)
            remaining_path = remaining_path[1:]

    # 1-indexed positions needed for password
    print(1000 * (current_xy[1] + 1) + 4 * (current_xy[0] + 1) + current_direction)


def go_forward_cube(
    board: np.ndarray,
    xy: np.ndarray,
    direction: int,
    steps: int,
    wrap_map: Dict[Tuple[int, int, int], Tuple[int, int, int]],
) -> Tuple[np.ndarray, int]:
    for _ in range(steps):
        next_xy = xy + DIR_VECTORS[direction]
        next_direction = direction
        wrap_spot = wrap_map.get((next_xy[0], next_xy[1], next_direction))
        if wrap_spot:
            next_xy[0], next_xy[1], next_direction = wrap_spot

        # Make sure we didn't screw up the wrapping.
        assert board[next_xy[1], next_xy[0]] != EMPTY

        if board[next_xy[1], next_xy[0]] == WALL:
            # Hit a wall. Can't go any further.
            break
        xy = next_xy
        direction = next_direction
    return xy, direction


def part2():
    # Create a lookup for each cube edge traversal.
    # dict[(x, y, direction)] = (new_x, new_y, new_direction)

    # Hardcoded for specific input shape.
    # Which looks like:
    ###############
    #    AAABBB
    #    AAABBB
    #    AAABBB
    #    CCC
    #    CCC
    #    CCC
    # DDDEEE
    # DDDEEE
    # DDDEEE
    # FFF
    # FFF
    # FFF

    CUBE_SIZE = 50

    wrap_map = {}

    for i in range(CUBE_SIZE):
        # going right off of B ends in going left into E
        wrap_map[(150, i, RIGHT)] = (99, 149 - i, LEFT)
        # going right off of C ends in going up into B
        wrap_map[(100, 50 + i, RIGHT)] = (100 + i, 49, UP)
        # going right off of E ends in going left into B
        wrap_map[(100, 100 + i, RIGHT)] = (149, 49 - i, LEFT)
        # going right off of F ends in going up into E
        wrap_map[(50, 150 + i, RIGHT)] = (50 + i, 149, UP)

        # going down off of B ends in going left into C
        wrap_map[(100 + i, 50, DOWN)] = (99, 50 + i, LEFT)
        # going down off of E ends in going left into F
        wrap_map[(50 + i, 150, DOWN)] = (49, 150 + i, LEFT)
        # going down off of F ends in going down into B
        wrap_map[(i, 200, DOWN)] = (100 + i, 0, DOWN)

        # going left off of A ends in going right into D
        wrap_map[(49, i, LEFT)] = (0, 149 - i, RIGHT)
        # going left off of C ends in going down into D
        wrap_map[(49, 50 + i, LEFT)] = (i, 100, DOWN)
        # going left off of D ends in going right into A
        wrap_map[(-1, 100 + i, LEFT)] = (50, 49 - i, RIGHT)
        # going left off of F ends in going down into A
        wrap_map[(-1, 150 + i, LEFT)] = (50 + i, 0, DOWN)

        # going up off of A ends in going right into F
        wrap_map[(50 + i, -1, UP)] = (0, 150 + i, RIGHT)
        # going up off of B ends in going up into F
        wrap_map[(100 + i, -1, UP)] = (i, 199, UP)
        # going up off of D ends in going right into C
        wrap_map[(i, 99, UP)] = (50, 50 + i, RIGHT)

    board, path = load_data()

    # Find start position
    start_row = 0
    start_col = 0
    while board[start_row, start_col] != OPEN:
        start_col += 1

    start_direction = RIGHT

    current_xy = np.array([start_col, start_row])
    current_direction = start_direction

    remaining_path = path

    while remaining_path:
        num_numeric = 0
        while remaining_path[: num_numeric + 1].isnumeric() and num_numeric <= len(
            remaining_path
        ):
            num_numeric += 1
        if num_numeric > 0:
            forward_steps = int(remaining_path[:num_numeric])
            current_xy, current_direction = go_forward_cube(
                board, current_xy, current_direction, forward_steps, wrap_map
            )
            remaining_path = remaining_path[num_numeric:]

        else:
            turn_direction = remaining_path[0]
            if turn_direction == "L":
                current_direction = turn_left(current_direction)
            else:
                current_direction = turn_right(current_direction)
            remaining_path = remaining_path[1:]

    # 1-indexed positions needed for password
    print(1000 * (current_xy[1] + 1) + 4 * (current_xy[0] + 1) + current_direction)


part1()
part2()
