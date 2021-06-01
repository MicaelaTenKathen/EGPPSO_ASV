from Enviroment.map import black_white
import pandas as pd
import numpy as np
from sys import path
from Benchmark.bench import create_map
import matplotlib.pyplot as plt


def map_bound_or(xs, ys, load_file=False, file=0):
    if load_file:
        with open(path[-1] + '/Data/bounds_or.npy'.format(file), 'rb') as bno:
            df_bounds_or = np.load(bno)

        with open(path[-1] + '/Data/grid_or.npy'.format(file), 'rb') as gdo:
            grid_or = np.load(gdo)

        with open(path[-1] + '/Data/available_or.npy'.format(file), 'rb') as avo:
            available_or = np.load(avo)

        # with open(path[-1] + '/Data/no_available.npy'.format(file), 'rb') as nav:
        #     no_available = np.load(nav)

        return df_bounds_or, grid_or, available_or

    else:
        grid_or, resolution = black_white(1, xs, ys)
        available_or, first, last, y_first, y_last = list(), list(), list(), list(), list()
        bound = True
        confirm = list()
        index, first_x, last_x, all_y = list(), list(), list(), list()

        f, o = True, False
        for j in range(len(grid_or[1])):
            for i in range(len(grid_or)):
                if grid_or[i, j] == 1:
                    if bound:
                        first.append(i)
                        y_first.append(j)
                        bound = False
                    available_or.append([i, j])
                    grid_ant = i
                    grid_y = j
                else:
                    if not bound:
                        last.append(grid_ant)
                        y_last.append(grid_y)
                        bound = True
                    # no_available.append([i, j])

        for i in range(len(first)):
            if first[i] == last[i]:
                confirm.append(True)

        if np.array(confirm).all():
            for i in range(len(first)):
                first_x.append(first[i])
                last_x.append(last[i])
                all_y.append(y_first[i])
                # index.append(first[i][1])
            first_x.pop(0), last_x.pop(0), all_y.pop(0)
            first_x.pop(0), last_x.pop(0), all_y.pop(0)
            first_x.pop(-1), last_x.pop(-1), all_y.pop(-1)
            first_x.pop(-1), last_x.pop(-1), all_y.pop(-1)
            bounds = {'First X': first_x, 'Last X': last_x, 'Y': all_y}
            df_bounds_or = pd.DataFrame(data=bounds)
        else:
            print('An error occurred. Map bound, y array')

        with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
                  'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/bounds_or.npy', 'wb') as bno:
            np.save(bno, df_bounds_or)

        with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
                  'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/grid_or.npy', 'wb') as gdo:
            np.save(gdo, grid_or)

        with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
                  'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/available.npy', 'wb') as avo:
            np.save(avo, available_or)

        # with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
        #           'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/no_available.npy', 'wb') as nav:
        #     np.save(nav, no_available)

        return df_bounds_or, grid_or, available_or




# df_bounds, grid, available = map_bound(100, 150)
# grid[grid == 0] = np.nan
# new_grid = pd.DataFrame.to_numpy(new_grid)
#secure = interest_area(100, 150, load_file=False, file=0)
#secure[secure == 0] = np.nan


#

# minz = np.min(_z)
#
# im4 = plt.imshow(grid.T)  # for imshow the array must be transposed
#im5 = plt.imshow(secure.T)  # for imshow the array must be transposed

# plt.colorbar(im4, format='%.2f', shrink=1)
# plt.xlabel("x [m]")
# plt.ylabel("y [m]")
# plt.ylim([0, 1500])
# # Axs[1].set_aspect('equal')
# # plt.title('Ground Truth')
# plt.grid(True)
# # plt.savefig("map.PNG")
#plt.show()
# im5.show()
