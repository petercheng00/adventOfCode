import sys
from collections import defaultdict

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

rules_after = defaultdict(list)
rules_before = defaultdict(list)
updates = []
read_rules = False
for line in lines:
    if line == "":
        read_rules = True
        continue
    if not read_rules:
        a, b = line.split("|")
        rules_after[int(a)].append(int(b))
        rules_before[int(b)].append(int(a))
    else:
        updates.append([int(x) for x in line.split(",")])


def valid_update(update):
    seen = set()
    for x in update:
        for required_after in rules_after[x]:
            if required_after in seen:
                return False
        seen.add(x)
    return True

def fix_update(update):
    remaining = update.copy()
    fixed = []
    while remaining:
        for i in range(len(remaining)):
            safe_to_insert = True
            for required_before in rules_before[remaining[i]]:
                if required_before in remaining:
                    safe_to_insert = False
                    break
            if safe_to_insert:
                fixed.append(remaining.pop(i))
                break
    return fixed

def part1():
    sum = 0
    for update in updates:
        if valid_update(update):
            sum += update[len(update) // 2]
    print(sum)

def part2():
    sum = 0
    for update in updates:
        if not valid_update(update):
            fixed = fix_update(update)
            sum += fixed[len(fixed) // 2]
    print(sum)


part1()
part2()
