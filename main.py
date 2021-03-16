# from Bench import create_map
#
# from Enviroment import *

from PSO.Stats_PSO import statistic
from PSO.Initialize_PSO import *
from PSO.Fitness_PSO import *

from GaussianP.GP import *
from GaussianP.Max_values import *

from sklearn.gaussian_process import GaussianProcessRegressor

from Bohachevsky import *

from Distance import *

from Error import *

from Data_treat import *

from Data_save import savexlsx

from Plots import *

# grid, resolution = black_white(1)
#
# grid_min, grid_max, grid_max_x, grid_max_y = map_values(grid)
#
# _z = create_map(grid, resolution, obstacles_on=False, randomize_shekel=False, sensor="", no_maxima=10,
#                 load_from_db=False, file=0)

grid, grid_min, grid_max, grid_max_x, grid_max_y = 50, -50, 50, 50, 50
gp_best, mu_best = [0, 0], [0, 0]
part_dist, part_ant, distances, n_data, n_plot = np.zeros(8), np.zeros(8), np.zeros(4), float(1), float(1)
benchmark_data, n, sigma_data, mu_data, MSE_data, it = list(), list(), list(), list(), list(), list()
g, samples = 0, 0
x_p, y_p, x_g, y_g, y_data = list(), list(), list(), list(), list()

c1, c2, c3, c4, GEN, t, e1, e2, e3, e4 = 2, 2, 0, 0, 200, 10, 'Pruebas/Error.xlsx', 'Pruebas/Sigma.xlsx', 'Pruebas/Mu' \
                                                                                                          '.xlsx', \
                                         'Pruebas/Distance.xlsx'
initPSO()
generate(grid_min, grid_max)
toolbox = tool(grid_min, grid_max, generate, updateParticle)
random.seed(26)
pop, best = swarm(toolbox, 4)
stats, logbook = statistic()

x, y, i_data, j_data, X_test, ker = initGP(grid, 0.6, 0.5, grid_min, grid_max_x, grid_max_y, simple_equation=True)

bench_max, bench_function = bohache(X_test, x, y, toolbox, benchmark_data)

gpr = GaussianProcessRegressor(kernel=ker, alpha=1 ** 2)  # alpha = noise**2

for part in pop:
    x_p, y_p, x_g, y_g, y_data, x_bench, y_bench, part, best, n_plot = part_fitness(g, part, x_p, y_p, x_g, y_g,
                                                                                    bench_function, y_data, n, n_plot,
                                                                                    grid_min, grid_max, creator, best,
                                                                                    init=True)
    n.append(n_data)
    part_ant, distances = distance(n_data, part, part_ant, distances, init=True)
    n_data += float(1)
    if n_data > 4.0:
        n_data = float(1)
    sigma, mu, Z_var, Z_mean, x_a, y_a = gaussian_regression(x, y, x_p, y_p, y_data, X_test, gpr)
    sigma_data, mu_data = gpr_value(x_bench, y_bench, grid_min, Z_mean, Z_var, sigma_data, mu_data)
    samples += 1

MSE_data, it = mse(g, y_data, mu_data, samples, MSE_data, it, init=True)

for part in pop:
    toolbox.update(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4)

for g in range(GEN):
    for part in pop:
        x_p, y_p, x_g, y_g, y_data, x_bench, y_bench, part, best, n_plot = part_fitness(g, part, x_p, y_p, x_g, y_g,
                                                                                        bench_function, y_data, n,
                                                                                        n_plot, grid_min, grid_max,
                                                                                        creator, best, init=False)
        part_ant, distances = distance(n_data, part, part_ant, distances, init=False)
        n_data += 1.0
        if n_data > 4.0:
            n_data = float(1)
        sigma, mu, Z_var, Z_mean, x_a, y_a = gaussian_regression(x, y, x_p, y_p, y_data, X_test, gpr)
        sigma_data, mu_data = gpr_value(x_bench, y_bench, grid_min, Z_mean, Z_var, sigma_data, mu_data)
        samples += 1
    MSE_data, it = mse(g, y_data, mu_data, samples, MSE_data, it, init=False)
    if g >= t:
        c1, c2, c3, c4 = 1, 1, 3, 3
        sigma_max, index_x, index_y = sigmamax(grid_min, Z_var)
        mu_max, index_xmu, index_ymu = mumax(grid_min, Z_mean)
        gp_best = gp_generate(index_x, index_y)
        mu_best = gp_generate(index_xmu, index_ymu)
    for part in pop:
        toolbox.update(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4)
    logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
    print(logbook.stream)

x_a, y_a, x_ga, y_ga = arrays(x_p, y_p, x_g, y_g)
savexlsx(MSE_data, sigma_data, mu_data, distances, e1, e2, e3, e4)
plot_gaussian(x_ga, y_ga, n, Z_var, Z_mean)
plot_benchmark(bench_function)
plot_error(MSE_data, it, GEN)
