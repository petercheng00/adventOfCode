from collections import defaultdict
from fractions import gcd
import math

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

station = (22, 28)


# idea will be to group all asteroids into direction buckets. then within each bucket sort by distance
# then we can just iterate through each bucket, popping off the front each time
# direction buckets need to be sorted first up, then clockwise

asteroid_directions = defaultdict(list)
for asteroid in asteroids:
    if asteroid == station:
        continue
    v = (asteroid[0] - station[0], asteroid[1] - station[1])
    d = getDirection(v)
    asteroid_directions[d].append(asteroid)

# sort each list's contents by magnitude
for _, asteroids in asteroid_directions.items():
    asteroids.sort(key=lambda x: getSqMagnitude((x[0]-station[0], x[1]-station[1])))

# to make trigonometry easier, we'll group by quadrant
# these are lists of direction
ur_asteroids = []
dr_asteroids = []
dl_asteroids = []
ul_asteroids = []
for direction in asteroid_directions:
    if direction[0] >= 0:
        if direction[1] < 0:
            ur_asteroids.append(direction)
        else:
            dr_asteroids.append(direction)
    else:
        if direction[1] >= 0:
            dl_asteroids.append(direction)
        else:
            ul_asteroids.append(direction)

def unit_vectorX(d):
    mag = math.sqrt(d[0]*d[0]+d[1]*d[1])
    return d[0] / mag

# sort within each quadrant by angle
ur_asteroids.sort(key=unit_vectorX)
dr_asteroids.sort(key=unit_vectorX, reverse=True)
dl_asteroids.sort(key=unit_vectorX, reverse=True)
ul_asteroids.sort(key=unit_vectorX)

sorted_asteroid_dirs = ur_asteroids + dr_asteroids + dl_asteroids + ul_asteroids

num_destroyed = 0
while num_destroyed < 200:
    for asteroid_dir in sorted_asteroid_dirs:
        if len(asteroid_directions[asteroid_dir]) > 0:
            asteroid = asteroid_directions[asteroid_dir].pop(0)
            num_destroyed += 1
            print(f'destroyed {num_destroyed} : {asteroid}')
            if num_destroyed == 200:
                break
