import re
import sys

with open(sys.argv[1]) as f:
    data = f.read()


def day1():
    pattern = r"mul\((\d+),(\d+)\)"
    matches = re.findall(pattern, data)
    print(sum(int(a) * int(b) for a, b in matches))
    
def day2():
    do_indices = [m.start() for m in re.finditer("do\(\)", data)]
    dont_indices = [m.start() for m in re.finditer("don't\(\)", data)]
    pattern = r"mul\((\d+),(\d+)\)"
    matches = re.finditer(pattern, data)

    enabled = True
    sum = 0
    for m in matches:
        m_index = m.start()
        while True:
            next_do_index = do_indices[0] if do_indices else len(data)
            next_dont_index = dont_indices[0] if dont_indices else len(data)
            if next_do_index < next_dont_index and next_do_index < m_index:
                enabled = True
                do_indices.pop(0)
            elif next_dont_index < next_do_index and next_dont_index < m_index:
                enabled = False
                dont_indices.pop(0)
            else:
                break
        if enabled:
           sum += int(m.group(1)) * int(m.group(2))
    print(sum)


day1()
day2()
