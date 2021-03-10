import numpy as np
from sklearn.gaussian_process.kernels import RBF

def initGP(leng_scale, sigma_kernel, grid_min, grid_max, simple_equation='True'):
    if simple_equation == True:
        ker = RBF(length_scale=leng_scale)
    else:
        ker = sigma_kernel * RBF(length_scale=leng_scale)

    j = 0
    i = 0

    x_grid = []
    y_grid = []

    x = abs(grid_min) + abs(grid_max)
    y = abs(grid_min) + abs(grid_max)

    while i < x:
        j = 0
        while j < y:
            x_grid.append(j - abs(grid_min))
            y_grid.append(i - abs(grid_min))
            j = j + 1
        i += 1

    X_grid = np.array(x_grid).reshape(-1, 1)
    Y_grid = np.array(y_grid).reshape(-1, 1)

    X_test = np.concatenate([X_grid, Y_grid], axis=1).reshape(-1, 2)

    res = ker(X_test)

    return x, y, X_test, ker, res

def gaussian_regression(x, y, X_test, gpr, x_train, y_train):
    gpr.fit(x_train, y_train)
    gpr.get_params()

    mu, sigma = gpr.predict(X_test, return_std=True)

    Z_var = sigma.reshape(x, y)
    Z_mean = mu.reshape(x, y)

    return sigma, mu, Z_var, Z_mean