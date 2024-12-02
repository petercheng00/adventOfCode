import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
    reports = [[int(x) for x in line.split()] for line in lines]


def is_safe(report):
    for direction in [-1, 1]:
        failed = False
        for a, b in zip(report, report[1:]):
            a *= direction
            b *= direction
            if b - a < 1 or b - a > 3:
                failed = True
                break
        if not failed:
            return True
    return False

def is_safe2(report):
    for direction in [-1, 1]:
        failed = False
        for i in range(len(report)-1):
            a = report[i] * direction
            b = report[i+1] * direction
            if b - a < 1 or b - a > 3:
                report_sub1 = report[:i] + report[i+1:]
                report_sub2 = report[:i+1] + report[i+2:]
                failed = not is_safe(report_sub1) and not is_safe(report_sub2)
                break
        if not failed:
            return True
    return False



def day1():
    print(sum(is_safe(report) for report in reports))


def day2():
    print(sum(is_safe2(report) for report in reports))


day1()
day2()
