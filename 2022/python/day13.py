import functools
import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

A_LT_B = -1
A_GT_B = 1
TIE = 0

def get_order(a, b):
    if isinstance(a, int) and isinstance(b, int):
        # 2 ints.
        if a < b:
            return A_LT_B
        elif a > b:
            return A_GT_B
        else:
            return TIE
    if isinstance(a, list) and isinstance(b, list):
        # 2 lists.
        maxlen = max(len(a), len(b))
        for i in range(maxlen):
            if i >= len(a):
                # A ran out.
                return A_LT_B
            elif i >= len(b):
                # B ran out.
                return A_GT_B
            elem_order = get_order(a[i], b[i])
            if elem_order != TIE:
                return elem_order
        # Reached end of both lists.
        return TIE
    else:
        if isinstance(a, int):
            return get_order([a], b)
        else:
            return get_order(a, [b])


def part1():
    index = 1
    sum_in_order_indices = 0
    lines_no_space = [l for l in lines if l]
    for l1, l2 in zip(lines_no_space[::2], lines_no_space[1::2]):
        packet1 = eval(l1)
        packet2 = eval(l2)

        if get_order(packet1, packet2) == A_LT_B:
            sum_in_order_indices += index

        index += 1

    print(sum_in_order_indices)



def part2():
    packets = [eval(l) for l in lines if l]
    divider1 = [[2]]
    divider2 = [[6]]
    packets += [divider1, divider2]
    sorted_packets = sorted(packets, key=functools.cmp_to_key(get_order))

    i1 = sorted_packets.index(divider1) + 1
    i2 = sorted_packets.index(divider2) + 1

    print(i1 * i2)


part1()
part2()
