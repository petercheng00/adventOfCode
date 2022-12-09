import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def part1():
    sum = 0
    max_sum = 0
    for line in lines:
        if line.isnumeric():
            sum += int(line)
        else:
            max_sum = max(max_sum, sum)
            sum = 0
    max_sum = max(max_sum, sum)

    print(max_sum)


def part2():
    sum = 0
    max1_sum = 0
    max2_sum = 0
    max3_sum = 0
    for line in lines:
        if line.isnumeric():
            sum += int(line)
        else:
            if sum >= max1_sum:
                max3_sum = max2_sum
                max2_sum = max1_sum
                max1_sum = sum
            elif sum >= max2_sum:
                max3_sum = max2_sum
                max2_sum = sum
            elif sum > max3_sum:
                max3_sum = sum
            sum = 0
    if sum >= max1_sum:
        max3_sum = max2_sum
        max2_sum = max1_sum
        max1_sum = sum
    elif sum >= max2_sum:
        max3_sum = max2_sum
        max2_sum = sum
    elif sum > max3_sum:
        max3_sum = sum

    print(max1_sum + max2_sum + max3_sum)


part1()
part2()
