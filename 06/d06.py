print("Day 6 of Advent of Code!")

try:
    with open("input06", mode='r') as inp6:
        orbits = [(body.split(')')[0], body.split(')')[1].rstrip()) for body in inp6.readlines()]
except:
    print("File not found")

orbit_tree = {}
for o in orbits:
    orbit_tree[o[1]] = o[0]

orbiters = orbit_tree.keys()
sum_orbits = 0

for child in orbiters:
    ancestor = orbit_tree.get(child, None)
    while ancestor:
        sum_orbits += 1
        ancestor = orbit_tree.get(ancestor, None)

print("Total orbits:", sum_orbits)

santa_anc, you_anc = {}, {}


def get_ancestors(child, tree):
    ancestors = {}
    for node in tree:
        if node == child:
            hops = 0
            anc = orbit_tree.get(node, None)
            while anc:
                hops += 1
                ancestors[anc] = hops
                anc = orbit_tree.get(anc, None)
    return ancestors

santa_anc = get_ancestors('SAN', orbiters)
you_anc = get_ancestors('YOU', orbiters)
merged_path = {**you_anc, **santa_anc}

for k, v in merged_path.items():
    if k in you_anc and k in santa_anc:
        merged_path[k] = [v, you_anc[k]]

min_hops = sorted([sum(v) for v in merged_path.values() if isinstance(v, list)])[0] - 2
print("Required orbital hops:", min_hops)
