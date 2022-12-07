import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def part1():
    count = 0
    for line in lines:
        p1, p2 = line.split(",")
        p11, p12 = p1.split("-")
        p21, p22 = p2.split("-")
        if int(p11) <= int(p21) and int(p12) >= int(p22):
            count += 1
        elif int(p21) <= int(p11) and int(p22) >= int(p12):
            count += 1
    print(count)


def part2():
    count = 0
    for line in lines:
        p1, p2 = line.split(",")
        p11, p12 = p1.split("-")
        p21, p22 = p2.split("-")
        p11 = int(p11)
        p12 = int(p12)
        p21 = int(p21)
        p22 = int(p22)
        if p11 >= p21 and p11 <= p22:
            count += 1
        elif p12 >= p21 and p11 <= p22:
            count += 1
        elif p21 >= p11 and p21 <= p12:
            count += 1
        elif p22 >= p11 and p22 <= p12:
            count += 1
    print(count)

    pass


part1()
part2()
