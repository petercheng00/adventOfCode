import sys
from typing import Dict, List, Set


def load_data() -> Dict[str, List[str]]:
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()
    cave_connections = {}
    for line in lines:
        a, b = line.split("-")
        if a not in cave_connections:
            cave_connections[a] = []
        if b not in cave_connections:
            cave_connections[b] = []
        cave_connections[a].append(b)
        cave_connections[b].append(a)

    return cave_connections


def part1_solver(
    start: str, end: str, connections: Dict[str, List[str]], prohibited_caves: Set[str]
) -> int:
    """Counts the number of paths from start to end, disallowing visits to prohibited caves."""
    if start == end:
        # We're done!
        return 1
    # If we're leaving a small cave, we can't return.
    new_prohibited = prohibited_caves
    if start.islower():
        new_prohibited = new_prohibited.copy()
        new_prohibited.add(start)
    paths = 0
    for neighbor in connections[start]:
        if neighbor.islower():
            if neighbor in prohibited_caves:
                continue
            paths += part1_solver(neighbor, end, connections, new_prohibited)
        else:
            paths += part1_solver(neighbor, end, connections, new_prohibited)

    return paths


def part1():
    connections = load_data()
    print(part1_solver("start", "end", connections, set()))


def part2_solver(
    start: str,
    end: str,
    connections: Dict[str, List[str]],
    prohibited_caves: Set[str],
    used_double_visit: bool,
) -> int:
    """Counts the number of paths from start to end, disallowing visits to prohibited caves. We're allowed one double visit, exluding the start or end spots."""
    if start == end:
        # We're done!
        return 1
    # If we're leaving a small cave, we can't return.
    new_prohibited = prohibited_caves
    if start.islower():
        new_prohibited = new_prohibited.copy()
        new_prohibited.add(start)
    paths = 0
    for neighbor in connections[start]:
        if neighbor.islower():
            if neighbor in prohibited_caves:
                if used_double_visit or neighbor == "start":
                    continue
                else:
                    # We can use our 1 double visit.
                    paths += part2_solver(
                        neighbor, end, connections, new_prohibited, True
                    )
            else:
                paths += part2_solver(
                    neighbor, end, connections, new_prohibited, used_double_visit
                )
        else:
            paths += part2_solver(
                neighbor, end, connections, new_prohibited, used_double_visit
            )

    return paths


def part2():
    connections = load_data()
    print(part2_solver("start", "end", connections, set(), False))


part1()
part2()
