print("Day 3 of Advent of Code!")

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

def move(d, visited, extended_visited):
    d_x, d_y = parse_dir(d)
    cur = visited[-1]
    steps = extended_visited[-1][1]
    x, y = cur[0], cur[1]
    if d_x != 0:
        for _ in range(abs(d_x)):
            if d_x > 0: x += 1
            else: x -= 1
            steps += 1
            visited.append((x,y))
            extended_visited.append(((x, y), steps))
    elif d_y != 0:
        for _ in range(abs(d_y)):
            if d_y > 0: y += 1
            else: y -= 1
            steps += 1
            visited.append((x,y))
            extended_visited.append(((x, y), steps))

def manhattan(p,q):
        return abs(p[0]-q[0])+abs(p[1]-q[1])

def execute_dirs(dirs):
    start = (0, 0)
    visited = [start]
    extended_visited = [[start, 0]]
    for d in dirs:
        move(d, visited, extended_visited)
    return visited, extended_visited

def find_intersects(w1, w2):
    first = execute_dirs(w1)
    second = execute_dirs(w2)
    intersections = set(first[0][1:]) & set(second[0][1:])
    lowest_distance = sorted([manhattan((0,0), isct) for isct in intersections])[0]
    
    steps1 = {mv1[0]: mv1[1] for mv1 in first[1][1:] for isct in intersections if isct == mv1[0]}
    steps2 = {mv2[0]: mv2[1] for mv2 in second[1][1:] for isct in intersections if isct == mv2[0]}
    total_steps = [steps1[d] + steps2[d] for d in steps1.keys()]
    least_steps = sorted(total_steps)[0]
    return intersections, lowest_distance, least_steps

with open("input03", mode = 'r') as inp3:
    data = inp3.read()
    wires = data.split('\n')
    w1 = wires[0].split(',')
    w2 = wires[1].split(',')

_, lowest_distance, least_steps = find_intersects(w1, w2)

print("Closest intersection: ", lowest_distance)
print("Least steps:", least_steps)