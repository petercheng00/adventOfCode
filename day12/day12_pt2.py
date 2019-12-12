from fractions import gcd

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

def getPeriodForDim(pos_1d, vel_1d):
    orig_pos_1d = pos_1d.copy()
    orig_vel_1d = vel_1d.copy()
    time = 0
    while True:
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                val1 = pos_1d[i]
                val2 = pos_1d[j]
                if val1 > val2:
                    vel_1d[i] -= 1
                    vel_1d[j] += 1
                elif val1 < val2:
                    vel_1d[i] += 1
                    vel_1d[j] -= 1
        for i in range(len(pos_1d)):
            pos_1d[i] += vel_1d[i]

        time += 1
        if pos_1d == orig_pos_1d and vel_1d == orig_vel_1d:
            return time

def getDim(vec, dim):
    return [v[dim] for v in vec]

period0 = getPeriodForDim(getDim(positions, 0), getDim(velocities, 0))
period1 = getPeriodForDim(getDim(positions, 1), getDim(velocities, 1))
period2 = getPeriodForDim(getDim(positions, 2), getDim(velocities, 2))

lcm01 = (period0 * period1  // gcd(period0, period1))
print(lcm01 * period2 // gcd(lcm01, period2))
