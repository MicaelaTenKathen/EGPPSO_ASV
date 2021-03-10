import numpy as np

def data(x_p, y_p, y_data):
    x_a = np.array(x_p).reshape(-1, 1)
    y_a = np.array(y_p).reshape(-1, 1)
    x_train = np.concatenate([x_a, y_a], axis=1).reshape(-1, 2)
    y_train = np.array(y_data).reshape(-1, 1)

    return x_a, y_a, x_train, y_train

def sigmamax(grid_min, Z_var):
    sigma_max = np.max(Z_var)
    print(sigma_max)
    index_sigma = np.where(Z_var == sigma_max)
    #print(index_sigma)
    index_x1 = index_sigma[1] - abs(grid_min)
    index_x2 = index_x1[0]
    index_y1 = index_sigma[0] - abs(grid_min)
    index_y2 = index_y1[0]
    index_x = float(index_x2)
    index_y = float(index_y2)
    return sigma_max, index_x, index_y

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