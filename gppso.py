from PSO.stats_pso import statistic
from PSO.initialize_PSO import *
from PSO.fitness_pso import *

from GaussianP.gp import *
from GaussianP.max_values import *

from sklearn.gaussian_process import GaussianProcessRegressor

from Data_scripts.distance import *
from Data_scripts.error import *

from Enviroment.plots import *


def main_loop(seed_list, toolbox, leng_scale, bench_function, grid_min, X_test, df_bounds, grid, GEN, c11, c21, c31,
              c41):
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
            x_p, y_p, x_g, y_g, y_data, x_bench, y_bench, part, best, n_plot = part_fitness(g, part, part_data, x_p,
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
                x_p, y_p, x_g, y_g, y_data, x_bench, y_bench, part, best, n_plot = part_fitness(g, part, part_data, x_p,
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

    return array_MSE
