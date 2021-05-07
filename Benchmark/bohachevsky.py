import numpy as np
from Enviroment.bounds import *


# def bohache(X_test, x, y, toolbox, benchmark_data):
#     for i in range(len(X_test)):
#         benchmark_value = toolbox.evaluate(X_test[i])
#         benchmark_data.append(benchmark_value)
#     benchmark_array = np.array(benchmark_data)
#     meanz = np.nanmean(benchmark_array)
#     stdz = np.nanstd(benchmark_array)
#     benchmark_array = (benchmark_array - meanz) / stdz
#     bench_min = min(benchmark_array)
#     bench_max = abs(bench_min[0])
#     benchmark_plot = benchmark_array.reshape(x, y)
#     return bench_max, benchmark_plot


def available_bench(xs, ys, load_file=True, load_from_db=True):
    bench = list()
    df_bounds, grid, X_test = map_bound(xs, ys, load_file=load_file)
    _z = create_map(grid, 1, obstacles_on=False, randomize_shekel=False, sensor="", no_maxima=10,
                    load_from_db=load_from_db, file=0)
    for i in range(len(X_test)):
        bench.append(_z[X_test[i][0], X_test[i][+1]])

    bench_function = np.array(bench)
    return bench_function, X_test, grid, df_bounds
