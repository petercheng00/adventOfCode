import sys

BRACES = {"(": ")", "[": "]", "{": "}", "<": ">"}
ILLEGAL_SCORE = {")": 3, "]": 57, "}": 1197, ">": 25137}
COMPLETION_SCORE = {")": 1, "]": 2, "}": 3, ">": 4}

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def get_illegal_score(line: str) -> int:
    opened_queue = []
    for c in line:
        if c in BRACES.keys():
            opened_queue.append(c)
        else:
            if not opened_queue or c != BRACES[opened_queue[-1]]:
                return ILLEGAL_SCORE[c]
            else:
                opened_queue.pop()
    return 0


def part1():
    sum_illegal_score = 0
    for line in lines:
        sum_illegal_score += get_illegal_score(line)
    print(sum_illegal_score)


def get_completion_score(line: str) -> int:
    opened_queue = []
    for c in line:
        if c in BRACES.keys():
            opened_queue.append(c)
        else:
            assert c == BRACES[opened_queue[-1]]
            opened_queue.pop()

    score = 0
    for opener in reversed(opened_queue):
        closer = BRACES[opener]
        score = score * 5 + COMPLETION_SCORE[closer]

    return score


def part2():
    completion_scores = []
    for line in lines:
        if get_illegal_score(line) > 0:
            continue
        completion_scores.append(get_completion_score(line))
    completion_scores.sort()
    print(completion_scores[len(completion_scores) // 2])


part1()
part2()
