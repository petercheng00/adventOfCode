import itertools
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


def execute(program, prog_inputs):
    # print(f'running with input {prog_inputs}')
    input_ind = 0
    position = 0
    while True:
        instruction = program[position]
        opcode = int(str(instruction)[-2:])
        param_modes = [int(d) for d in str(instruction)[:-2]]
        param_modes.reverse()
        # print(f'instruction is {instruction}, opcode is {opcode}, param_modes are {param_modes}')
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
            program[dst_ind] = prog_inputs[input_ind]
            input_ind += 1
            position += 2
        elif opcode == 4:
            src = getSrcParam(program, position+1, param_modes, 0)
            # print(f'output: {src}')
            program_output = src
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
            # print('halting')
            return program_output
            break
        else:
            print('error')
            break

def runProgramsWithPhases(program, phases):
    output1 = execute(program, [phases[0], 0])
    output2 = execute(program, [phases[1], output1])
    output3 = execute(program, [phases[2], output2])
    output4 = execute(program, [phases[3], output3])
    output5 = execute(program, [phases[4], output4])
    return output5

max_output = 0

for phase in itertools.permutations([0, 1, 2, 3, 4]):
    output = runProgramsWithPhases(ints, phase)
    max_output = max(output, max_output)
print(max_output)
