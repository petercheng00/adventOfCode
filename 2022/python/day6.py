from collections import defaultdict
import sys


with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def find_unique_chars_substr(substr_len):
    line = lines[0]
    counts = defaultdict(int)
    num_dup_chars = 0
    for i, c in enumerate(line):
        counts[c] += 1
        if counts[c] == 2:
            num_dup_chars += 1
        if i >= substr_len:
            removed_char = line[i - substr_len]
            counts[removed_char] -= 1
            if counts[removed_char] == 1:
                num_dup_chars -= 1
        if i >= substr_len - 1 and num_dup_chars == 0:
            print(i + 1)
            return


def part1():
    find_unique_chars_substr(4)


def part2():
    find_unique_chars_substr(14)


part1()
part2()
