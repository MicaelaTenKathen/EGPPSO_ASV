import numpy as np


def mse(g, y_data, mu_data, samples, MSE_data, it):
    total_suma = 0
    y_array = np.array(y_data)
    mu_array = np.array(mu_data)
    for i in range(len(mu_array)):
        total_suma = (float(y_array[i]) - float(mu_array[i])) ** 2 + total_suma
    MSE = total_suma / samples
    MSE_data.append(MSE)
    it.append(g)
    return MSE_data, it
