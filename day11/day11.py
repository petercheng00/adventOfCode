import itertools
with open('input') as f:
    ints = f.readline().split(',')

# remove the newline
ints[-1] = ints[-1].strip()
ints = [int(i) for i in ints]

class Computer:
    def __init__(self, program, inputs):
        self.program = program.copy()
        self.inputs = inputs
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

def applyTurn(current_dir, turn): # 0 is left, 1 is right
    if current_dir == 'U':
        return 'L' if turn == 0 else 'R'
    if current_dir == 'R':
        return 'U' if turn == 0 else 'D'
    if current_dir == 'D':
        return 'R' if turn == 0 else 'L'
    if current_dir == 'L':
        return 'D' if turn == 0 else 'U'

def moveForward(current_dir, pos):
    if current_dir == 'U':
        return (pos[0], pos[1]-1)
    if current_dir == 'R':
        return (pos[0]+1, pos[1])
    if current_dir == 'D':
        return (pos[0], pos[1]+1)
    if current_dir == 'L':
        return (pos[0]-1, pos[1])

robot = Computer(ints, [])
panels = {}
current_position = (0, 0)
current_dir = 'U'

while True:
    current_color = panels[current_position] if current_position in panels else 0
    robot.inputs.append(current_color)
    robot.execute()
    if len(robot.outputs) == 2:
        color = robot.outputs[0]
        turn = robot.outputs[1]
        robot.outputs.clear()
        panels[current_position] = color
        current_dir = applyTurn(current_dir, turn)
        current_position = moveForward(current_dir, current_position)
    else:
        print(f'unexpected num robot outputs! {len(robot.outputs)}')
    if robot.halted:
        print('robot halt!')
        break

print(f'start black, num panels painted: {len(panels)}')


#### part 2

robot = Computer(ints, [])
panels = {}
current_position = (0, 0)
current_dir = 'U'
panels[current_position] = 1

while True:
    current_color = panels[current_position] if current_position in panels else 0
    robot.inputs.append(current_color)
    robot.execute()
    if len(robot.outputs) == 2:
        color = robot.outputs[0]
        turn = robot.outputs[1]
        robot.outputs.clear()
        panels[current_position] = color
        current_dir = applyTurn(current_dir, turn)
        current_position = moveForward(current_dir, current_position)
    else:
        print(f'unexpected num robot outputs! {len(robot.outputs)}')
    if robot.halted:
        print('robot halt!')
        break

print(f'start white, num panels painted: {len(panels)}')

min_x = 0
max_x = 0
min_y = 0
max_y = 0
for pos in panels:
    min_x = min(min_x, pos[0])
    max_x = max(max_x, pos[0])
    min_y = min(min_y, pos[1])
    max_y = max(max_y, pos[1])

for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
        pos = (x, y)
        color = panels[pos] if pos in panels else 0
        print('█' if color==1 else ' ', end ='')
    print('')
