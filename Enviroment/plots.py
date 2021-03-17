import matplotlib.pyplot as plt
from Data_scripts.data_treat import Z_var_mean


def plot_evolucion(log):
    gen = log.select("gen")
    fit_mins = log.select("min")
    fit_maxs = log.select("max")
    fit_ave = log.select("avg")

    fig, ax1 = plt.subplots()
    ax1.plot(gen, fit_mins, "b")
    ax1.plot(gen, fit_maxs, "r")
    ax1.plot(gen, fit_ave, "--k")
    ax1.fill_between(gen, fit_mins, fit_maxs,
                     where=fit_maxs >= fit_mins,
                     facecolor="g", alpha=0.2)
    ax1.set_xlabel("Generación")
    ax1.set_ylabel("Fitness")
    ax1.legend(["Min", "Max", "Avg"])
    plt.grid(True)


def plot_movimiento(x_a, y_a):
    plt.figure(2)
    plt.scatter(x_a, y_a)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.title("Movimiento de las partículas")
    plt.show()
    plt.close()


def plot_gaussian(x_ga, y_ga, n, mu_data, sigma_data, X_test, grid):
    Z_var, Z_mean = Z_var_mean(mu_data, sigma_data, X_test, grid)

    fig, axs = plt.subplots(2, 1, figsize=(3.5, 6))

    im1 = axs[0].scatter(x_ga, y_ga, c=n, cmap="gist_rainbow", marker='.')

    im2 = axs[0].imshow(Z_var, interpolation='bilinear', origin='lower', cmap="viridis")
    plt.colorbar(im2, ax=axs[0], format='%.2f', label='σ', shrink=1.0)
    # axs[0].set_xlabel("x [m]")
    axs[0].set_ylabel("y [m]")
    axs[0].set_aspect('equal')
    axs[0].grid(True)

    im3 = axs[1].imshow(Z_mean, interpolation='bilinear', origin='lower', cmap="jet")
    plt.colorbar(im3, ax=axs[1], format='%.2f', label='µ', shrink=1.0)
    axs[1].set_xlabel("x [m]")
    axs[1].set_ylabel("y [m]")
    axs[1].set_aspect('equal')
    axs[1].grid(True)

    plt.show()


def plot_benchmark(bench_function):
    plt.figure(2)
    im4 = plt.imshow(bench_function, interpolation='bilinear', origin='lower', cmap="jet")
    plt.colorbar(im4, format='%.2f', shrink=1)
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid(True)
    plt.show()


def plot_error(MSE_data, it, GEN):
    plt.figure(3)
    plt.plot(it, MSE_data, '-')
    plt.xlabel("Iterations")
    plt.ylabel("MSE")
    plt.xlim([0, GEN])
    plt.grid(True)
    plt.title("Mean Square Error")
    plt.show()
