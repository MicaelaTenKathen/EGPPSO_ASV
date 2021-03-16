import numpy as np
from sklearn.gaussian_process.kernels import RBF


def initGP(grid, leng_scale, sigma_kernel, grid_min, grid_max_x, grid_max_y, simple_equation=True):
    if simple_equation:
        ker = RBF(length_scale=leng_scale)
    else:
        ker = sigma_kernel * RBF(length_scale=leng_scale)

    j = 0

    x_grid = []
    y_grid = []
    i_data = []
    j_data = []

    x = abs(grid_min) + abs(grid_max_x)
    y = abs(grid_min) + abs(grid_max_y)

    while j < y:
        i = 0
        while i < x:
            x_grid.append(i - abs(grid_min))
            y_grid.append(j - abs(grid_min))
            # if grid[i, j] != 0:
            #     x_grid.append(i - abs(grid_min))
            #     y_grid.append(j - abs(grid_min))
            #     i_data.append(i)
            #     j_data.append(j)
            i += 1
        j += 1

    X_grid = np.array(x_grid).reshape(-1, 1)
    Y_grid = np.array(y_grid).reshape(-1, 1)

    X_test = np.concatenate([X_grid, Y_grid], axis=1).reshape(-1, 2)

    return x, y, i_data, j_data, X_test, ker


def data(x_p, y_p, y_data):
    x_a = np.array(x_p).reshape(-1, 1)
    y_a = np.array(y_p).reshape(-1, 1)
    x_train = np.concatenate([x_a, y_a], axis=1).reshape(-1, 2)
    y_train = np.array(y_data).reshape(-1, 1)

    return x_a, y_a, x_train, y_train


def gaussian_regression(x, y, x_p, y_p, y_data, X_test, gpr):
    x_a, y_a, x_train, y_train = data(x_p, y_p, y_data)

    gpr.fit(x_train, y_train)
    gpr.get_params()

    mu, sigma = gpr.predict(X_test, return_std=True)

    Z_var = sigma.reshape(x, y)
    Z_mean = mu.reshape(x, y)

    return sigma, mu, Z_var, Z_mean, x_a, y_a


def gpr_value(x_bench, y_bench, grid_min, Z_mean, Z_var, sigma_data, mu_data):
    mu_value = Z_mean[x_bench + abs(grid_min), y_bench + abs(grid_min)]
    sigma_value = Z_var[x_bench + abs(grid_min), y_bench + abs(grid_min)]
    sigma_data.append(sigma_value)
    mu_data.append(mu_value)
    return sigma_data, mu_data
