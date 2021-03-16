import numpy as np


def limit(part, grid_min, grid_max):
    if part[0] <= grid_min:
        part[0] = grid_min
    if part[0] >= grid_max:
        part[0] = grid_max - 1
    if part[1] <= grid_min:
        part[1] = grid_min
    if part[1] >= grid_max:
        part[1] = grid_max - 1
    return part


def arrays(x_p, y_p, x_g, y_g):
    x_a = np.array(x_p).reshape(-1, 1)
    y_a = np.array(y_p).reshape(-1, 1)
    x_ga = np.array(x_g).reshape(-1, 1)
    y_ga = np.array(y_g).reshape(-1, 1)
    return x_a, y_a, x_ga, y_ga
