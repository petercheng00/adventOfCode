import itertools
import sys
from typing import Dict, List

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

# If there's <key> unique segments, the number is <value>
UNIQUE_SEGMENTS_TO_NUM = {2: 1, 4: 4, 3: 7, 7: 8}


def part1():
    num_unique_segments_nums = 0
    for line in lines:
        patterns, output = line.split(" | ")
        for output_signal in output.split():
            num_segments = len(set(output_signal))
            if UNIQUE_SEGMENTS_TO_NUM.get(num_segments, None):
                num_unique_segments_nums += 1
    print(num_unique_segments_nums)


##########
# Part 2 #
##########

# Let's refer to the "correct" segments a-g by 0-6.
# For each number, these are the segments that should be active.
NUM_TO_SEGMENTS = [
    {0, 1, 2, 4, 5, 6},
    {2, 5},
    {0, 2, 3, 4, 6},
    {0, 2, 3, 5, 6},
    {1, 2, 3, 5},
    {0, 1, 3, 5, 6},
    {0, 1, 3, 4, 5, 6},
    {0, 2, 5},
    {0, 1, 2, 3, 4, 5, 6},
    {0, 1, 2, 3, 5, 6},
]
# Mapping for the other direction.
SEGMENTS_TO_NUM = {frozenset(x): i for i, x in enumerate(NUM_TO_SEGMENTS)}


def is_mapping_possible(mapping: Dict[str, int], patterns: List[str]) -> bool:
    # Determine if the mapping from coded segment letters to segment numbers is valid for each arrangement in the pattern.
    for pattern in patterns:
        segment_nums = frozenset(mapping[x] for x in pattern)
        if segment_nums not in SEGMENTS_TO_NUM:
            return False
    return True


def decode_patterns(patterns: List[str]) -> Dict[str, int]:
    # Smart approach would be a sudoku-style solver - iteratively reduce possibilities until left with one option.
    # Dumb approach would be to try all possible assignments of letter to number, which is 7! possibilites. Should be tractable. But maybe still ugly code.
    # Let's try the dumb approach first.
    for permutation in itertools.permutations("abcdefg", 7):
        mapping = {x: i for i, x in enumerate(permutation)}
        if is_mapping_possible(mapping, patterns):
            return mapping
    print("Failed to decode patterns!")
    return {}


def decode_output(output: List[str], mapping: Dict[str, int]) -> int:
    result = 0
    for pattern in output:
        segment_nums = frozenset(mapping[x] for x in pattern)
        digit = SEGMENTS_TO_NUM[segment_nums]
        result = 10 * result + digit

    return result


def part2():
    sum_outputs = 0
    for line in lines:
        patterns, output = line.split(" | ")
        patterns = patterns.split()
        output = output.split()
        segment_letters_to_segment_nums = decode_patterns(patterns)
        if not segment_letters_to_segment_nums:
            return
        output = decode_output(output, segment_letters_to_segment_nums)
        sum_outputs += output
    print(sum_outputs)


part1()
part2()
