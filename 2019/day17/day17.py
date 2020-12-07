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

computer = Computer(ints)
computer.execute()

rows = []
start_row = True
for elem in computer.outputs:
    if elem == 10:
        start_row = True
        continue
    if start_row:
        rows.append('')
        start_row = False
    rows[-1] += str(chr(elem))

for row in rows:
    print(row)

width = len(rows[0])
height = len(rows)


sum_intersect_prod = 0
for row_ind in range(1, height-1):
    for col_ind in range(1, width-1):
        if rows[row_ind][col_ind] == '#' and rows[row_ind-1][col_ind] == '#' and rows[row_ind+1][col_ind] == '#' and rows[row_ind][col_ind-1] == '#' and rows[row_ind][col_ind+1] == '#':
            sum_intersect_prod += row_ind * col_ind

print(f'{sum_intersect_prod=}')


# rows=['#######...#####','#.....#...#...#','#.....#...#...#','......#...#...#','......#...###.#','......#.....#.#','^########...#.#','......#.#...#.#','......#########','........#...#..','....#########..','....#...#......','....#...#......','....#...#......','....#####......']
# height = len(rows)
# width = len(rows[0])


# begin part 2
# let's first figure out the full sequence that navigates the full path
# padding is nice
padded_rows = rows.copy()
padded_rows = ['.' * width] + padded_rows + ['.' * width]
padded_rows = ['.' + pr + '.' for pr in padded_rows]

for row in range(height):
    for col in range(width):
        char = padded_rows[row][col]
        if char == '^' or char == 'v' or char == '<' or char == '>':
            robot_char = char
            robot_row = row
            robot_col = col

if robot_char == '^':
    direction = 'U'
elif robot_char == 'v':
    direction = 'D'
elif robot_char == '<':
    direction = 'L'
elif robot_char == '>':
    direction = 'R'

dirs = ['U', 'R', 'D', 'L']
steps = {'U':(-1, 0), 'R':(0, 1), 'D':(1, 0), 'L':(0, -1)}
opposite = {'U':'D', 'D':'U', 'R':'L', 'L':'R'}
turns = {('U','L'):'L',('U','R'):'R',('R','U'):'L',('R','D'):'R',('D','L'):'R',('D','R'):'L',('L','U'):'R',('L','D'):'L'}
first_move = True
moves = []
while (True):
    new_direction = None
    for d in dirs:
        if not first_move and d == opposite[direction]:
            continue
        step = steps[d]
        if padded_rows[robot_row + step[0]][robot_col + step[1]] == '#':
            new_direction = d
            break
    if new_direction == None:
        break
    moves.append(turns[(direction, new_direction)])
    first_move = False
    direction = new_direction
    num_moves = 0
    step = steps[direction]
    while (True):
        if padded_rows[robot_row + step[0]][robot_col + step[1]] == '#':
            robot_row += step[0]
            robot_col += step[1]
            num_moves += 1
        else:
            break
    moves.append(num_moves)

# convert the moves to comma separated string
moves = [str(m) for m in moves]
print(moves)


# now we need to come up with 3 strings which together can represent all of moves
# let's just brute force it
# state is [current list of substrings], [num elements matched]
# if num elements matched == len(moves), we are successful
# otherwise we have some moves available
# match next n elements to one of the existing substrings if possible
# create a new substring, matching the next n elements, if < 3 substrings
# if neither possible, we've failed
# or if we've made more than 20 moves, we've also failed
labels=['A', 'B', 'C']
def recursiveMatch(substrings, num_matched, main):
    if num_matched == len(moves):
        print('SUCCESS!')
        return (substrings, main)
    if len(main) >= 10:
        return False
    # see if any existing substrings work
    remaining = len(moves) - num_matched
    for i, substring in enumerate(substrings):
        if remaining >= len(substring) and moves[num_matched:num_matched+len(substring)] == substring:
            results = recursiveMatch(substrings, num_matched + len(substring), main + [labels[i]])
            if results:
                return results
    # create a new substring from the next n elements
    if len(substrings) >= 3:
        return False
    for i in range(10):
        new_substring = moves[num_matched:num_matched+i+1]
        label = labels[len(substrings)]
        results = recursiveMatch(substrings + [new_substring], num_matched + len(new_substring), main + [label])
        if results:
            return results

routines, main = recursiveMatch([], 0, [])

print(f'{main=}')
print(f'{routines=}')

ints[0] = 2
computer = Computer(ints)
for i,m in enumerate(main):
    for c in m:
        computer.inputs.append(ord(c))
    if i == len(main)-1:
        computer.inputs.append(10) # newline
    else:
        computer.inputs.append(44) # comma

for routine in routines:
    for i, r in enumerate(routine):
        for c in r:
            computer.inputs.append(ord(c))
        if i == len(routine)-1:
            computer.inputs.append(10) # newline
        else:
            computer.inputs.append(44) # comma

print(computer.inputs)


computer.inputs.append(ord('n'))
computer.inputs.append(10)
computer.execute()
print(computer.outputs)
print(computer.halted)
