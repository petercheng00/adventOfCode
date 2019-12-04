lowest = 137683
highest = 596253

count = 0
for int_num in range(lowest, highest+1):
    str_num = str(int_num)
    num_dups = 0
    valid = True
    for i in range(len(str_num) - 1):
        if str_num[i] > str_num[i+1]:
            valid = False
            break
        if str_num[i] == str_num[i+1]:
            num_dups += 1
    if valid and num_dups > 0:
        count += 1
print(count)

count = 0
for int_num in range(lowest, highest+1):
    str_num = str(int_num)
    num_exact2_dups = 0
    current_num_dups = 0
    valid = True
    for i in range(len(str_num) - 1):
        if str_num[i] > str_num[i+1]:
            valid = False
            break
        if str_num[i] == str_num[i+1]:
            current_num_dups += 1
        else:
            if current_num_dups == 1:
                num_exact2_dups += 1
            current_num_dups = 0
    if current_num_dups == 1:
        num_exact2_dups += 1

    if valid and num_exact2_dups > 0:
        count += 1
print(count)
