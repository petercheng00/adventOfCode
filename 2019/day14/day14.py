import math
from collections import defaultdict
# elements are keys, values are (<num output produced>, [(input element, amount), (input element, amount), ...]
recipes = {}
with open('input') as f:
    recipes_str = f.readlines()
    for recipe in recipes_str:
        recipe = recipe.replace(',', '')
        recipe = recipe.split()
        output = recipe[-1]
        output_amount = int(recipe[-2])
        inputs = []
        for i in range(0, len(recipe)-3, 2):
            inputs.append((recipe[i+1], int(recipe[i])))
        recipes[output] = (output_amount, inputs)

def getOreCostsForFuel(fuel_amount):
    ore_costs = 0
    required = {'FUEL': fuel_amount}
    surplus = defaultdict(int)

    while len(required) > 0:
        required_element, required_amount = required.popitem()
        if required_element == 'ORE':
            ore_costs += required_amount
            continue
        output_amount, inputs = recipes[required_element]
        num_copies = math.ceil(required_amount / output_amount)
        for input_element, input_amount in inputs:
            input_amount *= num_copies
            if surplus[input_element] <= input_amount:
                # use up all the surplus
                input_amount -= surplus[input_element]
                surplus[input_element] = 0
            else:
                # surplus can satisfy this input requirement
                surplus[input_element] -= input_amount
                continue
            if input_element in required:
                required[input_element] += input_amount
            else:
                required[input_element] = input_amount

        # we might have some extra output
        surplus[required_element] += (output_amount * num_copies - required_amount)
    return ore_costs

print(f'{getOreCostsForFuel(1)} ORE => 1 FUEL')


# we want to plug in different input numbers until the output number equals 1,000,000,000,000
# first find an upper limit
target = 1000000000000
lower_bound = 1
upper_bound = 1
while getOreCostsForFuel(upper_bound) < target:
    upper_bound *= 10

while upper_bound > lower_bound+1:
    middle = (lower_bound + upper_bound) // 2
    middle_cost = getOreCostsForFuel(middle)
    if middle_cost == target:
        print(f'{middle_cost} ORE => {target} FUEL')
        break
    elif middle_cost <= target:
        lower_bound = middle
    else:
        upper_bound = middle

print(f'{getOreCostsForFuel(lower_bound)} ORE => {lower_bound} FUEL')
print(f'{getOreCostsForFuel(upper_bound)} ORE => {upper_bound} FUEL')
