import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
    initial_stones = [int(x) for x in lines[0].split()]


def part1():
    stones = initial_stones
    for i in range(25):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(s := str(stone)) % 2 == 0:
                new_stones.append(int(s[: len(s) // 2]))
                new_stones.append(int(s[len(s) // 2 :]))
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
    print(len(stones))


def part2():
    stones = initial_stones
    # cache[(stone, steps to do)] = result
    cache = {}
    num_stones = 0
    for stone in stones:
        num_stones += part2_helper(stone, 75, cache)
    print(num_stones)


def part2_helper(stone, steps, cache):
    if steps == 0:
        return 1
    if (result := cache.get((stone, steps))) is not None:
        return result
    if stone == 0:
        result = part2_helper(1, steps - 1, cache)
    elif len(s := str(stone)) % 2 == 0:
        s1 = int(s[: len(s) // 2])
        s2 = int(s[len(s) // 2 :])
        result = part2_helper(s1, steps - 1, cache) + part2_helper(s2, steps - 1, cache)
    else:
        result = part2_helper(stone * 2024, steps - 1, cache)
    cache[(stone, steps)] = result
    return result


part1()
part2()
