from PSO import tool, generate, updateParticle_w
import numpy as np

benchmark_data = []

def bohache(grid_min, grid_max, X_test, benchmark_data, x, y):
    tool(grid_min, grid_max, 2, 2, 0.4, 0.9, generate, updateParticle_w)

    for i in range(len(X_test)):
        benchmark_value = toolbox.evaluate(X_test[i])
        benchmark_data.append(benchmark_value)
    benchmark_array = np.array(benchmark_data)
    meanz = np.nanmean(benchmark_array)
    stdz = np.nanstd(benchmark_array)
    benchmark_array = (benchmark_array - meanz) / stdz
    bench_min = min(benchmark_array)
    bench_max = abs(bench_min[0])
    Benchmark_plot = benchmark_array.reshape(x, y)
    return bench_max, Benchmark_plot