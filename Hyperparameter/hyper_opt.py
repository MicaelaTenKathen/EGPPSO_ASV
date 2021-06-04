from PSO.stats_pso import statistic
from PSO.initialize_PSO_new import *
from PSO.fitness_pso_new import *

from GaussianP.gp_new import *
from GaussianP.max_values import *

from sklearn.gaussian_process import GaussianProcessRegressor

from Benchmark.function import *

from Data_scripts.distance import *
from Data_scripts.error import *

from Enviroment.map import *
from Enviroment.plots import *

from bayes_opt import BayesianOptimization


number = 0

pbounds = {'c1': (0, 4), 'c2': (0, 4), 'c3': (0, 4), 'c4': (0, 4), 'leng_scale': (0.4, 1.0), 'lam': (0.1, 0.5)}


def model_psogp(c1, c2, c3, c4, leng_scale, lam):
    c1 = c1
    c2 = c2
    c31 = c3
    c41 = c4
    c3 = 0
    c4 = 0
    leng_scale = float(leng_scale)
    lam = float(lam)

    global model_psogp, sigma, mu, n_plot, n_data, number, bench_function, grid, X_test, df_bounds

    xs, ys = 100, 150
    grid_min, grid_max, grid_max_x, grid_max_y = map_values(xs, ys)
    GEN = 6000

    num = 3
    num_total = 10
    array_MSE = np.zeros(num_total)

    # while num < num_total:
    if num == 0:
        bench_function, X_test, grid, df_bounds, grid_or = bench_total(path[-1] + '/Data/shww.npy'.format(0), xs, ys,
                                                                       load_file=False, load_from_db=True)
    elif num == 1:
        bench_function, X_test, grid, df_bounds, grid_or = bench_total(path[-1] + '/Data/shww1.npy'.format(0), xs, ys,
                                                                       load_file=False, load_from_db=True)
    elif num == 2:
        bench_function, X_test, grid, df_bounds, grid_or = bench_total(path[-1] + '/Data/shww2.npy'.format(0), xs, ys,
                                                                       load_file=False, load_from_db=True)
    elif num == 3:
        bench_function, X_test, grid, df_bounds, grid_or = bench_total(path[-1] + '/Data/shww3.npy'.format(0), xs, ys,
                                                                       load_file=False, load_from_db=True)
    elif num == 4:
        bench_function, X_test, grid, df_bounds, grid_or = bench_total(path[-1] + '/Data/shww4.npy'.format(0), xs, ys,
                                                                       load_file=False, load_from_db=True)
    elif num == 5:
        bench_function, X_test, grid, df_bounds, grid_or = bench_total(path[-1] + '/Data/shww5.npy'.format(0), xs, ys,
                                                                       load_file=False, load_from_db=True)
    elif num == 6:
        bench_function, X_test, grid, df_bounds, grid_or = bench_total(path[-1] + '/Data/shww6.npy'.format(0), xs, ys,
                                                                       load_file=False, load_from_db=True)
    elif num == 7:
        bench_function, X_test, grid, df_bounds, grid_or = bench_total(path[-1] + '/Data/shww7.npy'.format(0), xs, ys,
                                                                       load_file=False, load_from_db=True)
    elif num == 8:
        bench_function, X_test, grid, df_bounds, grid_or = bench_total(path[-1] + '/Data/shww8.npy'.format(0), xs, ys,
                                                                       load_file=False, load_from_db=True)
    elif num == 9:
        bench_function, X_test, grid, df_bounds, grid_or = bench_total(path[-1] + '/Data/shww9.npy'.format(0), xs, ys,
                                                                       load_file=False, load_from_db=True)

    initPSO()
    generate(grid_min, grid_max)
    toolbox = tool_n(grid_min, grid_max, generate, updateParticle_n)
    seed = [20]  # , 541, 65, 145, 541, 156, 158, 12, 3, 89] # 57, 123, 456, 789, 987, 654, 321, 147, 258, 369, 741,
    # 852, 963, 159, 951, 753, 357, 756, 8462, 4875]

    num += 1
    random.seed(seed[0])
    pop, best = swarm(toolbox, 4)
    stats, logbook = statistic()

    part_dist, part_ant, distances = np.zeros(8), np.zeros((GEN + 1, 8)), np.zeros(4)
    n_data, n_plot = 1, 1
    benchmark_data, n, sigma_data, mu_data, MSE_data, it, mu_d = list(), list(), list(), list(), list(), list(), list()
    g, k, samples, last_sample = 0, 0, 0, 0
    x_p, y_p, y_data, part_data, x_g, y_g, y_mult = list(), list(), list(), list(), list(), list(), list()
    fitness, x_h, y_h = list(), list(), list()
    ok = False
    gp_best, mu_best = [0, 0], [0, 0]
    part_array = list()
    s_ant = np.zeros(4)
    s_n = np.array([True, True, True, True])

    ker = RBF(length_scale=leng_scale, length_scale_bounds=(1e-1, 10))
    post_array = [leng_scale, leng_scale, leng_scale, leng_scale]

    gpr = GaussianProcessRegressor(kernel=ker, alpha=1 ** 2)

    for part in pop:
        ok, x_h, y_h, fitness, x_p, y_p, y_data, x_bench, y_bench, part, best, n_plot, s_n = part_fitness(grid, ok,
                                                                                                          x_h, y_h,
                                                                                                          fitness,
                                                                                                          g, GEN,
                                                                                                          xs, ys,
                                                                                                          part,
                                                                                                          s_ant,
                                                                                                          s_n, x_p,
                                                                                                          y_p,
                                                                                                          bench_function,
                                                                                                          y_data, n,
                                                                                                          n_plot,
                                                                                                          n_data,
                                                                                                          grid_min,
                                                                                                          X_test,
                                                                                                          creator,
                                                                                                          best,
                                                                                                          df_bounds,
                                                                                                          part_ant,
                                                                                                          x_g, y_g,
                                                                                                          file=False,
                                                                                                          init=True)

        part_ant, distances = distance(g, GEN, n_data, part, part_ant, distances, init=True)

        n_data += 1
        if n_data > 4:
            n_data = 1

    for part in pop:
        toolbox.update(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4)

    ok = False

    for g in range(GEN):
        for part in pop:
            ok, x_h, y_h, fitness, x_p, y_p, y_data, x_bench, y_bench, part, best, n_plot, s_n = part_fitness(grid,
                                                                                                              ok,
                                                                                                              x_h,
                                                                                                              y_h,
                                                                                                              fitness,
                                                                                                              g,
                                                                                                              GEN,
                                                                                                              xs,
                                                                                                              ys,
                                                                                                              part,
                                                                                                              s_ant,
                                                                                                              s_n,
                                                                                                              x_p,
                                                                                                              y_p,
                                                                                                              bench_function,
                                                                                                              y_data,
                                                                                                              n,
                                                                                                              n_plot,
                                                                                                              n_data,
                                                                                                              grid_min,
                                                                                                              X_test,
                                                                                                              creator,
                                                                                                              best,
                                                                                                              df_bounds,
                                                                                                              part_ant,
                                                                                                              x_g,
                                                                                                              y_g,
                                                                                                              file=True,
                                                                                                              init=False)
            part_ant, distances = distance(g, GEN, n_data, part, part_ant, distances, init=False)
            n_data += 1
            if n_data > 4:
                n_data = 1

        if (np.mean(distances) - last_sample) >= (np.min(post_array) * lam):
            c3 = c31
            c4 = c41
            k += 1
            ok = True
            last_sample = np.mean(distances)

            for part in pop:
                ok, x_h, y_h, fitness, x_p, y_p, y_data, x_bench, y_bench, part, best, n_plot, s_n = part_fitness(grid,
                                                                                                                  ok,
                                                                                                                  x_h,
                                                                                                                  y_h,
                                                                                                                  fitness,
                                                                                                                  g,
                                                                                                                  GEN,
                                                                                                                  xs,
                                                                                                                  ys,
                                                                                                                  part,
                                                                                                                  s_ant,
                                                                                                                  s_n,
                                                                                                                  x_p,
                                                                                                                  y_p,
                                                                                                                  bench_function,
                                                                                                                  y_data,
                                                                                                                  n,
                                                                                                                  n_plot,
                                                                                                                  n_data,
                                                                                                                  grid_min,
                                                                                                                  X_test,
                                                                                                                  creator,
                                                                                                                  best,
                                                                                                                  df_bounds,
                                                                                                                  part_ant,
                                                                                                                  x_g,
                                                                                                                  y_g,
                                                                                                                  file=True,
                                                                                                                  init=False)

                sigma, mu, x_a, y_a, post_array = gp_regression(n_data, x_h, y_h, fitness, X_test, gpr, post_array)
                sigma_data, mu_data = gpr_value(g, int(part[0]), int(part[1]), X_test, sigma, mu, sigma_data, mu_data)

                samples += 1

                n_data += 1
                if n_data > 4:
                    n_data = 1

            MSE_data, it = mse(g, fitness, mu_data, samples, MSE_data, it)

            gp_best, mu_best = sigmamax(X_test, sigma, mu)
            ok = False

        for part in pop:
            toolbox.update(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4)

        logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        print(logbook.stream)
        mean_dist = np.mean(np.array(distances))
        print(mean_dist)

    # array_MSE[num - 1] = MSE_data[-1]

    # array_MSE = np.array(array_MSE)

    # MSE = np.mean(array_MSE)

    MSE = MSE_data[-1] * -1

    return MSE


optimizer = BayesianOptimization(
            f=model_psogp,
            pbounds=pbounds,
            random_state=1)

optimizer.maximize(init_points=10, n_iter=20, acq='ei')

print(optimizer.max)

for i, res in enumerate(optimizer.res):
    print("Iteration {}: \n\t{}".format(i, res))