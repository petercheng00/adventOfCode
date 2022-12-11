from dataclasses import dataclass, field
import math
import sys
from typing import List

from tqdm import tqdm

@dataclass
class Monkey:
    item_worries: List[int] = field(default_factory=list)
    operation: str = ""
    divisor: int = -1
    true_dst: int = -1
    false_dst: int = -1

def load_monkeys() -> List[Monkey]:
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()
    monkeys = []
    for line in lines:
        if not line:
            continue
        prefix, suffix = line.split(":")
        if "Monkey" in prefix:
            monkeys.append(Monkey())
        elif "Starting items" in prefix:
            monkeys[-1].item_worries = [int(x) for x in suffix.split(",")]
        elif "Operation" in prefix:
            monkeys[-1].operation = suffix.split("=")[-1]
        elif "Test" in prefix:
            monkeys[-1].divisor = int(suffix.split(" ")[-1])
        elif "If true" in prefix:
            monkeys[-1].true_dst = int(suffix.split(" ")[-1])
        elif "If false" in prefix:
            monkeys[-1].false_dst = int(suffix.split(" ")[-1])
        else:
            print(f"Unexpcted line {line}")

    return monkeys


def part1():
    monkeys = load_monkeys()
    inspect_counts = [0 for _ in monkeys]
    for monkey_round in range(20):
        for i, monkey in enumerate(monkeys):
            for item_worry in monkey.item_worries:
                inspect_counts[i] += 1
                operation = lambda old : eval(monkey.operation)
                new_worry = math.floor(operation(item_worry) / 3)
                dst_monkey = monkey.true_dst if (new_worry % monkey.divisor == 0) else monkey.false_dst
                monkeys[dst_monkey].item_worries.append(new_worry)

            # Assume a monkey can not throw to itself.
            monkey.item_worries = []

    sorted_counts = sorted(inspect_counts)
    print(sorted_counts[-2]*sorted_counts[-1])


def part2():
    monkeys = load_monkeys()
    divisor_prod = math.prod(m.divisor for m in monkeys)
    inspect_counts = [0 for _ in monkeys]
    for monkey_round in tqdm(range(10000)):
        for i, monkey in enumerate(monkeys):
            for item_worry in monkey.item_worries:
                inspect_counts[i] += 1
                operation = lambda old : eval(monkey.operation)
                new_worry = operation(item_worry)
                dst_monkey = monkey.true_dst if (new_worry % monkey.divisor == 0) else monkey.false_dst
                monkeys[dst_monkey].item_worries.append(new_worry % divisor_prod)

            # Assume a monkey can not throw to itself.
            monkey.item_worries = []

    sorted_counts = sorted(inspect_counts)
    print(sorted_counts[-2]*sorted_counts[-1])


part1()
part2()
