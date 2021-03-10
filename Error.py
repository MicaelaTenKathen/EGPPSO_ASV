import numpy as np

def mse(y_data, mu_data, samples):
    total_suma = 0
    y_array = np.array(y_data)
    mu_array = np.array(mu_data)
    for i in range(len(mu_array)):
        total_suma = (float(y_array[i]) - float(mu_array[i])) ** 2 + total_suma
    MSE1 = total_suma / samples
    return MSE1