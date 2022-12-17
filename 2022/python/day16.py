import re
import sys
from typing import Dict, List, Tuple

from tqdm import tqdm


def get_distance(a: str, b: str, neighbors: Dict[str, List[str]]):
    to_explore = [(a, 0)]
    explored = set()

    while to_explore:
        position, distance = to_explore.pop(0)
        if position == b:
            return distance
        explored.add(position)
        for neighbor in neighbors[position]:
            if neighbor not in explored:
                to_explore.append((neighbor, distance + 1))


def load_data():
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    valves = []
    flow_rates = {}
    neighbors = {}

    for line in lines:
        m = re.match(
            r"Valve (.+) has flow rate=(.+); tunnel(s)? lead(s)? to valve(s)? (.+)",
            line,
        )
        valve_name = m.group(1)
        flow_rate = int(m.group(2))
        valve_neighbors = [x.strip() for x in m.group(6).split(",")]

        valves.append(valve_name)
        flow_rates[valve_name] = flow_rate
        neighbors[valve_name] = valve_neighbors

    distances = {}
    # Compute distance from each valve to each other valve.
    for a in valves:
        for b in valves:
            if (a, b) in distances:
                continue
            distance = get_distance(a, b, neighbors)
            distances[(a, b)] = distance
            distances[(b, a)] = distance

    return valves, flow_rates, distances


def part1_solver(
    valves: List[str],
    flow_rates: Dict[str, int],
    distances: Dict[Tuple[str, str], int],
    position: str,
    valve_states: Dict[str, bool],
    time_elapsed: int,
    pressure_released: int,
    max_time: int,
):
    # How much pressure we release per time currently.
    current_flow_rate = sum(flow_rates[x] for x in valves if valve_states[x])

    # For each unopened valve, we have the option to take that as the next step (if there is enough time left)
    future_results = []
    for valve in valves:
        if valve_states[valve]:
            # Already opened.
            continue
        # Takes time to reach that valve and then open it.
        time_to_open = distances[(position, valve)] + 1
        if time_elapsed + time_to_open >= max_time:
            continue

        new_position = valve
        new_valve_states = valve_states.copy()
        new_valve_states[valve] = True
        new_time_elapsed = time_elapsed + time_to_open
        new_pressure_released = pressure_released + current_flow_rate * time_to_open
        future_results.append(
            part1_solver(
                valves,
                flow_rates,
                distances,
                new_position,
                new_valve_states,
                new_time_elapsed,
                new_pressure_released,
                max_time,
            )
        )
    if not future_results:
        # If there is no time to visit any unopened valves, or if all valves are open, then we just wait out the time.
        time_left = max_time - time_elapsed
        return pressure_released + current_flow_rate * time_left
    else:
        return max(future_results)


def part1():
    # instead, let's get the distance from each valve to each other valve.
    # then, the search space becomes deciding which valve to open next, and each possible action is just going to that valve and opening it, and adding on the corresponding amount of time.

    all_valves, flow_rates, distances = load_data()
    useful_valves = [x for x in all_valves if flow_rates[x] > 0]
    position = "AA"
    valve_states = {x: False for x in useful_valves}
    time_elapsed = 0
    pressure_released = 0
    max_time = 30
    print(
        part1_solver(
            useful_valves,
            flow_rates,
            distances,
            position,
            valve_states,
            time_elapsed,
            pressure_released,
            max_time,
        )
    )


def get_all_subgroups(valves):
    if not valves:
        return [[]]
    next_subgroups = get_all_subgroups(valves[1:])
    added = [[valves[0]] + x.copy() for x in next_subgroups]
    return next_subgroups + added


def part2():
    all_valves, flow_rates, distances = load_data()
    useful_valves = [x for x in all_valves if flow_rates[x] > 0]

    # Strategy: Divide the valves into 2 groups, solve each group independently, add results. Try all possible groups.
    all_subgroups = get_all_subgroups(useful_valves)

    position = "AA"
    time_elapsed = 0
    pressure_released = 0
    max_time = 26

    results = []
    for subgroup in tqdm(all_subgroups):
        group1 = subgroup
        group2 = [x for x in useful_valves if x not in group1]

        valve_states1 = {x: False for x in group1}
        valve_states2 = {x: False for x in group2}

        result1 = part1_solver(
            group1,
            flow_rates,
            distances,
            position,
            valve_states1,
            time_elapsed,
            pressure_released,
            max_time,
        )
        result2 = part1_solver(
            group2,
            flow_rates,
            distances,
            position,
            valve_states2,
            time_elapsed,
            pressure_released,
            max_time,
        )
        results.append(result1 + result2)

    print(max(results))


part1()
part2()
