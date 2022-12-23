import sys
from typing import Dict

from sympy import symbols, solve

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def get_value(key: str, input_dict: Dict[str, str], cache: Dict[str, int]) -> int:
    if key in cache:
        return cache[key]

    l, op, r = input_dict[key].split()

    l_val = get_value(l, input_dict, cache)
    r_val = get_value(r, input_dict, cache)

    result = int(eval(f"{l_val} {op} {r_val}"))
    cache[key] = result
    return result


def part1():
    input_dict = {}
    for line in lines:
        key, val = line.split(": ")
        input_dict[key] = val

    cache = {k: int(v) for k, v in input_dict.items() if v.isnumeric()}
    print(get_value("root", input_dict, cache))


def expand(key: str, input_dict: Dict[str, str], cache: Dict[str, str]) -> str:
    if key == "humn":
        return key
    if key in cache:
        return cache[key]

    l, op, r = input_dict[key].split()

    l_expanded = expand(l, input_dict, cache)
    r_expanded = expand(r, input_dict, cache)

    if l_expanded.isnumeric() and r_expanded.isnumeric():
        result = str(int(eval(f"{l_expanded} {op} {r_expanded}")))
    else:
        result = f"({l_expanded} {op} {r_expanded})"
    cache[key] = result
    return result


def part2():
    input_dict = {}
    for line in lines:
        key, val = line.split(": ")
        input_dict[key] = val

    cache = {k: v for k, v in input_dict.items() if v.isnumeric()}

    l_side, _, r_side = input_dict["root"].split()

    l_side = expand(l_side, input_dict, cache)
    r_side = expand(r_side, input_dict, cache)

    humn = symbols("humn")
    print(solve(f"{l_side} - {r_side}"))


part1()
part2()
