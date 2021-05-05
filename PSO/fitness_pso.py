from Data_scripts.data_treat import new_limit


def part_fitness(g, xs, ys, part, part_data, x_p, y_p, x_g, y_g, bench_function, y_data, n, n_plot, n_data, grid_min, X_test, creator, best,
                 df_bounds, grid, part_ant, init=True):
    """

    :rtype: object
    :type creator: object
    """
    part = new_limit(xs, ys, part, df_bounds, grid, part_ant, n_data)
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
        part.best = creator.Particle(part)
        part.best.fitness.values = part.fitness.values
        x_gap = int(part[0]) + abs(grid_min)
        y_gap = int(part[1]) + + abs(grid_min)
        x_g.append(x_gap)
        y_g.append(y_gap)
    else:
        if g % 10 == 0:
            x_gap = int(part[0]) + abs(grid_min)
            y_gap = int(part[1]) + abs(grid_min)
            x_g.append(x_gap)
            y_g.append(y_gap)
            n.append(n_plot)
            n_plot += float(1)
            if n_plot > 4:
                n_plot = float(1)
        if part.best.fitness < part.fitness:
            part.best = creator.Particle(part)
            part.best.fitness.values = part.fitness.values
    if best.fitness < part.fitness:
        best = creator.Particle(part)
        best.fitness.values = part.fitness.values
    return x_p, y_p, x_g, y_g, y_data, x_bench, y_bench, part, best, n_plot
