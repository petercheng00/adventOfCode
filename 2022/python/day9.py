import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def part1():
    head_x = 0
    head_y = 0
    tail_x = 0
    tail_y = 0
    tail_visited = set()
    tail_visited.add((tail_x, tail_y))

    for line in lines:
        direction, steps = line.split(" ")
        steps = int(steps)
        step_x = 0
        step_y = 0
        if direction == "U":
            step_y = 1
        elif direction == "D":
            step_y = -1
        elif direction == "L":
            step_x = -1
        elif direction == "R":
            step_x = 1
        else:
            print("unexpected dir")
        for _ in range(steps):
            head_x += step_x
            head_y += step_y
            if abs(head_x - tail_x) > 1 or abs(head_y - tail_y) > 1:
                tail_x = head_x - step_x
                tail_y = head_y - step_y
                tail_visited.add((tail_x, tail_y))

    print(len(tail_visited))


def get_new_tail_pos(new_head_pos, tail_pos):
    if abs(new_head_pos[0] - tail_pos[0]) <= 1 and abs(new_head_pos[1] - tail_pos[1]) <= 1:
        # tail doesn't need to move.
        return tail_pos
    x_step = 0
    y_step = 0
    if new_head_pos[0] != tail_pos[0]:
        x_step = 1 if new_head_pos[0] > tail_pos[0] else -1
    if new_head_pos[1] != tail_pos[1]:
        y_step = 1 if new_head_pos[1] > tail_pos[1] else -1
    return (tail_pos[0] + x_step, tail_pos[1] + y_step)


def part2():
    num_knots = 10
    knot_locs = [(0,0) for _ in range(num_knots)]
    tail_visited = set()
    tail_visited.add(knot_locs[-1])

    for line in lines:
        direction, steps = line.split(" ")
        steps = int(steps)
        step_x = 0
        step_y = 0
        if direction == "U":
            step_y = 1
        elif direction == "D":
            step_y = -1
        elif direction == "L":
            step_x = -1
        elif direction == "R":
            step_x = 1
        else:
            print("unexpected dir")
        for _ in range(steps):
            knot_locs[0] = (knot_locs[0][0] + step_x, knot_locs[0][1] + step_y)
            for i in range(1, num_knots):
                knot_locs[i] = get_new_tail_pos(knot_locs[i-1], knot_locs[i])
            tail_visited.add(knot_locs[-1])

    print(len(tail_visited))


part1()
part2()
