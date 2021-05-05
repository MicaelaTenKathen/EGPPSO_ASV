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

from skopt.utils import use_named_args
from skopt.space import Real, Integer, Categorical
from skopt import gp_minimize
import skopt

from skopt.plots import plot_convergence, plot_objective


dim_c1 = Integer(name="c1", low=0, high=4)
dim_c2 = Integer(name="c2", low=0, high=4)
dim_c3 = Integer(name="c3", low=0, high=4)
dim_c4 = Integer(name="c4", low=0, high=4)
# dim_n = Categorical([10, 20, 30, 40, 50], name="t")
dim_leng_scale = Categorical([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], name="leng_scale")
dimensions = [dim_c1, dim_c2, dim_c3, dim_c4, dim_leng_scale]
dimensions_name = ["c1", "c2", "c3", "c4", "t", "leng_scale"]
default_parameters = [1, 1, 3, 3, 0.5]

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


@use_named_args(dimensions=dimensions)
def model_psogp(c1, c2, c3, c4, leng_scale):
    c11 = int(c1)
    c21 = int(c2)
    c31 = int(c3)
    c41 = int(c4)
    # t = int(t)
    leng_scale = float(leng_scale)
    global model_psogp, sigma, mu, n_plot, n_data
    xs, ys = 100, 150

    bench_function, X_test, grid, df_bounds = available_bench(xs, ys, load_file=False, load_from_db=False)

    grid_min, grid_max, grid_max_x, grid_max_y = map_values(xs, ys)

    t, GEN = 10, 400

    initPSO()
    generate(grid_min, grid_max)
    toolbox = tool(grid_min, grid_max, generate, updateParticle)
    seed_list = [7, 10, 15, 20, 22, 27, 30, 34, 35, 37, 40, 42, 45, 47, 50, 52, 55, 57, 60, 62, 64, 67, 68, 70, 90, 95,
                 120, 150, 200, 1000]

    array_MSE = list()

    for i in range(len(seed_list)):

        random.seed(seed_list[i])
        pop, best = swarm(toolbox, 4)
        stats, logbook = statistic()

        gp_best, mu_best = [0, 0], [0, 0]
        part_dist, part_ant, distances, n_data, n_plot = np.zeros(8), np.zeros(8), np.zeros(4), float(1), float(1)
        benchmark_data, n, sigma_data, mu_data, MSE_data, it = list(), list(), list(), list(), list(), list()
        g, samples = 0, 0
        x_p, y_p, x_g, y_g, y_data, part_data, x_train, y_train = list(), list(), list(), list(), list(), list(), list(), list()

        ker = RBF(length_scale=leng_scale)

        gpr = GaussianProcessRegressor(kernel=ker, alpha=1 ** 2)  # alpha = noise**2

        for part in pop:
            c1, c2, c3, c4 = 2, 2, 0, 0
            x_p, y_p, x_g, y_g, y_data, x_bench, y_bench, part, best, n_plot = part_fitness(g, xs, ys, part, part_data, x_p,
                                                                                            y_p,
                                                                                            x_g, y_g,
                                                                                            bench_function, y_data, n,
                                                                                            n_plot,
                                                                                            n_data, grid_min, X_test,
                                                                                            creator, best,
                                                                                            df_bounds, grid, part_ant,
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
            toolbox.update(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4)

        for g in range(GEN):
            if g < t:
                c1, c2, c3, c4 = 2, 2, 0, 0
            else:
                c1, c2, c3, c4 = c11, c21, c31, c41
            for part in pop:
                x_p, y_p, x_g, y_g, y_data, x_bench, y_bench, part, best, n_plot = part_fitness(g, xs, ys, part, part_data, x_p,
                                                                                                y_p, x_g, y_g,
                                                                                                bench_function, y_data,
                                                                                                n,
                                                                                                n_plot, n_data,
                                                                                                grid_min,
                                                                                                X_test,
                                                                                                creator, best,
                                                                                                df_bounds,
                                                                                                grid, part_ant,
                                                                                                init=False)
                part_ant, distances = distance(n_data, part, part_ant, distances, init=False)
                n_data += 1.0
                if n_data > 4.0:
                    n_data = float(1)
                sigma, mu, x_a, y_a = gaussian_regression(x_p, y_p, y_data, X_test, gpr)
                sigma_data, mu_data = gpr_value(x_bench, y_bench, X_test, sigma, mu, sigma_data, mu_data)
                samples += 1
            MSE_data, it = mse(g, y_data, mu_data, samples, MSE_data, it, init=False)
            t = t
            if g >= t:
                gp_best, mu_best = sigmamax(X_test, sigma, mu)
            for part in pop:
                toolbox.update(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4)
            logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
            print(logbook.stream)

        array_MSE.append(MSE_data[-1])
    array_MSE = np.array(array_MSE)
    mean_MSE = np.mean(array_MSE)
    # x_a, y_a, x_ga, y_ga = arrays(x_p, y_p, x_g, y_g)
    # savexlsx(MSE_data, sigma_data, mu_data, distances, e1, e2, e3, e4)
    # plot_gaussian(ys, x_ga, y_ga, n, mu, sigma, X_test, grid)
    # plot_benchmark(xs, ys, grid, bench_function, X_test)
    # plot_error(MSE_data, it, GEN)

    return mean_MSE


search_result = gp_minimize(func=model_psogp,
                            dimensions=dimensions,
                            n_calls=200,
                            acq_func='EI',
                            x0=default_parameters)

best_parameters = search_result.x
print(best_parameters)
