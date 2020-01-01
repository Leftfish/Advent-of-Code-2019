from math import gcd

with open('input10', mode='r') as inp10:
    arr = [list(line) for line in inp10.readlines()]


def find_astros(arr):
    row, col = len(arr[0]), len(arr)
    astr = []
    for y in range(row):
        for x in range(col):
            if arr[x][y] in '#':
                astr.append((x, y))
    return astr


def check_dirs(astr, a):
    dirs = set()
    x, y = a[0], a[1]
    for oth in astr:
        rel_x = oth[0] - x
        rel_y = oth[1] - y
        dvsr = gcd(rel_x, rel_y)
        if dvsr == 0:
            continue
        path = (rel_x // dvsr, rel_y // dvsr)
        dirs.add(path)
    return len(dirs), dirs


def find_station(astr):
    best = 0
    station = None
    others = None
    for a in astr:
        results = check_dirs(astr, a)[0]
        if results > best:
            best = results
            station = a
            others = check_dirs(astr, a)[1]
    return station, best, others


def get_rel(a, station):
    rel_x = station[0] - a[0]
    rel_y = station[1] - a[1]
    if (rel_x >= 0 and rel_y > 0):
        default = 1e8
    else:
        default = -1e8
    ratio = rel_y/rel_x if rel_x != 0 else default
    return rel_y, rel_x, ratio


def find_nearest(others, station, astromap):
    x, y = station
    visible = []
    for o in others:
        cx, cy = x + o[0], y + o[1]
        try:
            while astromap[cx][cy] != '#':
                cx += o[0]
                cy += o[1]
            visible.append((cx, cy))
        except:
            continue
    return visible


def find_visible(astr, others, station, arr):
    visible = find_nearest(others, station, arr)
    q1, q2, q3, q4 = [], [], [], []
    for a in visible:
        rel_y, rel_x, _ = get_rel(a, station)
        if (rel_x >= 0 and rel_y <= 0):
            q1.append(a)
        elif (rel_x < 0 and rel_y <= 0):
            q2.append(a)
        elif (rel_x < 0 and rel_y > 0):
            q3.append(a)
        else:
            q4.append(a)
    q1.sort(key=lambda a: get_rel(a, station)[2], reverse=True)
    q2.sort(key=lambda a: get_rel(a, station)[2], reverse=True)
    q3.sort(key=lambda a: get_rel(a, station)[2], reverse=True)
    q4.sort(key=lambda a: get_rel(a, station)[2], reverse=True)
    return q1, q2, q3, q4


def vape_asteroids(astr, others, station, arr):
    i = 0
    while len(astr) > 1:
        q1, q2, q3, q4 = find_visible(astr, others, station, arr)
        all_asteroids = q1 + q2 + q3 + q4
        for a in all_asteroids:
            x, y = a[0], a[1]
            arr[x][y] = '.'
            i += 1
            if i == 200:
                return "200th vaped asteroid: {}, {}".format(y, x)
        astr = find_astros(arr)
    return "Less than 200 asteroids vaped"

astr = find_astros(arr)
station, visible, others = find_station(astr)
print("Best station: ", station)
print("Visible from station: ", visible)
print(vape_asteroids(astr, others, station, arr))
