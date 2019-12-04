print("Day 3 of Advent of Code!")

from collections import OrderedDict

def parse_dir(d):
    d_x, d_y = 0, 0
    if d[0] == 'R':
        d_x = int(d[1:])
    elif d[0] == 'L':
        d_x = -int(d[1:])
    elif d[0] == 'U':
        d_y = int(d[1:])
    elif d[0] == 'D':
        d_y = -int(d[1:])
    return d_x, d_y

def move(d, visited):
    d_x, d_y = parse_dir(d)
    last = visited.popitem()
    steps = last[1]
    x, y = last[0][0], last[0][1]
    if d_x != 0:
        for _ in range(abs(d_x)):
            if d_x > 0: x += 1
            else: x -= 1
            steps += 1
            visited[(x, y)] = steps
    elif d_y != 0:
        for _ in range(abs(d_y)):
            if d_y > 0: y += 1
            else: y -= 1
            steps += 1
            visited[(x, y)] = steps

def execute_dirs(dirs):
    visited = OrderedDict({(0, 0): 0})
    for d in dirs:
        move(d, visited)
    return visited

def manhattan(p,q):
        return abs(p[0]-q[0])+abs(p[1]-q[1])

def find_intersects(w1, w2):
    first = execute_dirs(w1)
    second = execute_dirs(w2)
    intersections = set(first.keys()) & set(second.keys())
    lowest_distance = sorted([manhattan((0,0), isct) for isct in intersections])[0]
    
    steps_first = {mv: first[mv] for mv in first.keys() & intersections}
    steps_second = {mv: second[mv] for mv in second.keys() & intersections}
    least_steps = sorted([steps_first[d] + steps_second[d] for d in steps_first.keys()])[0]
    
    return lowest_distance,  least_steps

with open("input03", mode = 'r') as inp3:
    data = inp3.read()
    wires = data.split('\n')
    w1 = wires[0].split(',')
    w2 = wires[1].split(',')

lowest_distance, least_steps = find_intersects(w1, w2)
print("Closest intersection: ", lowest_distance)
print("Least steps:", least_steps)