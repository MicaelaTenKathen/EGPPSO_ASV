from Enviroment import black_white
import pandas as pd
import numpy as np
from Bench import create_map
import matplotlib.pyplot as plt


def map_bound():
    grid, resolution = black_white(1, 1000, 1500)
    available, first, last = list(), list(), list()
    bound = True
    confirm = list()
    index, first_x, last_x, all_y = list(), list(), list(), list()
    new_grid = pd.DataFrame(data=grid)

    for j in range(len(grid[1])):
        for i in range(len(grid)):
            if grid[i, j] == 1:
                if bound:
                    first.append([i, j])
                    bound = False
                available.append([i, j])
            else:
                if not bound:
                    last.append([i, j])
                    bound = True

    for i in range(len(first)):
        if first[i][1] == last[i][1]:
            confirm.append(True)

    if np.array(confirm).all():
        for i in range(len(first)):
            first_x.append(first[i][0])
            last_x.append(last[i][0])
            all_y.append(first[i][1])
            index.append(first[i][1])
        bounds = {'First X': first_x, 'Last X': last_x, 'Y': all_y}
        df_bounds = pd.DataFrame(data=bounds, index=index)
    else:
        print('An error occurred. Map bound, y array')

    return df_bounds, new_grid


df, new_grid = map_bound()
new_grid = new_grid.replace(0, np.nan)
new_grid = pd.DataFrame.to_numpy(new_grid)

_z = create_map(new_grid, 1, obstacles_on=False, randomize_shekel=False, sensor="", no_maxima=10,
                 load_from_db=False, file=0)


_z2 = np.transpose(new_grid)
minz = np.min(_z)

im4 = plt.imshow(new_grid) #for imshow the array must be transposed
plt.colorbar(im4, format='%.2f', shrink=1)
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.ylim([0, 1500])
    #Axs[1].set_aspect('equal')
#plt.title('Ground Truth')
plt.grid(True)
# plt.savefig("map.PNG")
plt.show()