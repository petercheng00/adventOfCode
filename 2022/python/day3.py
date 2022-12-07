import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def part1():
    sum_priority = 0
    for line in lines:
        common = set(line[: len(line) // 2]) & set(line[len(line) // 2 :])
        char = next(iter(common))
        if char.islower():
            sum_priority += ord(char) - ord("a") + 1
        else:
            sum_priority += ord(char) - ord("A") + 27
    print(sum_priority)


def part2():
    sum_priority = 0
    for l1, l2, l3 in zip(lines[::3], lines[1::3], lines[2::3]):
        common = set(l1) & set(l2) & set(l3)
        char = next(iter(common))
        if char.islower():
            sum_priority += ord(char) - ord("a") + 1
        else:
            sum_priority += ord(char) - ord("A") + 27
    print(sum_priority)


part1()
part2()
