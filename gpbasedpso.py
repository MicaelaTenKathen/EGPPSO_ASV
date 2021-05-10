from PSO.stats_pso import statistic
from PSO.initialize_PSO import *
from PSO.fitness_pso import *

from GaussianP.gp import *
from GaussianP.max_values import *

from sklearn.gaussian_process import GaussianProcessRegressor

from Benchmark.bohachevsky import *

from Data_scripts.distance import *
from Data_scripts.error import *
from Data_scripts.data_treat import *
from Data_scripts.data_save import savexlsx

from Enviroment.map import *
from Enviroment.plots import *


xs, ys = 100, 150

bench_function, X_test, grid, df_bounds = available_bench(xs, ys, load_file=False, load_from_db=False)

grid_min, grid_max, grid_max_x, grid_max_y = map_values(xs, ys)

gp_best, mu_best = [0, 0], [0, 0]
part_dist, part_ant, distances, n_data, n_plot = np.zeros(8), np.zeros(8), np.zeros(4), float(1), float(1)
benchmark_data, n, sigma_data, mu_data, MSE_data, it = list(), list(), list(), list(), list(), list()
g, samples = 0, 0
x_p, y_p, y_data, part_data = list(), list(), list(), list()

c1, c2, c3, c4, GEN, t, e1, e2, e3, e4 = 2, 2, 0, 0, 10, 10, 'Pruebas/Error400.xlsx', 'Pruebas/Sigma400.xlsx', \
                                         'Pruebas/Mu400.xlsx', 'Pruebas/Distance400.xlsx'
initPSO()
generate(grid_min, grid_max)
toolbox = tool(grid_min, grid_max, generate, updateParticle)
random.seed(26)
pop, best = swarm(toolbox, 4)
stats, logbook = statistic()
part_array = list()
distances = np.zeros(4)
part_ant = np.zeros((GEN + 1, 8))

ker = RBF(length_scale=0.5)

gpr = GaussianProcessRegressor(kernel=ker, alpha=1 ** 2)  # alpha = noise**2

for part in pop:
    x_p, y_p, y_data, x_bench, y_bench, part, best, n_plot, bn = part_fitness(g, GEN, xs, ys, part, part_data, x_p,
                                                                                        y_p, bench_function, y_data, n,
                                                                                        n_plot,
                                                                                        n_data, grid_min, X_test,
                                                                                        creator, best,
                                                                                        df_bounds, grid, part_ant,
                                                                                        init=True)
    part_array.append(part)
    part_ant, distances = distance(g, GEN, n_data, part, part_ant, distances, init=True)
    n_data += float(1)
    if n_data > 4.0:
        n_data = float(1)
    sigma, mu, x_a, y_a = gaussian_regression(x_p, y_p, y_data, X_test, gpr)
    sigma_data, mu_data = gpr_value(x_bench, y_bench, X_test, sigma, mu, sigma_data, mu_data)
    samples += 1

MSE_data, it = mse(g, y_data, mu_data, samples, MSE_data, it, init=True)

for part in pop:
    toolbox.update(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4)

for g in range(GEN):
    for part in pop:
        x_p, y_p, y_data, x_bench, y_bench, part, best, n_plot, bn = part_fitness(g, GEN, xs, ys, part, part_data, x_p,
                                                                                        y_p,
                                                                                        bench_function, y_data, n,
                                                                                        n_plot,
                                                                                        n_data, grid_min, X_test,
                                                                                        creator, best,
                                                                                        df_bounds, grid, part_ant,
                                                                                        init=True)
        part_array.append(part)
        part_ant, distances = distance(g, GEN, n_data, part, part_ant, distances, init=False)
        n_data += 1.0
        if n_data > 4.0:
            n_data = float(1)
        sigma, mu, x_a, y_a = gaussian_regression(x_p, y_p, y_data, X_test, gpr)
        sigma_data, mu_data = gpr_value(x_bench, y_bench, X_test, sigma, mu, sigma_data, mu_data)
        samples += 1
    MSE_data, it = mse(g, y_data, mu_data, samples, MSE_data, it, init=False)
    if g >= t:
        c1, c2, c3, c4 = 1, 1, 3, 3
        gp_best, mu_best = sigmamax(X_test, sigma, mu)
    for part in pop:
        toolbox.update(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4)
    logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
    print(logbook.stream)

print(MSE_data[-1])
savexlsx(MSE_data, sigma_data, mu_data, distances, e1, e2, e3, e4)
plot_gaussian(ys, x_a, y_a, n, mu, sigma, X_test, grid, grid_min, part_ant)
plot = plot_benchmark(xs, ys, grid, bench_function, X_test)
plot_error(MSE_data, it, GEN)
