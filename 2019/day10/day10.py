from fractions import gcd

with open('input') as f:
    asteroid_strs = f.readlines()
    asteroid_strs = [a.strip() for a in asteroid_strs]

asteroids = []
for row, row_str in enumerate(asteroid_strs):
    for col, c in enumerate(row_str):
        if c == '#':
            asteroids.append((col, row))

def getDirection(v):
    x = abs(gcd(v[0], v[1]))
    return (v[0]//x, v[1]//x)

def getSqMagnitude(v):
    return v[0]*v[0] + v[1]*v[1]


def occluded(a, b, asteroids):
    a_to_b = (b[0]-a[0], b[1]-a[1])
    ab_dir = getDirection(a_to_b)
    ab_mag = getSqMagnitude(a_to_b)

    for asteroid in asteroids:
        if asteroid == a or asteroid == b:
            continue
        a_to_asteroid = (asteroid[0]-a[0], asteroid[1]-a[1])
        a_to_asteroid_mag = getSqMagnitude(a_to_asteroid)
        if a_to_asteroid_mag >= ab_mag:
            continue
        a_to_asteroid_dir = getDirection(a_to_asteroid)
        if a_to_asteroid_dir == ab_dir:
            return True
    return False

best_location = None
max_num_visible = 0
for i, a in enumerate(asteroids):
    num_visible = 0
    for j, b in enumerate(asteroids):
        if i == j:
            continue
        if not occluded(a, b, asteroids):
            num_visible += 1
    if num_visible > max_num_visible:
        max_num_visible = num_visible
        best_location = a
    print(f'{i} / {len(asteroids)} : {num_visible} : {max_num_visible}')

print(best_location)
print(max_num_visible)
