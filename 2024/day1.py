import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def day1():
    list1 = [int(line.split()[0]) for line in lines]
    list2 = [int(line.split()[1]) for line in lines]
    list1.sort()
    list2.sort()
    diffs = [abs(a - b) for a, b in zip(list1, list2)]
    print(sum(diffs))


def day2():
    list1 = [int(line.split()[0]) for line in lines]
    list2 = [int(line.split()[1]) for line in lines]
    list2_counts = {}
    for x in list2:
        list2_counts[x] = list2_counts.get(x, 0) + 1
    sum = 0
    for x in list1:
        sum += x * list2_counts.get(x, 0)
    print(sum)


day1()
day2()
