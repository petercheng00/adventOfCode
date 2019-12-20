with open('input') as f:
    signal = [int(x) for x in f.readline()[0:-1]]

base_pattern = [0, 1, 0, -1]
start_index = int(''.join([str(digit) for digit in signal[0:7]]))

print(start_index)
repeated_pattern = signal * 10000
print(len(repeated_pattern))

offset_pattern = repeated_pattern[start_index:]
print(len(offset_pattern))

for iteration in range(100):
    print(f'{iteration=}')
    next_op = offset_pattern.copy()
    so_far = 0
    for i in range(len(offset_pattern)-1, -1, -1):
        next_op[i] = (offset_pattern[i] + so_far) % 10
        so_far = next_op[i]

    # print(offset_pattern[-5:])
    offset_pattern = next_op
    # print(offset_pattern[-5:])

print(offset_pattern[0:8])
