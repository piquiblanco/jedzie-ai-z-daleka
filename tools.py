import random
import numpy as np


def rotations(card):
    all_rotations = (card,)
    for i in range(3):
        new_rotation = ()
        for track in card:
            new_track = ()
            for j in [0, 1]:
                new_track = new_track + ((track[j] + 1) % 8 + 1,)
            new_rotation = new_rotation + (tuple(sorted(new_track)),)
        all_rotations = all_rotations + (tuple(sorted(new_rotation)),)
        card = new_rotation
    return all_rotations


def get_other(card, element):
    for track in card:
        if element in track:
            if element == track[0]:
                return track[1]
            else:
                return track[0]


def split_tag(tag):
    a, b = tag[0], tag[1]
    return int(a), int(b)


def move_a_tag(tag, vector):
    a, b = tag
    if len(vector) == 2:
        c, d = vector
    else:
        if vector[0] == '-':
            c = vector[0:2]
            d = vector[2]
        else:
            c = vector[0]
            d = vector[1:3]
    new_tag = str(int(a)+int(c)) + str(int(b)+int(d))
    return new_tag


def rargmax(vector):
    m = np.amax(vector)
    valuesum = sum(vector)
    vector_array = np.array(vector)
    is_best = vector_array == m
    indices_best = np.nonzero(is_best)[0]
    count_best = len(indices_best)
    indices_all = np.arange(len(vector))
    weights = []
    for value in vector:
        if value == m:
            weights.append(0.5 / count_best + 0.5 * value / valuesum)
        else:
            weights.append(0.5 * value / valuesum)
    return random.choices(indices_all, weights=weights)[0]


def rargmax2(vector):
    m = np.amax(vector)
    vector_array = np.array(vector)
    is_best = vector_array == m
    indices_best = np.nonzero(is_best)[0]
    return random.choices(indices_best)[0]

