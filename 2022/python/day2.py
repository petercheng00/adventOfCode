import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def get_score(opp_move, my_move):
    move_score = 1 + my_move
    if my_move == opp_move:
        result_score = 3
    elif my_move == (opp_move + 1) % 3:
        result_score = 6
    else:
        result_score = 0
    return move_score + result_score


def part1():
    score = 0

    for line in lines:
        opp_move, my_move = line.split(" ")
        opp_move = ord(opp_move) - ord("A")
        my_move = ord(my_move) - ord("X")
        score += get_score(opp_move, my_move)

    print(score)


def part2():
    score = 0

    for line in lines:
        opp_move, goal = line.split(" ")
        opp_move = ord(opp_move) - ord("A")
        goal = ord(goal) - ord("X")

        if goal == 0:
            my_move = (opp_move + 3 - 1) % 3
        elif goal == 1:
            my_move = opp_move
        elif goal == 2:
            my_move = (opp_move + 1) % 3

        score += get_score(opp_move, my_move)

    print(score)


part1()
part2()
