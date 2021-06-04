import math


def distance(g, GEN, n_data, part, part_ant, distances, init=False):

    if init:
        if n_data == 1:
            part_ant[0, 0] = part[0]
            part_ant[0, 1] = part[1]
        if n_data == 2:
            part_ant[0, 2] = part[0]
            part_ant[0, 3] = part[1]
        if n_data == 3:
            part_ant[0, 4] = part[0]
            part_ant[0, 5] = part[1]
        if n_data == 4:
            part_ant[0, 6] = part[0]
            part_ant[0, 7] = part[1]
    else:
        if n_data == 1:
            part_ant[g + 1, 0] = part[0]
            part_ant[g + 1, 1] = part[1]
            distances[0] = math.sqrt((part_ant[g + 1, 0] - part_ant[g, 0]) ** 2 + (part_ant[g + 1, 1] - part_ant[g, 1])
                                     ** 2) + distances[0]
        elif n_data == 2:
            part_ant[g + 1, 2] = part[0]
            part_ant[g + 1, 3] = part[1]
            distances[1] = math.sqrt((part_ant[g + 1, 2] - part_ant[g, 2]) ** 2 + (part_ant[g + 1, 3] - part_ant[g, 3])
                                     ** 2) + distances[1]
        elif n_data == 3:
            part_ant[g + 1, 4] = part[0]
            part_ant[g + 1, 5] = part[1]
            distances[2] = math.sqrt((part_ant[g + 1, 4] - part_ant[g, 4]) ** 2 + (part_ant[g + 1, 5] - part_ant[g, 5])
                                     ** 2) + distances[2]
        elif n_data == 4:
            part_ant[g + 1, 6] = part[0]
            part_ant[g + 1, 7] = part[1]
            distances[3] = math.sqrt((part_ant[g + 1, 6] - part_ant[g, 6]) ** 2 + (part_ant[g + 1, 7] - part_ant[g, 7])
                                     ** 2) + distances[3]

    return part_ant, distances