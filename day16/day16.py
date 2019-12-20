with open('input') as f:
    signal = [int(x) for x in f.readline()[0:-1]]

base_pattern = [0, 1, 0, -1]

for iteration in range(100):
    print(f'{iteration=}')
    nextsignal = signal.copy()
    for i in range(len(signal)):
        # compute element i
        sum_so_far = 0

        base_pattern_ind = 0
        base_pattern_repeats = 1 # because we skip the first element
        for j in range(len(signal)):
            if base_pattern_repeats > i:
                base_pattern_ind = (base_pattern_ind+1) % len(base_pattern)
                base_pattern_repeats = 0

            sum_so_far += signal[j] * base_pattern[base_pattern_ind]

            base_pattern_repeats += 1

        nextsignal[i] = int(str(sum_so_far)[-1])
    signal = nextsignal

print(signal)
