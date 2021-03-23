from Enviroment.map import black_white
import pandas as pd
import numpy as np
from sys import path
from Benchmark.bench import create_map


def map_bound(xs, ys, load_file=False, file=0):
    if load_file:
        with open(path[-1] + '/Data/bounds.npy'.format(file), 'rb') as bn:
            df_bounds = np.load(bn)

        with open(path[-1] + '/Data/grid.npy'.format(file), 'rb') as gd:
            grid = np.load(gd)

        with open(path[-1] + '/Data/available.npy'.format(file), 'rb') as av:
            available = np.load(av)

        # with open(path[-1] + '/Data/no_available.npy'.format(file), 'rb') as nav:
        #     no_available = np.load(nav)

        return df_bounds, grid, available

    else:
        grid, resolution = black_white(1, xs, ys)
        available, first, last = list(), list(), list()
        bound = True
        confirm = list()
        index, first_x, last_x, all_y = list(), list(), list(), list()

        for j in range(len(grid[1])):
            for i in range(len(grid)):
                if grid[i, j] == 1:
                    if bound:
                        first.append([i, j])
                        bound = False
                    available.append([i, j])
                    grid_ant = [i, j]
                else:
                    if not bound:
                        last.append(grid_ant)
                        bound = True
                    # no_available.append([i, j])

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

        with open(path[-1] + '/Data/bounds.npy'.format(file), 'wb') as bn:
            np.save(bn, df_bounds)

        with open(path[-1] + '/Data/grid.npy'.format(file), 'wb') as gd:
            np.save(gd, grid)

        with open(path[-1] + '/Data/available.npy'.format(file), 'wb') as av:
            np.save(av, available)

        # with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
        #           'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/no_available.npy', 'wb') as nav:
        #     np.save(nav, no_available)

        return df_bounds, grid, available


def interest_area(load_file=False, file=0):
    if load_file:
        with open(path[-1] + '/Data/area.npy'.format(file), 'rb') as ar:
            return np.load(ar)

    else:
        grid = map_bound(load_file=False)
        _z = create_map(grid, 1, obstacles_on=False, randomize_shekel=False, sensor="", no_maxima=10,
                        load_from_db=True, file=0)
        for j in range(len(grid[1])):
            for i in range(len(grid)):
                if grid[i, j] == 0:
                    _z[i, j] = np.nan
        _z2 = np.transpose(_z)

        with open('/Data/area.npy', 'wb') as ar:
            np.save(ar, _z2)

        return _z2


# df_bounds, grid, available, no_available = map_bound(load_file=False, file=0)
# new_grid = new_grid.replace(0, np.nan)
# new_grid = pd.DataFrame.to_numpy(new_grid)


#

# minz = np.min(_z)
#
# im4 = plt.imshow(_z2)  # for imshow the array must be transposed
# plt.colorbar(im4, format='%.2f', shrink=1)
# plt.xlabel("x [m]")
# plt.ylabel("y [m]")
# plt.ylim([0, 1500])
# # Axs[1].set_aspect('equal')
# # plt.title('Ground Truth')
# plt.grid(True)
# # plt.savefig("map.PNG")
# plt.show()
