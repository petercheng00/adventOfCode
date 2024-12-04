import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def day1():
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    target = "XMAS"

    count = 0
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            if lines[row][col] != target[0]:
                continue
            for direction in directions:
                for step in range(1, len(target)):
                    r = row + step * direction[0]
                    c = col + step * direction[1]
                    if r < 0 or r >= len(lines) or c < 0 or c >= len(lines[0]):
                        break
                    if lines[r][c] != target[step]:
                        break
                    if step == len(target) - 1:
                        count += 1
    print(count)


def day2():
    pair1 = [(-1, -1), (1, 1)]
    pair2 = [(-1, 1), (1, -1)]
    count = 0
    for row in range(1, len(lines) - 1):
        for col in range(1, len(lines[0]) - 1):
            if lines[row][col] != "A":
                continue
            failed = False
            for pair in [pair1, pair2]:
                (d1, d2) = pair
                c1 = lines[row + d1[0]][col + d1[1]]
                c2 = lines[row + d2[0]][col + d2[1]]
                if not ((c1 == "M" and c2 == "S") or (c1 == "S" and c2 == "M")):
                    failed = True
                    break
            if not failed:
                count += 1
    print(count)


day1()
day2()
