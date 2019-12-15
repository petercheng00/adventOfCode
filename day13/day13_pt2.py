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

ints[0] = 2

arcade = Computer(ints, [])
ball_position = None
paddle_position = None
world = defaultdict(int)
ball_direction = None
while not arcade.halted:
    arcade.execute()
    if len(arcade.outputs) % 3 != 0:
        print('error: arcade outputs not a multiple of 3')
        break
    for i in range(0, len(arcade.outputs), 3):
        coord = (arcade.outputs[i], arcade.outputs[i+1])
        val = arcade.outputs[i+2]
        if coord[0] == -1 and coord[1] == 0:
            print(f'score is {val}')
        else:
            world[coord] = val
            if val == 3:
                paddle_position = coord
            elif val == 4:
                if ball_position != None:
                    ball_direction = (coord[0] - ball_position[0], coord[1] - ball_position[1])
                ball_position = coord
    arcade.outputs.clear()
    print(f'{ball_position=} {paddle_position=}')

    if ball_position[0] < paddle_position[0]:
        arcade.inputs.append(-1)
    elif ball_position[0] > paddle_position[0]:
        arcade.inputs.append(1)
    else:
        arcade.inputs.append(0)
    continue


    # doh all the below stuff kept getting stuck in an infinite loop.
    # then I realized ball will bounce off of any corner, not just corners in the direction it is going


    # if ball_direction == None:
    #     arcade.inputs.append(0)
    # else:
    #     # find the ball's next position. if ball is going up and left, can hit objects left, up, or left+up.
    #     vert_test = (ball_position[0], ball_position[1]+ball_direction[1])
    #     side_test = (ball_position[0]+ball_direction[0], ball_position[1])
    #     diag_test = (ball_position[0]+ball_direction[0], ball_position[1]+ball_direction[1])

    #     if world[side_test] != 0 or (world[diag_test] != 0 and world[vert_test] == 0):
    #         # print(f'predict bounce')
    #         target_x = ball_position[0] - ball_direction[0]
    #     else:
    #         target_x = ball_position[0] + ball_direction[0]
    #     # print(f'{target_x=}')

    #     if paddle_position[0] < target_x:
    #         arcade.inputs.append(1)
    #     elif paddle_position[0] > target_x:
    #         arcade.inputs.append(-1)
    #     else:
    #         arcade.inputs.append(0)
    # # print(f'sent input {arcade.inputs[-1]}')
