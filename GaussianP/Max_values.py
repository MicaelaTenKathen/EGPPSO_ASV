import numpy as np


def sigmamax(grid_min, Z_var):
    sigma_max = np.max(Z_var)
    print(sigma_max)
    index_sigma = np.where(Z_var == sigma_max)
    # print(index_sigma)
    index_x1 = index_sigma[1] - abs(grid_min)
    index_x2 = index_x1[0]
    index_y1 = index_sigma[0] - abs(grid_min)
    index_y2 = index_y1[0]
    index_x = float(index_x2)
    index_y = float(index_y2)
    return sigma_max, index_x, index_y


def mumax(grid_min, Z_mean):
    mu_max = np.max(Z_mean)
    print(mu_max)
    index_mu = np.where(Z_mean == mu_max)
    # print(index_sigma)
    index_x11 = index_mu[1] - abs(grid_min)
    index_x21 = index_x11[0]
    index_y11 = index_mu[0] - abs(grid_min)
    index_y21 = index_y11[0]
    index_xmu = float(index_x21)
    index_ymu = float(index_y21)
    return mu_max, index_xmu, index_ymu
