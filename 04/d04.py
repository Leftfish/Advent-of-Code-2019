print("Day 4 of Advent of Code!")

from collections import Counter

lower = 248345
upper = 746315
test_digs = range(lower, upper + 1)

def is_valid(d):
    d = str(d)
    adj = False
    for i in range(len(d) - 1):
        d1, d2 = int(d[i]), int(d[i+1])
        if d1 > d2:
            return False, adj
        if d1 == d2:
            adj = True
    return True, adj

def is_valid_proper(d):
    d = str(d)
    inc, adj = True, False
    c = Counter(d)
    ok = {}
    for i in range(len(d) - 1):
        d1, d2 = int(d[i]), int(d[i+1])
        if d1 > d2:
            inc = False
            return inc, adj
        if d1 == d2:
            ok[str(d1)] = c[str(d1)]
            if 2 in ok.values():
                adj = True
    return inc, adj

valid = [t for t in test_digs if all(is_valid(t))]
print("Number of valid according to first set of criteria:", len(valid))
proper_valid = [t for t in test_digs if all(is_valid_proper(t))]
print("Number of valid according to second set of criteria:", len(proper_valid))