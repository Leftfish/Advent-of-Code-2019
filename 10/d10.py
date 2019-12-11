from math import gcd


with open('input10', mode='r') as inp10:
    arr = [list(line) for line in inp10.readlines()]


def find_astros(arr):
    row, col = len(arr[0]), len(arr)
    astr = []
    for y in range(row):
        for x in range(col):
            if arr[x][y] == '#':
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


astr = find_astros(arr)
station, visible = find_station(astr)[0], find_station(astr)[1]
print("Best station: ", station)
print("Visible from station: ", visible)

'''
def make_ratio(x):
    if x[1] == 0:
        return 0
    else:
        return x[0]/x[1]

def find_visible(astr):
    station, _, others = find_station(astr)
    h1, h2 = [], []
    print(len(others))
    for a in others:
        if (a[0] > 0 and a[1] > 0) or (a[0] > 0 and a[1]) < 0:
            h1.append(a)
        else:
            h2.append(a)
    h1.sort(key = lambda a: make_ratio(a))
    h2.sort(key = lambda a: make_ratio(a))
    print(h1)
    print(h2)
    
'''

#TODO: sorting lists of ratios, maybe rewriting to radians and arctan2?