from Enviroment.map import black_white
import pandas as pd
import numpy as np
from sys import path
from Benchmark.bench import create_map
import matplotlib.pyplot as plt


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
        available, first, last, y_first, y_last = list(), list(), list(), list(), list()
        bound = True
        confirm = list()
        index, first_x, last_x, all_y = list(), list(), list(), list()

        f, o = True, False
        for j in range(len(grid[1])):
            for i in range(len(grid)):
                if grid[i, j] == 1:
                    if bound:
                        first.append(i)
                        y_first.append(j)
                        u = 4 + int(y_first[0])
                        if f:
                            if j > u:
                                if y_first[-1] == y_last[-1]:
                                    first[-5] = first[-2]
                                    first.insert(-4, first[-1])
                                    y_first.insert(-4, y_first[-5])
                                    first[-4] = first[-2]
                                    first.insert(-3, first[-1])
                                    y_first.insert(-3, y_first[-4])
                                    first[-3] = first[-2]
                                    first.insert(-2, first[-1])
                                    y_first.insert(-2, y_first[-3])
                                    o = True
                                    f = False
                        bound = False
                    available.append([i, j])
                    grid_ant = i
                    grid_y = j
                else:
                    if not bound:
                        last.append(grid_ant)
                        y_last.append(grid_y)
                        bound = True
                        if o:
                            last[-5] = last[-2]
                            last.insert(-4, last[-1])
                            last[-4] = last[-2]
                            last.insert(-3, last[-1])
                            last[-3] = last[-2]
                            last.insert(-2, last[-1])
                            o = False
                    # no_available.append([i, j])

        for i in range(len(first)):
            if first[i] == last[i]:
                confirm.append(True)

        if np.array(confirm).all():
            for i in range(len(first)):
                first_x.append(first[i] + 2)
                last_x.append(last[i] - 2)
                all_y.append(y_first[i])
                # index.append(first[i][1])
            first_x.pop(0), last_x.pop(0), all_y.pop(0)
            first_x.pop(0), last_x.pop(0), all_y.pop(0)
            first_x.pop(-1), last_x.pop(-1), all_y.pop(-1)
            first_x.pop(-1), last_x.pop(-1), all_y.pop(-1)
            bounds = {'First X': first_x, 'Last X': last_x, 'Y': all_y}
            df_bounds = pd.DataFrame(data=bounds)
        else:
            print('An error occurred. Map bound, y array')

        with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
                  'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/bounds.npy', 'wb') as bn:
            np.save(bn, df_bounds)

        with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
                  'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/grid.npy', 'wb') as gd:
            np.save(gd, grid)

        with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
                  'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/available.npy', 'wb') as av:
            np.save(av, available)

        # with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
        #           'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/no_available.npy', 'wb') as nav:
        #     np.save(nav, no_available)

        return df_bounds, grid, available


def interest_area(xs, ys, load_file=False, file=0):
    if load_file:
        with open(path[-1] + '/Data/secure_grid.npy'.format(file), 'rb') as sg:
            secure_grid = np.load(sg)

        with open(path[-1] + '/Data/secure_av.npy'.format(file), 'rb') as sa:
            se_available = np.load(sa)
        return secure_grid, se_available
    else:
        df_bounds, grid, available = map_bound(xs, ys, load_file=False, file=0)
        secure_grid = np.zeros((xs, ys))
        for i in range(len(df_bounds)):
            #p = 0
            #for j in range(len(df_bounds)):
            #    if np.array(df_bounds)[i, 0] == np.array(df_bounds)[j, 0] and np.array(df_bounds)[i, 1] == \
            #            np.array(df_bounds)[j, 1] and np.array(df_bounds)[i, 2] == np.array(df_bounds)[j, 2]:
            #        p += 1
            #        if p == 2:
            #            del(df_bounds[i])
            #            p = 0
            secure_grid[np.array(df_bounds)[i, 0], np.array(df_bounds)[i, 2]] = 1
            secure_grid[np.array(df_bounds)[i, 1], np.array(df_bounds)[i, 2]] = 1
        se_first = list()
        se_last = list()
        se_available = list()
        for j in range(len(secure_grid[1])):
            con = False
            uno = 0
            for i in range(len(secure_grid)):
                if secure_grid[i, j] == 1:
                    con = True
                    uno += 1
                if con and uno == 1:
                    secure_grid[i, j] = 1

        bound = True
        for j in range(len(secure_grid[1])):
            for i in range(len(secure_grid)):
                if secure_grid[i, j] == 1:
                    if bound:
                        se_first.append([i, j])
                        bound = False
                    se_available.append([i, j])
                    grid_ant = [i, j]
                else:
                    if not bound:
                        se_last.append(grid_ant)
                        bound = True

        with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
                  'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/secure_grid.npy', 'wb') as sg:
            np.save(sg, secure_grid)

        with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
                  'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/secure_av.npy', 'wb') as sa:
            np.save(sa, se_available)

        return secure_grid, se_available, df_bounds
    # else:
    #     grid = map_bound(load_file=False)
    #     _z = create_map(grid, 1, obstacles_on=False, randomize_shekel=False, sensor="", no_maxima=10,
    #                     load_from_db=True, file=0)
    #     for j in range(len(grid[1])):
    #         for i in range(len(grid)):
    #             if grid[i, j] == 0:
    #                 _z[i, j] = np.nan
    #     _z2 = np.transpose(_z)
    #
    #     with open('C:/Users/mcjara/OneDrive - Universidad Loyola '
    #               'Andalucía/Documentos/PycharmProjects/PSO_ASVs/Data/area.npy', 'wb') as ar:
    #         np.save(ar, _z2)
    #
    #     return _z2


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
