from collections import defaultdict
import itertools
with open('input') as f:
    ints = f.readline().split(',')

# remove the newline
ints[-1] = ints[-1].strip()
ints = [int(i) for i in ints]

class Computer:
    def __init__(self, program, inputs):
        self.program = program.copy()
        self.inputs = inputs.copy()
        self.halted = False
        self.error = False
        self.position = 0
        self.relative_base = 0
        self.outputs = []
        self.extra_memory = {}

    def read(self, addr):
        if addr < len(self.program):
            return self.program[addr]
        if addr in self.extra_memory:
            return self.extra_memory[addr]
        return 0

    def write(self, addr, value):
        if addr < len(self.program):
            self.program[addr] = value
        else:
            self.extra_memory[addr] = value

    def getSrcParam(self, position, param_modes, param_index):
        param_mode = param_modes[param_index] if param_index < len(param_modes) else 0
        param_val = self.read(position)
        if param_mode == 0:
            return self.read(param_val)
        elif param_mode == 1:
            return param_val
        elif param_mode == 2:
            return self.read(self.relative_base + param_val)
        else:
            print(f'bad param mode {param_mode}')

    def getDstParam(self, position, param_modes, param_index):
        param_mode = param_modes[param_index] if param_index < len(param_modes) else 0
        param_val = self.read(position)
        if param_mode == 0:
            return param_val
        elif param_mode == 2:
            return self.relative_base + param_val
        else:
            print(f'bad param mode {param_mode}')

    # execute ends either when waiting for an input or halted
    def execute(self):
        while True:
            instruction = self.program[self.position]
            opcode = int(str(instruction)[-2:])
            param_modes = [int(d) for d in str(instruction)[:-2]]
            param_modes.reverse()
            # print(f'instruction is {instruction}, opcode is {opcode}, param_modes are {param_modes}')
            if opcode == 1 or opcode == 2: #add, mul
                src1 = self.getSrcParam(self.position+1, param_modes, 0)
                src2 = self.getSrcParam(self.position+2, param_modes, 1)
                dst = self.getDstParam(self.position+3, param_modes, 2)
                if opcode == 1:
                    self.write(dst, src1 + src2)
                else:
                    self.write(dst, src1 * src2)
                self.position += 4
            elif opcode == 3: #input
                if len(self.inputs) == 0:
                    break
                dst = self.getDstParam(self.position+1, param_modes, 0)
                self.write(dst, self.inputs.pop(0))
                self.position += 2
            elif opcode == 4: #output
                src = self.getSrcParam(self.position+1, param_modes, 0)
                self.outputs.append(src)
                self.position += 2
            elif opcode == 5 or opcode == 6: #jumpiftrue, jumpiffalse
                src1 = self.getSrcParam(self.position+1, param_modes, 0)
                src2 = self.getSrcParam(self.position+2, param_modes, 1)
                if opcode == 5 and src1 != 0:
                    self.position = src2
                elif opcode == 6 and src1 == 0:
                    self.position = src2
                else:
                    self.position += 3
            elif opcode == 7 or opcode == 8: #lt, equals
                src1 = self.getSrcParam(self.position+1, param_modes, 0)
                src2 = self.getSrcParam(self.position+2, param_modes, 1)
                dst = self.getDstParam(self.position+3, param_modes, 2)
                if opcode == 7:
                    self.write(dst, 1 if src1 < src2 else 0)
                elif opcode == 8:
                    self.write(dst, 1 if src1 == src2 else 0)
                self.position += 4
            elif opcode == 9: # set relative base
                src = self.getSrcParam(self.position+1, param_modes, 0)
                self.relative_base += src
                self.position += 2
            elif opcode == 99:
                # print('halt')
                self.halted = True
                break
            else:
                print('error')
                self.error = True
                self.halted = True
                break


# the plan will be to do bfs. for each valid set of inputs so far, we will try adding each of the 4 inputs to make new set of valid inputs. we will prune out any input sequences that hit a wall or do backtracking

def getVisitedCoords(inputs):
    vc = [(0,0)]
    for i in inputs:
        x, y = vc[-1] # y is north
        if i == 1: # north
            vc.append((x, y+1))
        elif i == 2: # south
            vc.append((x, y-1))
        elif i == 3: # west
            vc.append((x-1, y))
        elif i == 4: # east
            vc.append((x+1, y))
    return vc

def repeated_coord(vc_set, last_coord, i):
    x, y = last_coord
    if i == 1: # north
        return (x, y+1) in vc_set
    elif i == 2: # south
        return (x, y-1) in vc_set
    elif i == 3: # west
        return (x-1, y) in vc_set
    elif i == 4: # east
        return (x+1, y) in vc_set

def submitInputs(inputs):
    c = Computer(ints, inputs)
    c.execute()
    return c.outputs[-1]

# from part 1. so now we start with this input and find what's the longest sequence that can be tacked onto this. backtracking checks do not include this prefix
input_prefix = [4, 4, 1, 1, 4, 4, 2, 2, 2, 2, 4, 4, 4, 4, 1, 1, 3, 3, 1, 1, 4, 4, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 2, 2, 3, 3, 2, 2, 4, 4, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 4, 4, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 1, 1, 1, 1, 4, 4, 1, 1, 3, 3, 1, 1, 4, 4, 1, 1, 3, 3, 1, 1, 4, 4, 4, 4, 2, 2, 4, 4, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 1, 1, 3, 3, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 4, 4, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 3, 3, 2, 2, 3, 3, 1, 1, 1, 1, 1, 1, 4, 4, 2, 2, 4, 4, 4, 4, 2, 2, 4, 4, 1, 1, 4, 4, 1, 1, 3, 3, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 2, 2, 3, 3, 1, 1, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 2, 2, 4, 4, 1, 1]
valid_inputs=[[]]
while len(valid_inputs) > 0:
    print(f'num valid: {len(valid_inputs)} input size: {len(valid_inputs[0])}')
    next_valid_inputs = []
    for valid_input in valid_inputs:
        visited_coords = getVisitedCoords(valid_input)
        last_coord = visited_coords[-1]
        vc_set = set(visited_coords)
        for direction in [1, 2, 3, 4]:
            if repeated_coord(vc_set, last_coord, direction):
                continue
            new_input = valid_input + [direction]
            result = submitInputs(input_prefix + new_input)
            if result == 0:
                continue
            elif result == 1:
                next_valid_inputs.append(new_input)
            # can't get result == 2 now since it's our starting position
    valid_inputs = next_valid_inputs
