from collections import defaultdict
import itertools
with open('input') as f:
    ints = f.readline().split(',')

# remove the newline
ints[-1] = ints[-1].strip()
ints = [int(i) for i in ints]

class Computer:
    def __init__(self, program, inputs=[]):
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

    # step does one instruction at a time, unless halted
    # if on an input instruction and no input available, uses -1
    def step(self):
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
            dst = self.getDstParam(self.position+1, param_modes, 0)
            i = -1
            if len(self.inputs) > 0:
                i = self.inputs.pop(0)
            self.write(dst, i)
            self.position += 2
            if i == -1:
                return 'idle'
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
            print('halt')
            self.halted = True
            return 'halted'
        else:
            print('error')
            self.error = True
            self.halted = True
            return 'error'
        return 'stepped'



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

computers = []
for i in range(50):
    computers.append(Computer(ints, [i]))

while True:
    for c in computers:
        c.step()
    messages = []
    for c in computers:
        while len(c.outputs) >= 3:
            addr = c.outputs.pop(0)
            x = c.outputs.pop(0)
            y = c.outputs.pop(0)
            messages.append((addr, x, y))
    done = False
    for m in messages:
        addr, x, y = m
        if addr == 255:
            print((addr, x, y))
            done = True
            break
        computers[addr].inputs.append(x)
        computers[addr].inputs.append(y)
    for c in computers:
        if c.halted:
            print('halted')
            done = True
    if done:
        break


print('nat time')

computers = []
for i in range(50):
    computers.append(Computer(ints, [i]))

nat_packet = None
last_nat_y = None

# number of times a computer has been idle in a row without an output
idles = [0] * len(computers)


while True:
    for i, c in enumerate(computers):
        result = c.step()
        if result == 'idle':
            idles[i] += 1



    messages = []
    for i, c in enumerate(computers):
        if len(c.outputs) > 0:
            idles[i] = 0
        while len(c.outputs) >= 3:
            addr = c.outputs.pop(0)
            x = c.outputs.pop(0)
            y = c.outputs.pop(0)
            messages.append((addr, x, y))

    if len(messages) > 0:
        idles = [0] * len(computers)

    all_idle = True
    for i in idles:
        if i < 5:
            all_idle = False
            break

    if all_idle:
        # print(idles)
        # print('all idle')
        computers[0].inputs.append(nat_packet[0])
        computers[0].inputs.append(nat_packet[1])
        idles = [0] * len(computers)
        if nat_packet[1] == last_nat_y:
            print('doubled!')
            print(last_nat_y)
            break
        else:
            last_nat_y = nat_packet[1]
        continue



    for m in messages:
        addr, x, y = m
        if addr == 255:
            print('add to nat')
            nat_packet = (x, y)
        else:
            computers[addr].inputs.append(x)
            computers[addr].inputs.append(y)
