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

def toAscii(outputs):
    return ''.join([chr(o) for o in outputs])

def strToInput(s):
    return [ord(c) for c in s]

def directions(dirs):
    dir_str = ''
    for d in dirs:
        if d == 'n':
            dir_str += 'north\n'
        elif d == 's':
            dir_str += 'south\n'
        elif d == 'w':
            dir_str += 'west\n'
        elif d == 'e':
            dir_str += 'east\n'
        else:
            print('invalid direction')
    return dir_str
def revDirections(dirs):
    dir_str = ''
    for d in dirs[::-1]:
        if d == 's':
            dir_str += 'north\n'
        elif d == 'n':
            dir_str += 'south\n'
        elif d == 'e':
            dir_str += 'west\n'
        elif d == 'w':
            dir_str += 'east\n'
        else:
            print('invalid direction')
    return dir_str

goto_dirs = {'observatory' : 's',
             'navigation' : 'se',
             'holodeck' : 'n',
             'warp drive maintenance' : 'ne',
             'kitchen' : 'nen',
             'sick bay' : 'nenn',
             'hallway' : 'nene',
             'science lab' : 'nw',
             'gift wrapping center' : 'nww',
             'passages' : 'nwww',
             'storage' : 'nwwww',
             'hot chocolate fountain' : 'nwwws',
             'crew quarters' : 'nwn',
             'stables' : 'nwnw',
             'engineering' : 'nwne',
             'corridor' : 'nwnee',
             'arcade' : 'nwnes',
             'security checkpoint' : 'nwnesw'}

safe_items = {'whirled peas' : 'navigation',
              'ornament' : 'warp drive maintenance',
              'dark matter' : 'sick bay',
              'candy cane' : 'gift wrapping center',
              'tambourine' : 'storage',
              'astrolabe' : 'crew quarters',
              'hologram' : 'engineering',
              'klein bottle' : 'corridor'}

def getAllSafeItems():
    all_str = ''
    for item, location in safe_items.items():
        all_str += directions(goto_dirs[location])
        all_str += 'take ' + item + '\n'
        all_str += revDirections(goto_dirs[location])
    return all_str

computer = Computer(ints)
while (True):
    computer.execute()
    print(toAscii(computer.outputs))
    computer.outputs.clear()
    input_str = input("input: ")
    if input_str[:4] == 'goto':
        dst = input_str[5:]
        computer.inputs += strToInput(directions(goto_dirs[dst]))
    elif input_str[:5] == 'leave':
        dst = input_str[6:]
        computer.inputs += strToInput(revDirections(goto_dirs[dst]))
    elif input_str[:6] == 'getall':
        computer.inputs += strToInput(getAllSafeItems())
    elif input_str[:6] == 'tryall':
        items = []
        for i, l in safe_items.items():
            items.append(i)
        for num in range(256):
            all_str = ''
            for item in items:
                all_str += 'drop ' + item + '\n'

            binary_str = format(num, '#010b')[2:]
            for i, char in enumerate(binary_str):
                if char == '1':
                    all_str += 'take ' + items[i] + '\n'
            all_str += 'north\n'

            computer.inputs += strToInput(all_str)
            computer.execute()
            output = toAscii(computer.outputs)
            computer.outputs.clear()
            print(binary_str)
            # print('input!')
            # print(all_str)
            # print('begin output\n\n')
            # print(output)


            if 'Alert' not in output:
                print(output)
                print('no alert found')
                break
    else:
        for c in input_str:
            computer.inputs.append(ord(c))
        computer.inputs.append(10)
