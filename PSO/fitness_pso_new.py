from Data_scripts.data_bound import new_limit
import numpy as np

def part_fitness(grid, ok, x_h, y_h, fitness, g, GEN, xs, ys, part, s_ant, s_n, x_p, y_p, bench_function, y_data, n, n_plot, n_data, grid_min, X_test, creator, best,
                 df_bounds, part_ant, x_g, y_g, file, init=True):
    """

    :rtype: object
    :type creator: object
    """
    part, s_n = new_limit(g, xs, ys, part, df_bounds, part_ant, n_data, s_ant, s_n, grid)
    x_bench = int(part[0])
    y_bench = int(part[1])

    for i in range(len(X_test)):
        if X_test[i][0] == x_bench and X_test[i][1] == y_bench:
            part.fitness.values = [bench_function[i]]
            break
    if ok:
        x_h.append(int(part[0]))
        y_h.append(int(part[1]))
        fitness.append(part.fitness.values)
    else:
        x_p.append(part[0])
        y_p.append(part[1])
        y_data.append(part.fitness.values)
        if init:
            x_gap = int(part[0]) + abs(grid_min)
            y_gap = int(part[1]) + abs(grid_min)
            #n.append(n_plot)
            x_g.append(x_gap)
            y_g.append(y_gap)
            n.append(n_data)
            # n_data += 1.0
            # if n_data > 4.0:
            #     n_data = float(1)
            # n_plot += 1
            if n_plot > 4:
                n_plot = float(1)
            part.best = creator.Particle(part)
            part.best.fitness.values = part.fitness.values
        else:
            if g == GEN - 1:
                x_gap = int(part[0]) + abs(grid_min)
                y_gap = int(part[1]) + abs(grid_min)
                x_g.append(x_gap)
                y_g.append(y_gap)
                n.append(n_data)
                # n_data += 1.0
                # if n_data > 4.0:
                #     n_data = float(1)
                n_plot += float(1)
                if n_plot > 4:
                    n_plot = float(1)
            if part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
        if best.fitness < part.fitness:
            best = creator.Particle(part)
            best.fitness.values = part.fitness.values
    return ok, x_h, y_h, fitness, x_p, y_p, y_data, x_bench, y_bench, part, best, n_plot, s_n
