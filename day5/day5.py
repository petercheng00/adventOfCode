with open('input') as f:
    ints = f.readline().split(',')

# remove the newline
ints[-1] = ints[-1].strip()
ints = [int(i) for i in ints]

def getSrcParam(program, position, param_modes, param_index):
    param_mode = param_modes[param_index] if param_index < len(param_modes) else 0
    param_val = program[position]
    if param_mode == 0:
        return program[param_val]
    elif param_mode == 1:
        return param_val
    else:
        print(f'bad param mode {param_mode}')


def execute(program, prog_input):
    print(f'running with input {prog_input}')
    position = 0
    while True:
        instruction = program[position]
        opcode = int(str(instruction)[-2:])
        param_modes = [int(d) for d in str(instruction)[:-2]]
        param_modes.reverse()
        print(f'instruction is {instruction}, opcode is {opcode}, param_modes are {param_modes}')
        if opcode == 1 or opcode == 2:
            src1 = getSrcParam(program, position+1, param_modes, 0)
            src2 = getSrcParam(program, position+2, param_modes, 1)
            dst_ind = program[position+3]
            if opcode == 1:
                program[dst_ind] = src1 + src2
            else:
                program[dst_ind] = src1 * src2
            position += 4
        elif opcode == 3:
            dst_ind = program[position+1]
            program[dst_ind] = prog_input
            position += 2
        elif opcode == 4:
            src = getSrcParam(program, position+1, param_modes, 0)
            print(f'output: {src}')
            position += 2
        elif opcode == 5 or opcode == 6:
            src1 = getSrcParam(program, position+1, param_modes, 0)
            src2 = getSrcParam(program, position+2, param_modes, 1)
            if opcode == 5 and src1 != 0:
                position = src2
            elif opcode == 6 and src1 == 0:
                position = src2
            else:
                position += 3
        elif opcode == 7 or opcode == 8:
            src1 = getSrcParam(program, position+1, param_modes, 0)
            src2 = getSrcParam(program, position+2, param_modes, 1)
            dst_ind = program[position+3]
            if opcode == 7:
                program[dst_ind] = 1 if src1 < src2 else 0
            elif opcode == 8:
                program[dst_ind] = 1 if src1 == src2 else 0
            position += 4
        elif opcode == 99:
            print('halting')
            break
        else:
            print('error')
            break

# print(execute(ints, 1))
# print(execute(ints, 5))

test_eq_8_pos = [3,9,8,9,10,9,4,9,99,-1,8]
test_lt_8_pos = [3,9,7,9,10,9,4,9,99,-1,8]
test_eq_8_im = [3,3,1108,-1,8,3,4,3,99]
test_lt_8_im = [3,3,1107,-1,8,3,4,3,99]

test_nonzero_pos = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
test_nonzero_im = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

test_large = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

print(execute(ints, 5))
