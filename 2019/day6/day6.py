from collections import defaultdict

with open('input') as f:
    orbit_strs = f.read().splitlines()

orbiters = defaultdict(list)
orbiting = {}
for orbit_str in orbit_strs:
    objs = orbit_str.split(')')
    orbiters[objs[0]].append(objs[1])
    orbiting[objs[1]] = objs[0]

# for each object how many objects is it directly and indirectly orbiting
orbit_num = {'COM': 0}
visit_queue = ['COM']
while len(visit_queue) > 0:
    current = visit_queue.pop(0)
    current_orbit_num = orbit_num[current]
    for obj in orbiters[current]:
        orbit_num[obj] = current_orbit_num + 1
        visit_queue.append(obj)

sum_num = 0
for obj, num in orbit_num.items():
    sum_num += num
print(sum_num)


ancestors = set()
current_you = 'YOU'
current_san = 'SAN'
while True:
    if current_you != 'COM':
        current_you = orbiting[current_you]
        if current_you in ancestors:
            min_ancestor = current_you
            break
        ancestors.add(current_you)
    if current_san != 'COM':
        current_san = orbiting[current_san]
        if current_san in ancestors:
            min_ancestor = current_san
            break
        ancestors.add(current_san)
print(min_ancestor)

you_to_ma = 0
current_you = 'YOU'
while current_you != min_ancestor:
    current_you = orbiting[current_you]
    you_to_ma += 1
san_to_ma = 0
current_san = 'SAN'
while current_san != min_ancestor:
    current_san = orbiting[current_san]
    san_to_ma += 1

print(you_to_ma + san_to_ma - 2)
