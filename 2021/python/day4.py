import sys
from typing import List, Tuple

import numpy as np
import numpy.typing as npt

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def board_won(mark: npt.NDArray[np.bool8]) -> bool:
    for row in range(mark.shape[0]):
        if np.all(mark[row]):
            return True
    for col in range(mark.shape[1]):
        if np.all(mark[:, col]):
            return True
    return False


def compute_final_score(
    board: npt.NDArray[np.int32], mark: npt.NDArray[np.bool8], number: int
) -> int:
    unmarked_sum = np.sum(board[~mark])
    return number * unmarked_sum


def load_data() -> Tuple[
    List[int], List[npt.NDArray[np.int32]], List[npt.NDArray[np.bool8]]
]:
    numbers = [int(x) for x in lines[0].split(",")]
    boards = []
    board_rows = []
    for line in lines[1:]:
        if not line:
            continue
        board_rows.append([int(x) for x in line.split()])
        if len(board_rows) == 5:
            boards.append(np.array(board_rows))
            board_rows.clear()

    board_marks = []
    for board in boards:
        board_marks.append(np.full(board.shape, False))
    return numbers, boards, board_marks


def part1():
    numbers, boards, board_marks = load_data()

    for number in numbers:
        for board, mark in zip(boards, board_marks):
            mark[board == number] = True
            if board_won(mark):
                score = compute_final_score(board, mark, number)
                print(score)
                return


def part2():
    numbers, boards, board_marks = load_data()
    boards_won = [False for _ in boards]
    num_boards_won = 0
    for number in numbers:
        for i, (board, mark) in enumerate(zip(boards, board_marks)):
            if boards_won[i]:
                # No point updating this board if its already won.
                continue
            mark[board == number] = True
            if board_won(mark):
                boards_won[i] = True
                num_boards_won += 1
                if num_boards_won == len(boards):
                    score = compute_final_score(board, mark, number)
                    print(score)
                    return


part1()
part2()
