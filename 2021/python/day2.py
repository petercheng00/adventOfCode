import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def part1():
    x = 0
    depth = 0
    for line in lines:
        direction, amount = line.split()
        amount = int(amount)
        if direction == "forward":
            x += amount
        elif direction == "down":
            depth += amount
        elif direction == "up":
            depth -= amount
    print(x * depth)


def part2():
    x = 0
    depth = 0
    aim = 0
    for line in lines:
        direction, amount = line.split()
        amount = int(amount)
        if direction == "forward":
            x += amount
            depth += aim * amount
        elif direction == "down":
            aim += amount
        elif direction == "up":
            aim -= amount
    print(x * depth)


part1()
part2()
