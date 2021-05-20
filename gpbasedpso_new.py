from PSO.stats_pso import statistic
from PSO.initialize_PSO import *
from PSO.fitness_pso import *

from GaussianP.gp_new import *
from GaussianP.max_values import *

from sklearn.gaussian_process import GaussianProcessRegressor

from Benchmark.bohachevsky import *

from Data_scripts.distance_new import *
from Data_scripts.error_new import *
from Data_scripts.data_save import savexlsx

from Enviroment.map import *
from Enviroment.plots import *

import time

xs, ys = 100, 150

bench_function, X_test, grid, df_bounds = available_bench(xs, ys, load_file=False, load_from_db=False)

grid_min, grid_max, grid_max_x, grid_max_y = map_values(xs, ys)

gp_best, mu_best = [0, 0], [0, 0]

c1, c2, c3, c4 = 1, 1, 3, 3

e1, e2, e3, e4, e5 = 'Pruebas/Error1.xlsx', 'Pruebas/Sigma1.xlsx', \
                     'Pruebas/Mu1.xlsx', 'Pruebas/Distance1.xlsx', 'Pruebas/Data1.xlsx'
GEN, seed = 10000, 26

part_dist, part_ant, distances, post_array = np.zeros(8), np.zeros((GEN + 1, 8)), np.zeros(
    4), np.zeros(4)
n_data, n_plot = 1, 1
benchmark_data, n, sigma_data, mu_data, MSE_data, it, mu_d = list(), list(), list(), list(), list(), list(), list()
g, k, samples, last_sample = 0, 0, 0, 0
x_p, y_p, y_data, part_data, x_g, y_g, y_mult = list(), list(), list(), list(), list(), list(), list()
fitness, x_h, y_h = list(), list(), list()
ok = True

initPSO()
generate(grid_min, grid_max)
toolbox = tool(grid_min, grid_max, generate, updateParticle)
random.seed(seed)
pop, best = swarm(toolbox, 4)
stats, logbook = statistic()
part_array = list()
s_ant = np.zeros(4)
s_n = np.array([True, True, True, True])

ker = RBF(length_scale=0.5, length_scale_bounds=(1e-1, 10))

gpr = GaussianProcessRegressor(kernel=ker, alpha=1 ** 2)  # alpha = noise**2

start_time = time.time()

for part in pop:
    print(part)
    x_p, y_p, y_data, x_bench, y_bench, part, best, n_plot, s_n = part_fitness(g, GEN, xs, ys, part, s_ant, s_n, x_p,
                                                                               y_p,
                                                                               bench_function, y_data, n,
                                                                               n_plot,
                                                                               n_data, grid_min, X_test,
                                                                               creator, best,
                                                                               df_bounds, part_ant, x_g, y_g, file=False,
                                                                               init=True)

    part_ant, distances = distance(g, GEN, n_data, part, part_ant, distances, init=True)

    sigma, mu, x_a, y_a, post_array = gaussian_regression(n_data, x_p, y_p, y_data, X_test, gpr, post_array)
    # sigma_data, mu_data = gpr_value(g, int(part[0]), int(part[1]), X_test, sigma, mu, sigma_data, mu_data)
    # samples += 1

    n_data += 1
    if n_data > 4:
        n_data = 1

gp_best, mu_best = sigmamax(X_test, sigma, mu)

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

        x_p, y_p, y_data, x_bench, y_bench, part, best, n_plot, s_n = part_fitness(g, GEN, xs, ys, part, s_ant, s_n,
                                                                                   x_p,
                                                                                   y_p,
                                                                                   bench_function, y_data, n,
                                                                                   n_plot,
                                                                                   n_data, grid_min, X_test,
                                                                                   creator, best,
                                                                                   df_bounds, part_ant, x_g, y_g,
                                                                                   file=True,
                                                                                   init=False)
        part_ant, distances = distance(g, GEN, n_data, part, part_ant, distances, init=False)
        n_data += 1
        if n_data > 4:
            n_data = 1

    if (np.mean(distances) - last_sample) >= (np.min(post_array) * 0.375):
        k += 1
        print('entro')
        e = 4
        last_sample = np.mean(distances)
        while e > 0:
            x_h.append(x_p[-e])
            y_h.append(y_p[-e])
            fitness.append(y_data[-e])
            e -= 1

            sigma, mu, x_a, y_a, post_array = gaussian_regression(n_data, x_h, y_h, fitness, X_test, gpr,
                                                               post_array)
            sigma_data, mu_data = gpr_value(g, int(part[0]), int(part[1]), X_test, sigma, mu, sigma_data, mu_data)
            samples += 1

            n_data += 1
            if n_data > 4:
                n_data = 1

        MSE_data, it = mse(g, fitness, mu_data, samples, MSE_data, it)

        gp_best, mu_best = sigmamax(X_test, sigma, mu)


    for part in pop:
        toolbox.update(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4)

    logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
    print(logbook.stream)
    mean_dist = np.mean(np.array(distances))
    print(mean_dist)

data = {'Seed': seed, 'GEN': GEN, 'Time': time.time() - start_time, 'MSE_GEN': MSE_data[-1],
        'Avr_dist': np.mean(distances)}
data_array = [seed, GEN, time.time() - start_time, MSE_data[-1], np.mean(distances)]

savexlsx(MSE_data, sigma_data, mu_data, distances, data_array, e1, e2, e3, e4, e5)
plot_gaussian(ys, x_g, y_g, n, mu, sigma, X_test, grid, grid_min, part_ant)
plot = plot_benchmark(xs, ys, grid, bench_function, X_test)
plot_error(MSE_data, it, GEN)
