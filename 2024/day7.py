import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def can_produce(target, current, values):
    if not values:
        return target == current
    return (
        can_produce(target, current + values[0], values[1:])
        or can_produce(target, current * values[0], values[1:])
        or can_produce(target, int(str(current) + str(values[0])), values[1:])
    )


def part1():
    sum_possible = 0
    for line in lines:
        target, values = line.split(": ")
        target = int(target)
        values = [int(x) for x in values.split(" ")]
        if can_produce(target, values[0], values[1:]):
            sum_possible += target
    print(sum_possible)


def part2():
    pass


part1()
part2()
