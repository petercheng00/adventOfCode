positions = []
velocities = []
with open('input') as f:
    lines = f.readlines()
    for line in lines:
        x_ind = line.index('x=')
        x = int(line[x_ind+2:line.index(',',x_ind)])
        y_ind = line.index('y=')
        y = int(line[y_ind+2:line.index(',',y_ind)])
        z_ind = line.index('z=')
        z = int(line[z_ind+2:line.index('>',z_ind)])
        positions.append([x, y, z])
        velocities.append([0, 0, 0])

time = 0
while time < 1000:
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            for dim in range(3):
                val1 = positions[i][dim]
                val2 = positions[j][dim]
                if val1 > val2:
                    velocities[i][dim] -= 1
                    velocities[j][dim] += 1
                elif val1 < val2:
                    velocities[i][dim] += 1
                    velocities[j][dim] -= 1
    for i in range(len(positions)):
        for dim in range(3):
            positions[i][dim] += velocities[i][dim]

    time += 1

sum_energy = 0
for i, pos in enumerate(positions):
    vel = velocities[i]
    pot_energy = abs(pos[0]) + abs(pos[1]) + abs(pos[2])
    kin_energy = abs(vel[0]) + abs(vel[1]) + abs(vel[2])
    sum_energy += (pot_energy * kin_energy)

print(f'energy at time 1000: {sum_energy}')


