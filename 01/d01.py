print("Day 1 of Advent of Code!")

from math import floor

calculate_fuel = lambda x: floor(x / 3) - 2

def calculate_proper_fuel(x):
    result = calculate_fuel(x)
    fuel = result
    while fuel > 0:
        additional = calculate_fuel(fuel)
        if additional > 0: result += additional
        fuel = additional
    return result

with open("input01", mode = 'r') as inp1:
    modules = [int(line.rstrip()) for line in inp1]

fuel = sum(calculate_fuel(m) for m in modules)
proper_fuel = sum(calculate_proper_fuel(m) for m in modules)

print("Fuel needed: {}".format(fuel))
print("Fuel including fuel for fuel needed: {}".format(proper_fuel))