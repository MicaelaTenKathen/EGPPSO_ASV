from PSO.stats_pso import statistic
from PSO.initialize_PSO import *
from PSO.fitness_pso_new import *

from GaussianP.gp_new import *
from GaussianP.max_values import *

from sklearn.gaussian_process import GaussianProcessRegressor

from Benchmark.function import *

from Data_scripts.distance_new import *
from Data_scripts.error_new import *
from Data_scripts.data_treat import *
from Data_scripts.data_save import savexlsx

from Enviroment.map import *
from Enviroment.plots import *

from skopt.utils import use_named_args
from skopt.space import Real, Integer, Categorical
from skopt import gp_minimize
import skopt

import time

from skopt.plots import plot_convergence, plot_objective

dim_c1 = Integer(low=0, high=4.0, name="c1")
dim_c2 = Integer(low=0, high=4.0, name="c2")
dim_c3 = Integer(low=0, high=4.0, name="c3")
dim_c4 = Integer(low=0, high=4.0, name="c4")
dim_leng_scale = Real(low=0.4, high=1.0, name="leng_scale")
dim_lam = Real(low=0.2, high=0.6, name='lam')
dimensions = [dim_c1, dim_c2, dim_c3, dim_c4, dim_leng_scale, dim_lam]
dimensions_name = ["c1", "c2", "c3", "c4", "leng_scale", "lam"]
default_parameters = [1, 1, 3, 3, 0.5, 0.325]

variant_names = \
    {
        1: "best/1/exp",
        2: "rand/1/exp",
        3: "rand-to-best/1/exp",
        4: "best/2/exp",
        5: "rand/2/exp",
        6: "best/1/bin",
        7: "rand/1/bin",
        8: "rand-to-best/1/bin",
        9: "best/2/bin",
        10: "rand/2/bin"
    }
number = 0


@use_named_args(dimensions=dimensions)
def model_psogp(c1, c2, c3, c4, leng_scale, lam):
    c1 = int(c1)
    c2 = int(c2)
    c3 = int(c3)
    c4 = int(c4)
    leng_scale = float(leng_scale)
    lam = float(lam)
    global model_psogp, sigma, mu, n_plot, n_data, number
    xs, ys = 100, 150

    bench_function, X_test, grid, df_bounds, grid_or = bench_total(xs, ys, load_file=False, load_from_db=True)


    grid_min, grid_max, grid_max_x, grid_max_y = map_values(xs, ys)

    GEN, e1, e2, e3, e4 = 6000, 'Pruebas/Errorn50.xlsx', 'Pruebas/Sigman50.xlsx', 'Pruebas/Mun50' \
                                                                                  '.xlsx', \
                          'Pruebas/Distancen50.xlsx'

    initPSO()
    generate(grid_min, grid_max)
    toolbox = tool(grid_min, grid_max, generate, updateParticle)
    seed_list = [20]

    array_MSE = list()
    seed = [2] #, 541, 65, 145, 541, 156, 158, 12, 3, 89] # 57, 123, 456, 789, 987, 654, 321, 147, 258, 369, 741, 852, 963, 159, 951, 753, 357, 756, 8462, 4875]
    for i in range(len(seed)):

        random.seed(seed[i])
        pop, best = swarm(toolbox, 4)
        stats, logbook = statistic()

        part_dist, part_ant, distances = np.zeros(8), np.zeros((GEN + 1, 8)), np.zeros(
            4)
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

        gpr = GaussianProcessRegressor(kernel=ker, alpha=1 ** 2)  # alpha = noise**2
        start_time = time.time()

        for part in pop:
            print(part)
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

            # sigma, mu, x_a, y_a, post_array = gaussian_regression(n_data, x_p, y_p, y_data, X_test, gpr, post_array)
            # sigma_data, mu_data = gpr_value(g, int(part[0]), int(part[1]), X_test, sigma, mu, sigma_data, mu_data)
            # samples += 1

            n_data += 1
            if n_data > 4:
                n_data = 1

        # gp_best, mu_best = sigmamax(X_test, sigma, mu)

        # MSE_data, it = mse(g, y_data, mu_data, samples, MSE_data, it)

        for part in pop:
            toolbox.update(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4)

        ok = False

        for g in range(GEN):
            # print(last_sample)
            # print(np.min(post_array) * 0.375)
            # print(np.mean(distances))
            # print(ok)
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
                k += 1
                ok = True
                print('in')
                last_sample = np.mean(distances)
                for part in pop:
                    ok, x_h, y_h, fitness, x_p, y_p, y_data, x_bench, y_bench, part, best, n_plot, s_n = part_fitness(
                        grid, ok, x_h, y_h,
                        fitness, g,
                        GEN, xs, ys,
                        part, s_ant,
                        s_n,
                        x_p,
                        y_p,
                        bench_function,
                        y_data, n,
                        n_plot,
                        n_data,
                        grid_min,
                        X_test,
                        creator, best,
                        df_bounds,
                        part_ant, x_g,
                        y_g,
                        file=True,
                        init=False)

                    sigma, mu, x_a, y_a, post_array = gp_regression(n_data, x_h, y_h, fitness, X_test, gpr, post_array)
                    sigma_data, mu_data = gpr_value(g, int(part[0]), int(part[1]), X_test, sigma, mu, sigma_data,
                                                    mu_data)
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

        data = {'Seed': seed, 'GEN': GEN, 'Time': time.time() - start_time, 'MSE_GEN': MSE_data[-1],
                'Avr_dist': np.mean(distances)}
        data_array = [seed, GEN, time.time() - start_time, MSE_data[-1], np.mean(distances)]

        #savexlsx(MSE_data, sigma_data, mu_data, distances, data_array, e1, e2, e3, e4, e5)
        #plot_gaussian(ys, x_g, y_g, n, mu, sigma, X_test, grid, grid_min, part_ant)
        #plot = plot_benchmark(xs, ys, grid, bench_function, X_test)
        #plot_error(MSE_data, it, GEN)
        if last_sample >= 170:
            array_MSE.append(MSE_data[-1])
        else:
            array_MSE.append(5)

    array_MSE = np.array(array_MSE)
    MSE = np.mean(array_MSE)

    return MSE


search_result = gp_minimize(func=model_psogp,
                            dimensions=dimensions,
                            n_calls=30,
                            acq_func='EI',
                            x0=default_parameters)

best_parameters = search_result.x
print(best_parameters)
