from collections import defaultdict
import sys
from typing import DefaultDict, Dict, Tuple


def load_data() -> Tuple[str, Dict[str, str]]:
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()
    polymer = lines[0]
    rules = {}
    for line in lines[2:]:
        rules[line[0:2]] = line[-1]
    return polymer, rules


def do_step(polymer: str, rules: Dict[str, str]) -> str:
    new_inserts = ["" for _ in polymer]
    for i in range(len(polymer) - 1):
        new_inserts[i] = rules.get(polymer[i : i + 2], "")

    return "".join(x for y in zip(polymer, new_inserts) for x in y)


def part1():
    polymer, rules = load_data()
    for _ in range(10):
        polymer = do_step(polymer, rules)
    element_counts = defaultdict(int)
    for e in polymer:
        element_counts[e] += 1
    print(max(element_counts.values()) - min(element_counts.values()))


def do_step2(
    pair_counts: DefaultDict[str, int], rules: Dict[str, str]
) -> DefaultDict[str, int]:
    new_pair_counts = defaultdict(int)
    for pair, count in pair_counts.items():
        rule_output = rules.get(pair, "")
        if not rule_output:
            # This pair just passes along.
            new_pair_counts[pair] += count
        else:
            # This pair gets a new element inserted in the middle, creating 2 new pairs.
            new_pair_counts[pair[0] + rule_output] += count
            new_pair_counts[rule_output + pair[1]] += count

    return new_pair_counts


def part2():
    # Instead of tracking polymers, track the unique pairs, and how many of each pair we have at each step.
    polymer, rules = load_data()
    pair_counts = defaultdict(int)
    for i in range(len(polymer) - 1):
        pair_counts[polymer[i : i + 2]] += 1

    for _ in range(40):
        pair_counts = do_step2(pair_counts, rules)

    # Count up the elements. We gather the first element of each pair, which should be unique.
    # This misses the final element in the polymer, but that will just be the final element in the initial polymer.
    element_counts = defaultdict(int)
    for pair, count in pair_counts.items():
        element_counts[pair[0]] += count
    element_counts[polymer[-1]] += 1
    print(max(element_counts.values()) - min(element_counts.values()))


part1()
part2()
