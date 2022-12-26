import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

SNAFU_TO_DEC = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
DEC_TO_SNAFU = {v: k for k, v in SNAFU_TO_DEC.items()}


def snafu_to_decimal(s: str) -> int:
    value = 0
    base = 1
    for char in reversed(s):
        value += SNAFU_TO_DEC[char] * base
        base *= 5
    return value


# For a given target digit, and a given base, we can figure out which value is the best to use. We can figure out how many bases we need, by increasing base until we have a leading zero. then, we work backwards from that base.


def snafu_digit_for_base(target: int, base: int) -> int:
    best_digit = 0
    closest = abs(target)
    for d in range(-2, 3):
        value = d * base
        if abs(value - target) < closest:
            closest = abs(value - target)
            best_digit = d
    return best_digit


def decimal_to_snafu(d: int) -> str:
    max_base = 1
    while True:
        digit = snafu_digit_for_base(d, max_base * 5)
        if digit == 0:
            break
        max_base *= 5

    remainder = d
    base = max_base
    result = ""
    while base >= 1:
        digit = snafu_digit_for_base(remainder, base)
        result += DEC_TO_SNAFU[digit]
        remainder = remainder - digit * base
        base /= 5

    return result


def part1():
    sum_decimal = 0
    for line in lines:
        sum_decimal += snafu_to_decimal(line)
    print(decimal_to_snafu(sum_decimal))


def part2():
    pass


part1()
part2()
