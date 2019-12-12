import re
from math import gcd
from itertools import combinations_with_replacement
from functools import reduce


class Planet():
    def __init__(self, x, y, z, name):
        self.x = x
        self.y = y
        self.z = z

        self.dx = 0
        self.dy = 0
        self.dz = 0

        self.name = name

    def __str__(self):
        s = "{}: pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>"
        return s.format(self.name, self.x, self.y, self.z,
                        self.dx, self.dy, self.dz)

    def apply_velocity(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

    def apply_gravity_to_axis(self, axis, delta):
        if axis == 0:
            self.dx += delta
        elif axis == 1:
            self.dy += delta
        elif axis == 2:
            self.dz += delta

    def calculate_energy(self):
        potential = sum((abs(self.x), abs(self.y), abs(self.z)))
        kinetic = sum((abs(self.dx), abs(self.dy), abs(self.dz)))
        energy = potential * kinetic
        return energy


def apply_gravity(moon1, moon2):
    axes = (moon1.x, moon1.y, moon1.z)
    other_axes = (moon2.x, moon2.y, moon2.z)

    for o in list(enumerate(zip(axes, other_axes))):
        if o[1][0] > o[1][1]:
            moon1.apply_gravity_to_axis(o[0], -1)
            moon2.apply_gravity_to_axis(o[0], 1)
        elif o[1][0] < o[1][1]:
            moon1.apply_gravity_to_axis(o[0], 1)
            moon2.apply_gravity_to_axis(o[0], -1)


def get_universe_state(moons, axis):
    if axis == 0:  # X
        return tuple([(m.x, m.dx) for m in moons])
    elif axis == 1:  # Y
        return tuple([(m.y, m.dy) for m in moons])
    elif axis == 2:  # Z
        return tuple([(m.z, m.dz) for m in moons])


def lcm(a, b):
    return a * b // gcd(a, b)


def lcmm(*args):
    return reduce(lcm, args)


def run_sim(moons, runs):
    for _ in range(runs):
        for m in combinations_with_replacement(moons, 2):
            if m[0] != m[1]:
                apply_gravity(m[0], m[1])
        for m in moons:
            m.apply_velocity()
    energy = sum([m.calculate_energy() for m in moons])
    return energy


def run_dry(moons):
    xs = set()
    ys = set()
    zs = set()
    cx, cy, cz = None, None, None
    counter = 1
    while True:
        xs.add(get_universe_state(moons, 0))
        ys.add(get_universe_state(moons, 1))
        zs.add(get_universe_state(moons, 2))
        for m in combinations_with_replacement(moons, 2):
            if m[0] != m[1]:
                apply_gravity(m[0], m[1])
        for m in moons:
            m.apply_velocity()
        if counter >= 2:
            state_x = get_universe_state(moons, 0)
            state_y = get_universe_state(moons, 1)
            state_z = get_universe_state(moons, 2)
            if not cx and state_x in xs:
                cx = counter
                print("Xs", cx)
            if not cy and state_y in ys:
                cy = counter
                print("Ys", cy)
            if not cz and state_z in zs:
                cz = counter
                print("Zs", cz)
        if all([cx, cy, cz]) and counter > 5:
            return cx, cy, cz
        counter += 1

inp = '''<x=-2, y=9, z=-5>
<x=16, y=19, z=9>
<x=0, y=3, z=6>
<x=11, y=0, z=11>'''

data = [re.findall(r'-?\d+', l) for l in inp.splitlines()]
for d in data:
    for i in range(len(d)):
        d[i] = int(d[i])

io = Planet(data[0][0], data[0][1], data[0][2], "io")
europa = Planet(data[1][0], data[1][1], data[1][2], "eu")
ganymede = Planet(data[2][0], data[2][1], data[2][2], "gn")
callisto = Planet(data[3][0], data[3][1], data[3][2], "cl")

runs = 1000
moons = (io, europa, ganymede, callisto)
print("Energy after {} cycles: {}".format(runs, run_sim(moons, runs)))

x, y, z = run_dry(moons)

print("First recurrence: ", lcmm(x, y, z))
