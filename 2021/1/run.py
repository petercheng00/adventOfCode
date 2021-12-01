data = []
with open('input') as f:
    for line in f:
        data.append(int(line))

num_increase = 0
for i in range(1, len(data)):
    if data[i] > data[i-1]:
        num_increase += 1

print(num_increase)

sums3 = []
for i in range(2, len(data)):
    sums3.append(data[i] + data[i-1] + data[i-2])

num_increase3 = 0
for i in range(1, len(sums3)):
    if sums3[i] > sums3[i-1]:
        num_increase3 += 1

print(num_increase3)
