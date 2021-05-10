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


def new_limit(g, xs, ys, part, df_bounds, grid, part_ant, n_data, init):
    df_bounds = np.array(df_bounds)
    x_int = int(part[0])
    y_int = int(part[1])
    if x_int >= xs:
        part[0] = xs - 1
        x_int = int(part[0])
    if y_int >= ys:
        part[1] = ys - 1
        y_int = (part[1])
    if grid[x_int, y_int] == 0:
        s, n = 0, 0
        bn = list()
        for i in range(len(df_bounds)):
            if int(y_int) == df_bounds[i, 2]:
                s += 1
                bn.append(df_bounds[i, :])
        if s == 0:
            if part[1] < df_bounds[0, 2]:
                part[1] = df_bounds[0, 2]
                for i in range(len(df_bounds)):
                    if df_bounds[i, 2] == int(part[1]):
                        s += 1
                        bn.append(df_bounds[i, :])
            else:
                part[1] = df_bounds[-1, 2]
                for i in range(len(df_bounds)):
                    if df_bounds[i, 2] == int(part[1]):
                        s += 1
                        bn.append(df_bounds[i, :])
        bn = np.array(bn)
        if len(bn) <= 1:
            if part[0] <= bn[0, 0]:
                part[0] = bn[0, 0]
            else:
                part[0] = bn[0, 1]
        else:
            if x_int < bn[0, 0]:
                part[0] = bn[0, 0]
            elif x_int > bn[-1, 1]:
                part[0] = bn[-1, 1]
            else:
                if init:
                    if x_int < bn[0, 0]:
                        part[0] = bn[0, 0]
                    elif x_int > bn[-1, 1]:
                        part[0] = bn[-1, 1]
                else:
                    if n_data == 1.0:
                        ant = part_ant[g, 0]
                    elif n_data == 2.0:
                        ant = part_ant[g, 2]
                    elif n_data == 3.0:
                        ant = part_ant[g, 4]
                    elif n_data == 4.0:
                        ant = part_ant[g, 6]
                    for i in range(len(bn)):
                        if ant >= bn[i, 1]:
                            part[0] = bn[i, 1]
                            break
                        else:
                            part[0] = bn[i + 1, 0]
                            break
    else:
        part = part
    return part, bn


def Z_var_mean(mu, sigma, X_test, grid):
    Z_var = np.zeros([grid.shape[0], grid.shape[1]])
    Z_mean = np.zeros([grid.shape[0], grid.shape[1]])
    for i in range(len(X_test)):
        Z_var[X_test[i][0], X_test[i][1]] = sigma[i]
        Z_mean[X_test[i][0], X_test[i][1]] = mu[i]
    Z_var[Z_var == 0] = np.nan
    Z_mean[Z_mean == 0] = np.nan
    return Z_var, Z_mean