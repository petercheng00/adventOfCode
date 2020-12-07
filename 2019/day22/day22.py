with open('input') as f:
    instructions = [l.strip() for l in f.readlines()]

num_cards = 10007

def newStack(index):
    return (num_cards-1) - index

def cut(index, x):
    return (index-x) % num_cards

def dealIncrement(index, x):
    return (index*x) % num_cards

index = 2019
for instruction in instructions:
    if instruction == 'deal into new stack':
        index = newStack(index)
    elif instruction[0:3] == 'cut':
        index = cut(index, int(instruction[3:]))
    elif instruction[0:19] == 'deal with increment':
        index = dealIncrement(index, int(instruction[19:]))
    else:
        print(f'unknown instruction {instruction}')
        break
print(index)

# now for part 2
num_cards = 119315717514047
num_shuffles = 101741582076661

def reverseCut(index, x):
    return (index+x) % num_cards


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def reverseRun(index):
    for instruction in reversed(instructions):
        if instruction == 'deal into new stack':
            index = (num_cards-1) - index
        elif instruction[0:3] == 'cut':
            x = int(instruction[3:])
            index = (index+x) % num_cards
        elif instruction[0:19] == 'deal with increment':
            x = int(instruction[19:])
            index = (index * modinv(x, num_cards)) % num_cards
        else:
            print(f'unknown instruction {instruction}')
            break
    return index

x = 2020
y = reverseRun(x)
z = reverseRun(y)

print(x)
print(y)
print(z)


# X = 2020
# Y = f(X)
# Z = f(Y)
# A = (Y-Z) * modinv(X-Y+D, D) % D
# B = (Y-A*X) % D

a = ((y-z) * modinv(x-y+num_cards, num_cards)) % num_cards
b = (y - a * x) % num_cards
print(f'{a=}')
print(f'{b=}')

# now we need to apply this lots of times
# borrowed from reddit comment
# f^n(x) = A^n*x + A^(n-1)*B + A^(n-2)*B + ... + B
#        = A^n*x + (A^(n-1) + A^(n-2) + ... + 1) * B
#        = A^n*x + (A^n-1) / (A-1) * B
print((pow(a, num_shuffles, num_cards) * 2020 + (pow(a, num_shuffles, num_cards)-1) * modinv(a-1, num_cards) * b) % num_cards)
