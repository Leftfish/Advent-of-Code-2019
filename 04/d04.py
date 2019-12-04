print("Day 4 of Advent of Code!")

from collections import Counter

def is_valid(d):
    d = str(d)
    return sorted(d) == list(d) and len(set(d)) != len(d)
    
def is_valid_proper(d):
    d = str(d)
    return sorted(d) == list(d) and 2 in Counter(d).values()

lower = 248345
upper = 746315
test_digs = range(lower, upper + 1)

valid = [t for t in test_digs if is_valid(t)]
print("Number of valid according to first set of criteria:", len(valid))
proper_valid = [t for t in test_digs if is_valid_proper(t)]
print("Number of valid according to second set of criteria:", len(proper_valid))