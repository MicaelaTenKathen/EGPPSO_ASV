import math
import numpy as np


def distance(n_data, part, part_ant, distances, init=True):
    part_dist = np.zeros(8)
    if init:
        if n_data == 1.0:
            part_ant[0] = part[0]
            part_ant[1] = part[1]
        if n_data == 2.0:
            part_ant[2] = part[0]
            part_ant[3] = part[1]
        if n_data == 3.0:
            part_ant[4] = part[0]
            part_ant[5] = part[1]
        if n_data == 4.0:
            part_ant[6] = part[0]
            part_ant[7] = part[1]
    else:
        if n_data == 1.0:
            part_dist[0] = part[0]
            part_dist[1] = part[1]
            distances[0] = math.sqrt((part_dist[0] - part_ant[0]) ** 2 + (part_dist[1] - part_ant[1]) ** 2) + distances[
                0]
            part_ant[0] = part[0]
            part_ant[1] = part[1]
        elif n_data == 2.0:
            part_dist[2] = part[0]
            part_dist[3] = part[1]
            distances[1] = math.sqrt((part_dist[2] - part_ant[2]) ** 2 + (part_dist[3] - part_ant[3]) ** 2) + distances[
                1]
            part_ant[2] = part[0]
            part_ant[3] = part[1]
        elif n_data == 3.0:
            part_dist[4] = part[0]
            part_dist[5] = part[1]
            distances[2] = math.sqrt((part_dist[4] - part_ant[4]) ** 2 + (part_dist[5] - part_ant[5]) ** 2) + distances[
                2]
            part_ant[4] = part[0]
            part_ant[5] = part[1]
        elif n_data == 4.0:
            part_dist[6] = part[0]
            part_dist[7] = part[1]
            distances[3] = math.sqrt((part_dist[6] - part_ant[6]) ** 2 + (part_dist[7] - part_ant[7]) ** 2) + distances[
                3]
            part_ant[6] = part[0]
            part_ant[7] = part[1]
    return part_ant, distances
