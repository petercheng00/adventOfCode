import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def part1():
    x = 1
    sum_strengths = 0
    cycle = 0
    for line in lines:
        if line == "noop":
            x_incr = 0
            cycle_incr = 1
        else:
            x_incr = int(line.split(" ")[1])
            cycle_incr = 2

        for cycle_step in range(cycle_incr):
            cycle += 1
            if cycle >= 20 and (cycle - 20) % 40 == 0:
                sum_strengths += cycle * x
        x += x_incr

    print(sum_strengths)

def part2():
    x = 1
    cycle = 0
    crt_row = ""
    crt_col = 0
    for line in lines:
        if line == "noop":
            x_incr = 0
            cycle_incr = 1
        else:
            x_incr = int(line.split(" ")[1])
            cycle_incr = 2

        for cycle_step in range(cycle_incr):
            cycle += 1

            # Drawing.
            if abs(crt_col - x) <= 1:
                crt_row += "#"
            else:
                crt_row += "."
            crt_col += 1
            if crt_col >= 40:
                print(crt_row)
                crt_row = ""
                crt_col = 0

        x += x_incr



part1()
part2()
