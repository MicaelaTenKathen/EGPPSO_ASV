"""
Benchmark functions map #todo ver nombre, preguntar
author: Federico Peralta
"""

from sys import path

import numpy as np
from deap import benchmarks
from skopt.benchmarks import branin as brn


w_obstacles = False

a = []
c = []


def bohachevsky_arg0(sol):
    return np.nan if w_obstacles and sol[2] == 1 else benchmarks.bohachevsky(sol[:2])[0]


def ackley_arg0(sol):
    return np.nan if w_obstacles and sol[2] == 1 else benchmarks.ackley(sol[:2])[0]


def rosenbrock_arg0(sol):
    return np.nan if w_obstacles and sol[2] == 1 else benchmarks.rosenbrock(sol[:2])[0]


def himmelblau_arg0(sol):
    return np.nan if w_obstacles and sol[2] == 1 else benchmarks.himmelblau(sol[:2])[0]


def branin(sol):
    return np.nan if w_obstacles and sol[2] == 1 else brn(sol[:2])


def shekel_arg0(sol):
    return np.nan if w_obstacles and sol[2] == 1 else benchmarks.shekel(sol[:2], a, c)[0]


def schwefel_arg0(sol):
    return np.nan if w_obstacles and sol[2] == 1 else benchmarks.schwefel(sol[:2])[0]


def create_map(grid, resolution, obstacles_on=False, randomize_shekel=False, sensor="", no_maxima=10,
               load_from_db=False, file=0):
    if load_from_db:
        if sensor == "s1":
            file = 0
        elif sensor == "s2":
            file = 1
        elif sensor == "s3":
            file = 2
        elif sensor == "s4":
            file = 3
        elif sensor == "s5":
            file = 4
        elif sensor == "s6":
            file = 5
        elif sensor == "s7":
            file = 6
        elif sensor == "s8":
            file = 7
        with open(path[-1] + '/Data/shww.npy'.format(file), 'rb') as g:
            return np.load(g)
    else:
        global w_obstacles, a, c
        w_obstacles = obstacles_on
        xmin = -1.5
        xmax = 1.5
        ymin = 0
        ymax = 3

        if randomize_shekel:
            no_maxima = np.random.randint(3, 6)
            xmin = 0
            xmax = 10
            ymin = 0
            ymax = 10
            a = []
            c = []
            for i in range(no_maxima):
                a.append([1.2 + np.random.rand() * 8.8, 1.2 + np.random.rand() * 8.8])
                c.append(5)
            a = np.array(a)
            c = np.array(c).T
        else:
            a = np.array([[0.16, 1 / 1.5], [0.9, 0.2 / 1.5]])
            c = np.array([0.15, 0.15]).T

        xadd = 0
        yadd = 0

        _x = np.arange(xmin, xmax, resolution * (xmax - xmin) / (grid.shape[1])) + xadd
        _y = np.arange(xmin, xmax, resolution * (ymax - ymin) / (grid.shape[0])) + yadd
        _x, _y = np.meshgrid(_x, _y)

        _z = np.fromiter(map(shekel_arg0, zip(_x.flat, _y.flat, grid.flat)), dtype=np.float,
                         count=_x.shape[0] * _x.shape[1]).reshape(_x.shape)

        meanz = np.nanmean(_z)
        stdz = np.nanstd(_z)
        _z = (_z - meanz) / stdz

        with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
                  'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/shww.npy', 'wb') as g:
            np.save(g, _z)
        return _z


def get_init_pos4(n=1, rotate_rnd=True, expand=False, map_data=None):
    step = np.pi * 2 / n
    if rotate_rnd:
        extra_angle = np.random.rand() * np.pi * 2
    else:
        extra_angle = 0
    angles = [step * i + extra_angle for i in range(n)]
    initial_positions = np.full((n, 3), [500.0, 750.0, 0.0])

    cosine = np.cos(angles)
    sine = np.sin(angles)
    if expand:
        initial_positions[:, 0] += 220 * cosine
        initial_positions[:, 1] += 220 * sine
        for i in range(len(initial_positions[:, 0])):
            while True:
                initial_positions[i, 0] += cosine[i]
                initial_positions[i, 1] += sine[i]
                if map_data[np.round(initial_positions[i, 1]).astype(np.int), np.round(initial_positions[i, 0]).astype(
                        np.int)] == 1:
                    initial_positions[i, 0] -= cosine[i]
                    initial_positions[i, 1] -= sine[i]
                    break
    else:
        initial_positions[:, 0] += 10 * cosine
        initial_positions[:, 1] += 10 * sine
    return np.round(initial_positions).astype(np.int)


# grid, resolution = black_white(1, 1000, 1500)
# _z = create_map(grid, resolution, obstacles_on=False, randomize_shekel=False, sensor="", no_maxima=10,
#                load_from_db=True, file=0)
# _z = bench_plot(_z, grid)
# plt.figure(2)
# im4 = plt.imshow(_z, interpolation='bilinear', origin='lower', cmap="jet")
# plt.colorbar(im4, format='%.2f', shrink=1)
# plt.xlabel("x [m]")
# plt.ylabel("y [m]")
# plt.ylim([1500, 0])
# plt.grid(True)
# plt.show()