from collections import defaultdict
import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

def parse_filesystem():
    dir_sizes = defaultdict(int)
    current_dir = ["/"]
    line_ind = 0
    while line_ind < len(lines):
        line = lines[line_ind]
        if line.startswith("$ cd"):
            new_dir = line.split(" ")[-1]
            if new_dir == "/":
                current_dir = ["/"]
            elif new_dir == "..":
                current_dir.pop(-1)
            else:
                current_dir.append(new_dir)
        elif line.startswith("$ ls"):
            pass
        else:
            first_elem = line.split(" ")[0]
            if first_elem.isnumeric():
                # add size to all parent dirs also.
                for num_elems in range(len(current_dir)):
                    dir_sizes["_".join(current_dir[0:num_elems+1])] += int(first_elem)
        line_ind += 1

    return dir_sizes


def part1():
    dir_sizes = parse_filesystem()
    sum_lte_100000 = sum(x for x in dir_sizes.values() if x <= 100000)
    print(sum_lte_100000)

def part2():
    dir_sizes = parse_filesystem()
    current_free_space = 70000000 - dir_sizes["/"]
    need_to_free = 30000000 - current_free_space
    min_big_enough_dir_size = min(x for x in dir_sizes.values() if x >= need_to_free)
    print(min_big_enough_dir_size)




part1()
part2()
