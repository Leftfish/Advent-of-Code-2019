import numpy as np


print("Day 6 of Advent of Code!")


def make_layers(picture, w, h):
    layers = []
    l = w * h
    ptr = 0
    while ptr < len(picture):
        new_layer = picture[ptr:ptr+l]
        layers.append(new_layer)
        ptr += l
    return layers


def calculate_answer(picture, w, h):
    layers = make_layers(picture, w, h)
    zeros = {}
    for l in layers:
        zeros[l] = l.count('0')
    best = min(zeros.items(), key=lambda x: x[1])[0]
    return best.count('1') * best.count('2')


def decode_image(img, w, h):
    img_lrs = []
    decoded = [[None for i in range(h)] for j in range(w)]
    for l in make_layers(img, w, h):
        new = np.array(list(map(lambda x: int(x), l)))
        new = np.reshape(new, (w, h))
        img_lrs.append(new)

    for i in range(w):
        for j in range(h):
            for l in img_lrs:
                if l[i][j] in (0, 1) and decoded[i][j] is None:
                    decoded[i][j] = l[i][j]

    decoded = np.array([a for b in decoded for a in b])
    return np.reshape(decoded, (h, w))


def print_img(img):
    for row in img:
        to_print = list(row)
        for i in range(len(to_print)):
            cur = to_print[i]
            to_print[i] = '#' if cur == 1 else ' '
        print(''.join(to_print))


try:
    with open("input08", mode='r') as inp8:
        prod = inp8.read().rstrip()
except:
    print("File not found")

w, h = 25, 6

print("2s times 1s:", calculate_answer(prod, w, h))
img = decode_image(prod, w, h)
print("Message:")
print_img(img)
