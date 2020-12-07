def fuelRequired(mass):
    return mass // 3 - 2

sum_fuel = 0
with open('input') as f:
    for line in f:
        sum_fuel += fuelRequired(int(line))

print(f'pt1: {sum_fuel}')


sum_fuel = 0
with open('input') as f:
    for line in f:
        module_fuel = fuelRequired(int(line))
        fuel_for_fuel = fuelRequired(module_fuel)
        while fuel_for_fuel > 0:
            module_fuel += fuel_for_fuel
            fuel_for_fuel = fuelRequired(fuel_for_fuel)
        sum_fuel += module_fuel

print(f'pt2: {sum_fuel}')
