with open('input') as f:
    image_str = f.readline().strip()

rows=6
cols=25

min_num_zeros = rows*cols
num1s_mul_num2s = None
for i in range(0, len(image_str), rows*cols):
    substr = image_str[i:i+rows*cols]
    num_zeros = substr.count('0')
    num_ones = substr.count('1')
    num_twos = substr.count('2')
    if num_zeros < min_num_zeros:
        num1s_mul_num2s = num_ones * num_twos
        min_num_zeros = num_zeros

print(num1s_mul_num2s)


colors = ['2'] * rows * cols
for i in range(0, len(image_str), rows*cols):
    substr = image_str[i:i+rows*cols]
    for j, pixel in enumerate(substr):
        if colors[j] == '2':
            colors[j] = pixel

print(colors)

ind = 0
for row in range(rows):
    for col in range(cols):
        char = '█' if colors[ind] == '1' else ' '
        print(char, end='')
        ind += 1
    print('')
