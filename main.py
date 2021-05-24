from PSO.initialize_PSO import *

from Benchmark.function import *

from Enviroment.map import *
from Enviroment.plots import *

from gppso import main_loop

from skopt.utils import use_named_args
from skopt.space import Integer, Categorical
from skopt import gp_minimize

from multiprocessing import cpu_count, freeze_support, Pool

if __name__ == '__main__':

    freeze_support()

    dim_c1 = Integer(name="c1", low=0, high=4)
    dim_c2 = Integer(name="c2", low=0, high=4)
    dim_c3 = Integer(name="c3", low=0, high=4)
    dim_c4 = Integer(name="c4", low=0, high=4)
    # dim_n = Categorical([10, 20, 30, 40, 50], name="t")
    dim_leng_scale = Categorical([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], name="leng_scale")
    dimensions = [dim_c1, dim_c2, dim_c3, dim_c4, dim_leng_scale]
    dimensions_name = ["c1", "c2", "c3", "c4", "t", "leng_scale"]
    default_parameters = [1, 1, 3, 3, 0.5]

    pool = Pool(cpu_count())

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

        global model_psogp, sigma, mu, n_plot, n_data, MSE

        xs, ys = 100, 150

        bench_function, X_test, grid, df_bounds = available_bench(xs, ys, load_file=False, load_from_db=False)

        grid_min, grid_max, grid_max_x, grid_max_y = map_values(xs, ys)

        t, GEN = 10, 400

        initPSO()
        generate(grid_min, grid_max)
        toolbox = tool(grid_min, grid_max, generate, updateParticle)

        seed_list = [7, 10, 15, 20, 22, 27, 30, 34, 35, 37, 40, 42, 45, 47, 50, 52, 55, 57, 60, 62, 64, 67, 68, 69, 70, 90,
                     23032016, 20160323, 3232016, 24072021]



        def mainpsogp():
            array_MSE = [pool.apply(main_loop, args=(seed_list, toolbox, leng_scale, bench_function, grid_min, X_test,
                                                     df_bounds, grid, GEN, c11, c21, c31, c41))]

            return array_MSE

        array_MSE = mainpsogp()

        pool.close()
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
