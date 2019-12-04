import numpy as np

with open('input') as f:
    path1 = f.readline().split(',')
    path2 = f.readline().split(',')
    path1[-1] = path1[-1].strip()
    path2[-1] = path2[-1].strip()

# use [x, y] convention where positive is up and right
def stepToVector(step):
    direction = step[0]
    magnitude = int(step[1:])
    if direction == 'U':
        return np.array([0, magnitude])
    elif direction == 'D':
        return np.array([0, -magnitude])
    elif direction == 'L':
        return np.array([-magnitude, 0])
    elif direction == 'R':
        return np.array([magnitude, 0])
    else:
        print(f'Unexpected direction {direction}')

def getSegments(path):
    segments = []
    distances = []
    position = np.array([0, 0])
    distance_before = 0 # distance before corresponding segment
    for step in path:
        new_pos = position + stepToVector(step)
        segments.append((position, new_pos))
        distances.append(distance_before)
        position = new_pos
        distance_before += int(step[1:])
    return segments, distances


segments1, distances1 = getSegments(path1)
segments2, distances2 = getSegments(path2)

def getBestOption(option1, option2):
    if option1 == option2:
        return option1
    if option1 > 0 and option2 > 0:
        return min(option1, option2)
    if option1 < 0 and option2 < 0:
        return max(option1, option2)
    else:
        return 0

def intersect(segment1, segment2):
    s1_min_x = min(segment1[0][0], segment1[1][0])
    s1_max_x = max(segment1[0][0], segment1[1][0])
    s1_min_y = min(segment1[0][1], segment1[1][1])
    s1_max_y = max(segment1[0][1], segment1[1][1])
    s2_min_x = min(segment2[0][0], segment2[1][0])
    s2_max_x = max(segment2[0][0], segment2[1][0])
    s2_min_y = min(segment2[0][1], segment2[1][1])
    s2_max_y = max(segment2[0][1], segment2[1][1])
    x_intersect = s1_max_x >= s2_min_x and s1_min_x <= s2_max_x
    y_intersect = s1_max_y >= s2_min_y and s1_min_y <= s2_max_y

    if not x_intersect or not y_intersect:
        return None

    # in case of colinear, we have multiple options
    x_option1 = max(s1_min_x, s2_min_x)
    x_option2 = min(s1_max_x, s2_max_x)
    y_option1 = max(s1_min_y, s2_min_y)
    y_option2 = min(s1_max_y, s2_max_y)
    return np.array([getBestOption(x_option1, x_option2),
                     getBestOption(y_option1, y_option2)])

best_manhat_distance = -1
for i1, segment1 in enumerate(segments1):
    for i2, segment2 in enumerate(segments2):
        if i1 == 0 and i2 == 0:
            # can't count initial center as intersection
            # though this does miss the case where first paths
            # are colinear
            continue
        intersection = intersect(segment1, segment2)
        if intersection is not None:
            manhat_distance = abs(intersection[0]) + abs(intersection[1])
            if best_manhat_distance < 0 or manhat_distance < best_manhat_distance:
                best_manhat_distance = manhat_distance

print(f'best manhat intersection: {best_manhat_distance}')


best_wire_distance = -1
for i1, segment1 in enumerate(segments1):
    for i2, segment2 in enumerate(segments2):
        if i1 == 0 and i2 == 0:
            # can't count initial center as intersection
            # though this does miss the case where first paths
            # are colinear
            continue
        intersection = intersect(segment1, segment2)
        if intersection is not None:
            pre_distance1 = distances1[i1]
            pre_distance2 = distances2[i2]
            post_distance1 = np.abs(intersection - segment1[0]).sum()
            post_distance2 = np.abs(intersection - segment2[0]).sum()
            distance = pre_distance1 + pre_distance2 + post_distance1 + post_distance2
            if best_wire_distance < 0 or distance < best_wire_distance:
                best_wire_distance = distance

print(f'best wire intersection: {best_wire_distance}')
