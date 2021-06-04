import numpy as np


def data(x_p, y_p, y_data):
    x_a = np.array(x_p).reshape(-1, 1)
    y_a = np.array(y_p).reshape(-1, 1)
    x_train = np.concatenate([x_a, y_a], axis=1).reshape(-1, 2)
    y_train = np.array(y_data).reshape(-1, 1)

    return x_a, y_a, x_train, y_train


def gp_regression(n_data, x_p, y_p, y_data, X_test, gpr, post_array):

    x_a, y_a, x_train, y_train = data(x_p, y_p, y_data)
    gpr.fit(x_train, y_train)
    gpr.get_params()

    mu, sigma = gpr.predict(X_test, return_std=True)
    post_ls = np.min(np.exp(gpr.kernel_.theta[0]))
    post_array[n_data - 1] = post_ls

    return sigma, mu, x_a, y_a, post_array


def gpr_value(g, x_bench, y_bench, X_test, sigma, mu, sigma_data, mu_data):
    for i in range(len(X_test)):
        di = X_test[i]
        dix = di[0]
        diy = di[1]
        if dix == x_bench and diy == y_bench:
            mu_data.append(mu[i])
            sigma_data.append(sigma[i])

    return sigma_data, mu_data
