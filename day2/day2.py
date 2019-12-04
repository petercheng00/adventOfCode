with open('input') as f:
    ints = f.readline().split(',')

# remove the newline
ints[-1] = ints[-1].strip()
ints = [int(i) for i in ints]

def execute(orig_program, noun, verb):
    program = orig_program.copy()
    program[1] = noun
    program[2] = verb
    position = 0
    while True:
        opcode = program[position]
        if opcode == 1 or opcode == 2:
            src_ind1 = program[position+1]
            src_ind2 = program[position+2]
            dst_ind = program[position+3]
            if opcode == 1:
                program[dst_ind] = program[src_ind1] + program[src_ind2]
            else:
                program[dst_ind] = program[src_ind1] * program[src_ind2]
            position += 4
        elif opcode == 99:
            break
        else:
            print('error')
            break

    return program[0]

print(execute(ints, 12, 2))

for noun in range(0, 100):
    for verb in range(0, 100):
        if execute(ints, noun, verb) == 19690720:
            print (100 * noun + verb)
