from Enviroment.bounds_or import map_bound_or
from Enviroment.bounds import *


def bench_total(e, xs, ys, load_file=True, load_from_db=False):
    bench = list()
    df_bounds_or, grid_or, X_test_or = map_bound_or(xs, ys, load_file=load_file, file=0)
    _z = create_map(e, grid_or, 1, obstacles_on=False, randomize_shekel=True, sensor="", no_maxima=10,
                    load_from_db=load_from_db, file=0)
    for i in range(len(X_test_or)):
        bench.append(_z[X_test_or[i][0], X_test_or[i][1]])

    bench_function_or = np.array(bench)

    secure_grid, X_test, df_bounds = interest_area(xs, ys, load_file=False, file=0)

    return bench_function_or, X_test_or, secure_grid, df_bounds, grid_or

