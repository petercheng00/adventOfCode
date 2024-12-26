import sys

import numpy as np

with open(sys.argv[1]) as f:
    line = f.read().splitlines()[0]


def part1():
    nums = [int(x) for x in line]
    total_len = sum(nums)
    data = np.zeros(total_len, dtype=int)
    position = 0
    for i, num in enumerate(nums):
        if i % 2 == 0:
            data[position : position + num] = i // 2
        else:
            data[position : position + num] = -1
        position += num

    left_index = 0
    right_index = total_len - 1
    while True:
        # Find right most data block.
        while data[right_index] == -1:
            right_index -= 1
        # Find left most empty space.
        while data[left_index] != -1:
            left_index += 1
        if left_index >= right_index:
            break
        data[left_index] = data[right_index]
        data[right_index] = -1

    checksum = 0
    for i, x in enumerate(data):
        if x == -1:
            break
        checksum += i * x
    print(checksum)


def part2():
    nums = [int(x) for x in line]
    # Each element is data, and len of that data.
    data = []
    for i, x in enumerate(line):
        if int(x) > 0:
            if i % 2 == 0:
                data.append((i // 2, int(x)))
            else:
                data.append((-1, int(x)))
    right_index = len(data) - 1

    last_attempted_id = None

    while right_index >= 0:
        if data[right_index][0] == -1:
            right_index -= 1
            continue
        id, size = data[right_index]
        if last_attempted_id is None or id < last_attempted_id:
            last_attempted_id = id
        else:
            right_index -= 1
            continue
        # scan left to right, until right_index, looking for a free spot.
        free_index = None
        for i in range(0, right_index):
            if data[i][0] == -1 and data[i][1] >= size:
                free_index = i
                break
        if free_index is None:
            right_index -= 1
            continue
        free_size = data[free_index][1]
        data[free_index] = (id, size)
        data[right_index] = (-1, size)
        if free_size == size:
            right_index -= 1
        else:
            data.insert(free_index + 1, (-1, free_size - size))

    checksum = 0
    index = 0
    for d in data:
        if d[0] != -1:
            for i in range(d[1]):
                checksum += d[0] * index
                index += 1
        else:
            index += d[1]

    print(checksum)


part1()
part2()
