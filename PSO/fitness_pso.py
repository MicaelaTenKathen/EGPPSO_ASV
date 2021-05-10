from Data_scripts.data_treat import new_limit


def part_fitness(g, GEN, xs, ys, part, part_data, x_p, y_p, bench_function, y_data, n, n_plot, n_data, grid_min, X_test, creator, best,
                 df_bounds, grid, part_ant, init=True):
    """

    :rtype: object
    :type creator: object
    """
    part, bn = new_limit(g, xs, ys, part, df_bounds, grid, part_ant, n_data, init)
    x_p.append(int(part[0]))
    y_p.append(int(part[1]))
    x_bench = int(part[0])
    y_bench = int(part[1])
    for i in range(len(X_test)):
        if X_test[i][0] == x_bench and X_test[i][1] == y_bench:
            part.fitness.values = [bench_function[i]]
            break
    y_data.append(part.fitness.values)
    if init:
        #x_gap = int(part[0]) + abs(grid_min)
        #y_gap = int(part[1]) + abs(grid_min)
        #n.append(n_plot)
        #x_g.append(x_gap)
        #y_g.append(y_gap)
        if n_plot > 4:
            n_plot = float(1)
        part.best = creator.Particle(part)
        part.best.fitness.values = part.fitness.values
    else:
        if g == GEN - 1:
            #x_gap = int(part[0]) + abs(grid_min)
            #y_gap = int(part[1]) + abs(grid_min)
            #x_g.append(x_gap)
            #y_g.append(y_gap)
            n.append(n_data)
            n_plot += float(1)
            if n_plot > 4:
                n_plot = float(1)
        if part.best.fitness < part.fitness:
            part.best = creator.Particle(part)
            part.best.fitness.values = part.fitness.values
    if best.fitness < part.fitness:
        best = creator.Particle(part)
        best.fitness.values = part.fitness.values
    return x_p, y_p, y_data, x_bench, y_bench, part, best, n_plot, bn
