from math import ceil
import re
import sys
from typing import List

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

TYPES = [ORE, CLAY, OBSIDIAN, GEODE]

RobotCost = List[int]
Blueprint = List[RobotCost]
RobotInventory = List[int]
MaterialInventory = List[int]


def get_blueprints() -> List[Blueprint]:
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()
    blueprints = []
    for line in lines:
        m = re.search(
            r"ore robot costs (\d+) ore.",
            line,
        )
        assert m
        ore_robot_cost = [0, 0, 0, 0]
        ore_robot_cost[ORE] = int(m.group(1))
        m = re.search(
            r"clay robot costs (\d+) ore.",
            line,
        )
        assert m
        clay_robot_cost = [0, 0, 0, 0]
        clay_robot_cost[ORE] = int(m.group(1))
        m = re.search(
            r"obsidian robot costs (\d+) ore and (\d+) clay.",
            line,
        )
        assert m
        obsidian_robot_cost = [0, 0, 0, 0]
        obsidian_robot_cost[ORE] = int(m.group(1))
        obsidian_robot_cost[CLAY] = int(m.group(2))
        m = re.search(
            r"geode robot costs (\d+) ore and (\d+) obsidian.",
            line,
        )
        assert m
        geode_robot_cost = [0, 0, 0, 0]
        geode_robot_cost[ORE] = int(m.group(1))
        geode_robot_cost[OBSIDIAN] = int(m.group(2))

        blueprints.append(
            [ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost]
        )

    return blueprints


def get_time_to_afford(
    cost: RobotCost, robots: RobotInventory, materials: MaterialInventory
) -> int:
    """Find out how long it will take to be able to afford cost given current robots and materials."""
    time_needed = 0
    for t in TYPES:
        if materials[t] >= cost[t]:
            continue
        if robots[t] == 0:
            return -1
        missing_count = cost[t] - materials[t]
        time_to_aquire = ceil(missing_count / robots[t])
        time_needed = max(time_needed, time_to_aquire)
    return time_needed


def produce_materials(
    robots: RobotInventory, materials: MaterialInventory, time: int
) -> MaterialInventory:
    """Return new materials based on robots producing for given amount of time."""
    return [materials[t] + time * robots[t] for t in TYPES]


def spend_robot_cost(
    materials: MaterialInventory, cost: RobotCost
) -> MaterialInventory:
    """Return new materials with deduceted cost."""
    return [materials[t] - cost[t] for t in TYPES]


def max_geodes_search(
    blueprint: Blueprint,
    time_left: int,
    robots: RobotInventory,
    materials: MaterialInventory,
    max_robots: RobotInventory,
    best_final_result_so_far: int,
) -> int:
    """The main recursive solver."""
    # Theoretical best result we could get right now would involve creating a geode robot in each of the remaining turns.
    theoretical_best = (
        materials[GEODE] + robots[GEODE] * time_left + time_left * (time_left + 1) / 2
    )
    if theoretical_best < best_final_result_so_far:
        return 0

    # For each robot type, determine how long it would take to build that robot.
    # If we have time available, wait that long, generating the resources. then build it. We'll need to spend one extra time step to build the robot.
    best_result = 0
    for t in TYPES:
        if t != GEODE and robots[t] >= max_robots[t]:
            # No point making more of this type.
            continue
        time_to_afford = get_time_to_afford(blueprint[t], robots, materials)
        if time_to_afford < 0:
            # Will never be able to afford.
            continue
        # After we can afford, takes one more time step to complete construction.
        time_to_construct = time_to_afford + 1
        if time_to_construct > time_left:
            # No point trying to construct..
            continue

        # Figure out how many new materials we'd get during the time.
        new_materials = produce_materials(robots, materials, time_to_construct)

        # Also spend materials to create the new robot.
        new_materials = spend_robot_cost(new_materials, blueprint[t])

        # Add the new robot
        new_robots = robots.copy()
        new_robots[t] += 1
        # Update the time.
        new_time_left = time_left - time_to_construct

        result = max_geodes_search(
            blueprint,
            new_time_left,
            new_robots,
            new_materials,
            max_robots,
            max(best_result, best_final_result_so_far),
        )
        best_result = max(result, best_result)
        best_final_result_so_far = max(best_final_result_so_far, best_result)

    if best_result == 0:
        # Can't make any more robots, so just wait out the clock.
        new_materials = produce_materials(robots, materials, time_left)
        return new_materials[GEODE]

    return best_result


def solve_max_geodes(blueprint: Blueprint, time: int) -> int:
    start_robots = [0, 0, 0, 0]
    start_robots[ORE] = 1
    start_materials = [0, 0, 0, 0]
    # Figure out the max number of robots it would ever make sense to produce.
    max_robots = [0, 0, 0, 0]
    for robot_type in TYPES:
        for cost_type in TYPES:
            max_robots[cost_type] = max(
                max_robots[cost_type], blueprint[robot_type][cost_type]
            )

    return max_geodes_search(
        blueprint, time, start_robots, start_materials, max_robots, 0
    )


def part1():
    blueprints = get_blueprints()
    print(f"Loaded {len(blueprints)} blueprints.")
    sum_quality = 0
    for i, bp in enumerate(blueprints):
        print(f"Working on blueprint {i}...")
        result = solve_max_geodes(bp, 24)
        print(result)
        quality = (i + 1) * result
        sum_quality += quality
    print(sum_quality)


def part2():
    blueprints = get_blueprints()[:3]
    print(f"Loaded {len(blueprints)} blueprints.")
    product = 1
    for i, bp in enumerate(blueprints):
        print(f"Working on blueprint {i}...")
        result = solve_max_geodes(bp, 32)
        print(result)
        product *= result
    print(product)


# part1()
part2()
