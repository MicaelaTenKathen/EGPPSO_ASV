from Enviroment import *
from Bench import create_map
from PSO import *
from GP import *
from sklearn.gaussian_process import GaussianProcessRegressor
from Bohachevsky import *

grid = black_white()
resolution = 1
_z = create_map(grid, resolution, obstacles_on=False, randomize_shekel=False, sensor="", no_maxima=10, load_from_db=False,
               file=0)
if grid.shape[0] > grid.shape[1]:
    value_grid = grid.shape[0]
else:
    value_grid = grid.shape[1]

grid_min, grid_max = 0, value_grid

initPSO(Minimize='True')
tool(grid_min, grid_max, 2, 2, 0.4, 0.9, generate, updateParticle_w)

x, y, X_test, ker = initGP(0.6, 0.5, grid_min, grid_max, simple_equation='True')

gpr = GaussianProcessRegressor(kernel=ker, alpha=2 ** 2) #alpha = noise**2

benchmark_plot = bohache(grid_min, grid_max, X_test, x, y)

