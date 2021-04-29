import numpy as np
from Enviroment.bounds import map_bound


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


def new_limit(part, df_bounds, grid, part_ant, n_data):
    df_bounds = np.array(df_bounds)
    x_int = int(part[0])
    y_int = int(part[1])
    if x_int > grid.shape[0]:
        x_int = grid.shape[0] - 1
    if grid[x_int, y_int] == 0:
        s, n = 0, 0
        bn = list()
        for i in range(len(df_bounds)):
            if int(y_int) == df_bounds[i, 2]:
                s += 1
                bn.append(df_bounds[i])
        bn = np.array(bn)
        print(bn)
        if s == 0:
            if y_int < df_bounds[0, 2]:
                part[1] = df_bounds[0, 2]
                for i in range(len(df_bounds[2])):
                    if df_bounds[i, 2] == int(df_bounds[0, 2]):
                        s += 1
                        bn.append(df_bounds[i])
                        bn = np.array(bn)
            else:
                part[1] = df_bounds[-1, 2]
                for i in range(len(df_bounds[2])):
                    if df_bounds[i, 2] == int(df_bounds[-1, 2]):
                        s += 1
                        bn.append(df_bounds[i])
                        bn = np.array(bn)
        if len(bn) <= 1:
            if x_int < bn[0, 0]:
                part[0] = bn[0, 0]
            else:
                part[0] = bn[0, 1]
        else:
            if x_int < bn[0, 0]:
                part[0] = bn[0, 0]
            elif x_int > bn[-1, 1]:
                part[0] = bn[-1, 1]
            else:
                if n_data == 1.0:
                    ant = part_ant[0]
                elif n_data == 2.0:
                    ant = part_ant[2]
                elif n_data == 3.0:
                    ant = part_ant[4]
                elif n_data == 4.0:
                    ant = part_ant[6]
                for i in range(len(bn)):
                    if bn[i, 0] < ant < bn[i, 1]:
                        if abs(ant - bn[i, 0]) > abs(ant - bn[i, 1]):
                            part[0] = bn[i, 1]
                        else:
                            part[0] = bn[i, 0]
                    elif x_int < bn[i, 0]:
                        if abs(part[0] - bn[i, 0]) > abs(part[0] - bn[i - 1, 1]):
                            part[0] = bn[i - 1, 1]
                        else:
                            part[0] = bn[i, 0]
    return part


def Z_var_mean(mu, sigma, X_test, grid):
    Z_var = np.zeros([grid.shape[0], grid.shape[1]])
    Z_mean = np.zeros([grid.shape[0], grid.shape[1]])
    for i in range(len(X_test)):
        Z_var[X_test[i][0], X_test[i][1]] = sigma[i]
        Z_mean[X_test[i][0], X_test[i][1]] = mu[i]
    Z_var[Z_var == 0] = np.nan
    Z_mean[Z_mean == 0] = np.nan
    return Z_var, Z_mean