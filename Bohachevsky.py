import numpy as np

def bohache(X_test, x, y, toolbox, benchmark_data):
    for i in range(len(X_test)):
        benchmark_value = toolbox.evaluate(X_test[i])
        benchmark_data.append(benchmark_value)
    benchmark_array = np.array(benchmark_data)
    meanz = np.nanmean(benchmark_array)
    stdz = np.nanstd(benchmark_array)
    benchmark_array = (benchmark_array - meanz) / stdz
    bench_min = min(benchmark_array)
    bench_max = abs(bench_min[0])
    benchmark_plot = benchmark_array.reshape(x, y)
    return bench_max, benchmark_plot