import numpy as np


def sigmamax(X_test, sigma, mu):
    sigma_max = np.max(sigma)
    index_sigma = np.where(sigma == sigma_max)
    index_x1 = index_sigma[0]
    index_x2 = index_x1[0]
    index_x = int(X_test[index_x2][0])
    index_y = int(X_test[index_x2][1])

    ml = mu
    n = 0
    index_xmu, index_ymu = list(), list()
    while n < 10:
        mu_max = np.max(ml)
        index_mu = np.where(mu == mu_max)
        index_x1mu = index_mu[0]
        index_x2mu = index_x1mu[0]
        index_xmu.append(int(X_test[index_x2mu][0]))
        index_ymu.append(int(X_test[index_x2mu][1]))
        ml = np.delete(ml, ([index_x1mu, index_x2mu]))
        n += 1

    best_1 = [index_x, index_y]
    gp_best = np.array(best_1)

    mu_b = zip(index_xmu, index_xmu)
    best_2 = mu_b[0]
    mu_best = np.array(best_2)

    return gp_best, mu_best
