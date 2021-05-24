from PSO.stats_pso import statistic
from PSO.initialize_PSO import *
from PSO.fitness_pso import *

from Original_PSO.update_opso import *

from GaussianP.gp import *

from sklearn.gaussian_process import GaussianProcessRegressor

from Benchmark.function import *

from Data_scripts.distance import *
from Data_scripts.error import *
from Data_scripts.data_treat import *
from Data_scripts.data_save import savexlsx

from Enviroment.map import *
from Enviroment.plots import *

bench_function, X_test, grid, _z = available_bench(load_file=True, load_from_db=True)

grid_min, grid_max, grid_max_x, grid_max_y = map_values(grid)

part_dist, part_ant, distances, n_data, n_plot = np.zeros(8), np.zeros(8), np.zeros(4), float(1), float(1)
benchmark_data, n, sigma_data, mu_data, MSE_data, it = list(), list(), list(), list(), list(), list()
g, samples = 0, 0
x_p, y_p, x_g, y_g, y_data = list(), list(), list(), list(), list()

GEN, t, e1, e2, e3, e4 = 100, 10, 'Pruebas/PSOError.xlsx', 'Pruebas/PSOSigma.xlsx', 'Pruebas/PSOMu' \
                                                                                    '.xlsx', \
                         'Pruebas/PSODistance.xlsx'
initPSO()
generate(grid_min, grid_max)
toolbox = tool(grid_min, grid_max, generate, updateParticleOPSO)
random.seed(26)
pop, best = swarm(toolbox, 4)
stats, logbook = statistic()

ker = initGP(0.6, 0.5, simple_equation=True)

gpr = GaussianProcessRegressor(kernel=ker, alpha=1 ** 2)  # alpha = noise**2

for part in pop:
    x_p, y_p, x_g, y_g, y_data, x_bench, y_bench, part, best, n_plot = part_fitness(g, part, x_p, y_p, x_g, y_g,
                                                                                    bench_function, y_data, n, n_plot,
                                                                                    grid_min, X_test, creator, best,
                                                                                    init=True)
    n.append(n_data)
    part_ant, distances = distance(n_data, part, part_ant, distances, init=True)
    n_data += float(1)
    if n_data > 4.0:
        n_data = float(1)
    sigma, mu, x_a, y_a = gaussian_regression(x_p, y_p, y_data, X_test, gpr)
    sigma_data, mu_data = gpr_value(x_bench, y_bench, X_test, sigma, mu, sigma_data, mu_data)
    samples += 1

MSE_data, it = mse(g, y_data, mu_data, samples, MSE_data, it, init=True)

for part in pop:
    toolbox.update(part, best)

for g in range(GEN):
    for part in pop:
        x_p, y_p, x_g, y_g, y_data, x_bench, y_bench, part, best, n_plot = part_fitness(g, part, x_p, y_p, x_g, y_g,
                                                                                        bench_function, y_data, n,
                                                                                        n_plot, grid_min, X_test,
                                                                                        creator, best, init=False)
        part_ant, distances = distance(n_data, part, part_ant, distances, init=False)
        n_data += 1.0
        if n_data > 4.0:
            n_data = float(1)
        sigma, mu, x_a, y_a = gaussian_regression(x_p, y_p, y_data, X_test, gpr)
        sigma_data, mu_data = gpr_value(x_bench, y_bench, X_test, sigma, mu, sigma_data, mu_data)
        samples += 1
    MSE_data, it = mse(g, y_data, mu_data, samples, MSE_data, it, init=False)
    for part in pop:
        toolbox.update(part, best)
    logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
    print(logbook.stream)

x_a, y_a, x_ga, y_ga = arrays(x_p, y_p, x_g, y_g)
# savexlsx(MSE_data, sigma_data, mu_data, distances, e1, e2, e3, e4)
plot_gaussian(x_ga, y_ga, n, mu, sigma, X_test, grid)
plot_benchmark(_z, grid)
plot_error(MSE_data, it, GEN)
