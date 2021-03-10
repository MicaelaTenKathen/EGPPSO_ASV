import numpy as np
import random
import math
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

def initPSO(Minimize='True'):
    if Minimize == True:
        weight = (-1.0,)
    else:
        weight = (1.0,)
    creator.create("FitnessMin", base.Fitness, weights=weight)
    creator.create("Particle", np.ndarray, fitness=creator.FitnessMin, speed=None, smin=None, smax=None, best=None)
    creator.create("BestGP", np.ndarray, fitness=creator.FitnessMin)

def generate(size, pmin, pmax, smin, smax):
    part = creator.Particle([random.uniform(pmin, pmax) for _ in range(size)])
    part.speed = np.array([random.uniform(smin, smax) for _ in range(size)])
    part.smin = smin
    part.smax = smax
    return part

def gp_generate(index_x, index_y):
    best_gp1 = [index_x, index_y]
    best_gp = np.array(best_gp1)
    return best_gp

def updateParticle(part, best, c1, c2):
    u1 = np.array([random.uniform(0, c1) for _ in range(len(part))])
    u2 = np.array([random.uniform(0, c2) for _ in range(len(part))])
    v_u1 = u1 * (part.best - part)  # diferencia con respecto a la mejor posición de la partícula
    v_u2 = u2 * (best - part)  # difeerencias con respecto a la mejor partícula de todas
    part.speed = v_u1 + v_u2 + part.speed
    for i, speed in enumerate(part.speed):
        if abs(speed) < part.smin:
            part.speed[i] = math.copysign(part.smin, speed)
        elif abs(speed) > part.smax:
            part.speed[i] = math.copysign(part.smax, speed)
    part[:] = part + part.speed
    return part

def updateParticle_w(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4, wmin, wmax):
    u1 = np.array([random.uniform(0, c1) for _ in range(len(part))])
    u2 = np.array([random.uniform(0, c2) for _ in range(len(part))])
    u3 = np.array([random.uniform(0, c3) for _ in range(len(part))])
    u4 = np.array([random.uniform(0, c4) for _ in range(len(part))])
    v_u1 = u1 * (part.best - part)  # diferencia con respecto a la mejor posición de la partícula
    v_u2 = u2 * (best - part)  # difeerencias con respecto a la mejor partícula de todas
    v_u3 = u3 * (gp_best - part)
    v_u4 = u4 * (mu_best - part)
    w = wmax - ((wmax - wmin) / GEN) * g
    part.speed = v_u1 + v_u2 + v_u3 + v_u4 + part.speed * w
    for i, speed in enumerate(part.speed):
        if abs(speed) < part.smin:
            part.speed[i] = math.copysign(part.smin, speed)
        elif abs(speed) > part.smax:
            part.speed[i] = math.copysign(part.smax, speed)
    part[:] = part + part.speed
    return part

def tool(grid_min, grid_max, c1, c2, wmin, wmax, generate, updateParticle_w, size='2', smin='-2', smax='2'):
    toolbox = base.Toolbox()
    toolbox.register("particle", generate, size=size, pmin=grid_min, pmax=grid_max, smin=smin, smax=smax)
    toolbox.register("population", tools.initRepeat, list, toolbox.particle)
    # toolbox.register("update", updateParticle, phi1=c1, phi2=c2)
    toolbox.register("update_w", updateParticle_w, wmin=wmin, wmax=wmax)
    toolbox.register("evaluate", benchmarks.bohachevsky)