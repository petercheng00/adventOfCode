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

class Amplifier:
    def __init__(self, program, inputs):
        self.program = program.copy()
        self.inputs = inputs
        self.halted = False
        self.error = False
        self.position = 0
        self.outputs = []

    # execute ends either when waiting for an input or halted
    def execute(self):
        while True:
            instruction = self.program[self.position]
            opcode = int(str(instruction)[-2:])
            param_modes = [int(d) for d in str(instruction)[:-2]]
            param_modes.reverse()
            # print(f'instruction is {instruction}, opcode is {opcode}, param_modes are {param_modes}')
            if opcode == 1 or opcode == 2: #add, mul
                src1 = getSrcParam(self.program, self.position+1, param_modes, 0)
                src2 = getSrcParam(self.program, self.position+2, param_modes, 1)
                dst_ind = self.program[self.position+3]
                if opcode == 1:
                    self.program[dst_ind] = src1 + src2
                else:
                    self.program[dst_ind] = src1 * src2
                self.position += 4
            elif opcode == 3: #input
                if len(self.inputs) == 0:
                    break
                dst_ind = self.program[self.position+1]
                self.program[dst_ind] = self.inputs.pop(0)
                self.position += 2
            elif opcode == 4: #output
                src = getSrcParam(self.program, self.position+1, param_modes, 0)
                # print(f'output: {src}')
                self.outputs.append(src)
                self.position += 2
            elif opcode == 5 or opcode == 6: #jumpiftrue, jumpiffalse
                src1 = getSrcParam(self.program, self.position+1, param_modes, 0)
                src2 = getSrcParam(self.program, self.position+2, param_modes, 1)
                if opcode == 5 and src1 != 0:
                    self.position = src2
                elif opcode == 6 and src1 == 0:
                    self.position = src2
                else:
                    self.position += 3
            elif opcode == 7 or opcode == 8: #lt, equals
                src1 = getSrcParam(self.program, self.position+1, param_modes, 0)
                src2 = getSrcParam(self.program, self.position+2, param_modes, 1)
                dst_ind = self.program[self.position+3]
                if opcode == 7:
                    self.program[dst_ind] = 1 if src1 < src2 else 0
                elif opcode == 8:
                    self.program[dst_ind] = 1 if src1 == src2 else 0
                self.position += 4
            elif opcode == 99:
                # print('halt')
                self.halted = True
                break
            else:
                print('error')
                self.error = True
                self.halted = True
                break

def runProgramsWithPhases(program, phases):
    amplifiers = []
    for i, phase in enumerate(phases):
        amplifiers.append(Amplifier(program, [phase]))

    amplifiers[0].inputs.append(0)

    current_amp = 0
    while True:
        # print(f'amp {current_amp}')
        amplifiers[current_amp].execute()
        # print(amplifiers[current_amp].outputs)
        current_output = amplifiers[current_amp].outputs.pop(0)
        if not current_output:
            print('error: no output')
            return 0

        next_amp = (current_amp + 1) % len(amplifiers)
        amplifiers[next_amp].inputs.append(current_output)
        if next_amp == 0 and amplifiers[current_amp].halted:
            return current_output
        current_amp = next_amp

# ints = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
# print(runProgramsWithPhases(ints, [9,8,7,6,5]))

max_output = 0
for phases in itertools.permutations([5, 6, 7, 8, 9]):
    output = runProgramsWithPhases(ints, phases)
    print(output)
    max_output = max(output, max_output)
print(max_output)
