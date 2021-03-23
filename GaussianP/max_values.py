import numpy as np


def sigmamax(X_test, sigma):
    sigma_max = np.max(sigma)
    print(sigma_max)
    index_sigma = np.where(sigma == sigma_max)
    index_x1 = index_sigma[0]
    index_x2 = index_x1[0]
    index_x = int(X_test[index_x2][0])
    index_y = int(X_test[index_x2][1])
    return sigma_max, index_x, index_y


def mumax(X_test, mu):
    mu_max = np.max(mu)
    print(mu_max)
    index_mu = np.where(mu == mu_max)
    index_x1mu = index_mu[0]
    index_x2mu = index_x1mu[0]
    index_xmu = int(X_test[index_x2mu][0])
    index_ymu = int(X_test[index_x2mu][1])
    return mu_max, index_xmu, index_ymu
