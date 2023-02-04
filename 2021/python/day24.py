import sys
from typing import Dict, List, Tuple

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def verify_pattern():
    # Run this to make sure input is as repetitive as it looks.
    x = 0
    count = 0
    while True:
        assert lines[x] == "inp w"
        x += 1
        assert lines[x] == "mul x 0"
        x += 1
        assert lines[x] == "add x z"
        x += 1
        assert lines[x] == "mod x 26"
        x += 1
        assert lines[x].startswith("div z")
        x += 1
        assert lines[x].startswith("add x")
        x += 1
        assert lines[x] == "eql x w"
        x += 1
        assert lines[x] == "eql x 0"
        x += 1
        assert lines[x] == "mul y 0"
        x += 1
        assert lines[x] == "add y 25"
        x += 1
        assert lines[x] == "mul y x"
        x += 1
        assert lines[x] == "add y 1"
        x += 1
        assert lines[x] == "mul z y"
        x += 1
        assert lines[x] == "mul y 0"
        x += 1
        assert lines[x] == "add y w"
        x += 1
        assert lines[x].startswith("add y")
        x += 1
        assert lines[x] == "mul y x"
        x += 1
        assert lines[x] == "add z y"
        x += 1
        count += 1
        if x >= len(lines):
            break
    print(f"Pattern verified {count} times")


def load_input():
    list_pattern_args = []
    start = 0
    while start < len(lines):
        line4 = lines[start + 4]
        line5 = lines[start + 5]
        line15 = lines[start + 15]
        list_pattern_args.append(
            (int(line4.split()[-1]), int(line5.split()[-1]), int(line15.split()[-1]))
        )
        start += 18
    return list_pattern_args


def forward_pass(w_input: int, z_input: int, z_div: int, x_add: int, y_add: int) -> int:
    w = w_input
    z = z_input

    x = z_input
    x %= 26
    z //= z_div
    x += x_add

    x = 1 if x == w else 0
    x = 1 if x == 0 else 0

    y = 25
    y *= x
    y += 1

    z *= y

    y = w
    y += y_add

    y *= x

    z += y

    return z


def part1():
    verify_pattern()

    pattern_args = load_input()

    z_to_largest_prefix = {0: 0}

    for input_num in range(14):
        next_z_to_largest_prefix = {}
        for z, prefix in z_to_largest_prefix.items():
            for w in range(1, 10):
                next_z = forward_pass(w, z, *pattern_args[input_num])
                number = prefix * 10 + w
                curr_number = next_z_to_largest_prefix.get(next_z, 0)
                if number > curr_number:
                    next_z_to_largest_prefix[next_z] = number
        z_to_largest_prefix = next_z_to_largest_prefix
        print(
            f"After step {input_num}, have {len(z_to_largest_prefix)} (max would be {9**(input_num+1)})"
        )

    print(z_to_largest_prefix.get(0, "Failed!"))


def part2():
    pattern_args = load_input()

    z_to_smallest_prefix = {0: 0}

    for input_num in range(14):
        next_z_to_smallest_prefix = {}
        for z, prefix in z_to_smallest_prefix.items():
            for w in range(1, 10):
                next_z = forward_pass(w, z, *pattern_args[input_num])
                number = prefix * 10 + w
                curr_number = next_z_to_smallest_prefix.get(next_z, 999999999999999999)
                if number < curr_number:
                    next_z_to_smallest_prefix[next_z] = number
        z_to_smallest_prefix = next_z_to_smallest_prefix
        print(
            f"After step {input_num}, have {len(z_to_smallest_prefix)} (max would be {9**(input_num+1)})"
        )

    print(z_to_smallest_prefix.get(0, "Failed!"))


part1()
part2()
