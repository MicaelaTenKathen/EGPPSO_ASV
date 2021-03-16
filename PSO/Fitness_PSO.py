from Data_treat import limit


def part_fitness(g, part, x_p, y_p, x_g, y_g, bench_function, y_data, n, n_plot, grid_min, grid_max, creator, best,
                 init=True):
    """

    :rtype: object
    :type creator: object
    """
    part = limit(part, grid_min, grid_max)
    x_p.append(int(part[0]))
    y_p.append(int(part[1]))
    x_bench = int(part[0])
    y_bench = int(part[1])
    part.fitness.values = [bench_function[x_bench + abs(grid_min), y_bench + abs(grid_min)]]
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
