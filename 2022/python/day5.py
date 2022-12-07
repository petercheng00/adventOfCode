import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def initial_stacks():
    elems = [[] for x in range(9)]
    for line in lines[:8]:
        for ci, char in enumerate(line):
            if char.isalpha():
                index = ci // 4
                elems[index].append(char)

    stacks = [list(reversed(x)) for x in elems]
    return stacks


def part1():
    stacks = initial_stacks()
    for line in lines[10:]:
        before_from, after_from = line.split(" from ")
        num_to_move = int(before_from.replace("move ", ""))
        src, dst = after_from.split(" to ")
        src = int(src)
        dst = int(dst)
        src -= 1
        dst -= 1
        for x in range(num_to_move):
            stacks[dst].append(stacks[src].pop())
    print(stacks)
    print("".join(x[-1] for x in stacks))


def part2():
    stacks = initial_stacks()
    for line in lines[10:]:
        before_from, after_from = line.split(" from ")
        num_to_move = int(before_from.replace("move ", ""))
        src, dst = after_from.split(" to ")
        src = int(src)
        dst = int(dst)
        src -= 1
        dst -= 1
        stacks[dst] += stacks[src][-num_to_move:]
        stacks[src] = stacks[src][:-num_to_move]
    print(stacks)
    print("".join(x[-1] for x in stacks))


part1()
part2()
