import numpy as np
import random
import math
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools


def initPSO():
    """
    
    :rtype: object
    """
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Particle", np.ndarray, fitness=creator.FitnessMax, speed=None, smin=None, smax=None, best=None)
    creator.create("BestGP", np.ndarray, fitness=creator.FitnessMax)


def generate(pmin, pmax, smin=0, smax=0.02, size=2):
    """

    :rtype: object
    """
    part = creator.Particle([random.uniform(pmin, pmax) for _ in range(size)])
    part.speed = np.array([random.uniform(smin, smax) for _ in range(size)])
    part.smin = smin
    part.smax = smax
    return part


def updateParticle_n(part, best, gp_best, mu_best, g, GEN, c1, c2, c3, c4, wmin=0.004, wmax=0.009):
    """

    :rtype: object
    :param part: 
    :param best: 
    :param gp_best: 
    :param mu_best: 
    :param g: 
    :param GEN: 
    :param c1: 
    :param c2: 
    :param c3: 
    :param c4: 
    :param wmin: 
    :param wmax: 
    :return: 
    """
    u1 = np.array([random.uniform(0, c1) for _ in range(len(part))])
    u2 = np.array([random.uniform(0, c2) for _ in range(len(part))])
    u3 = np.array([random.uniform(0, c3) for _ in range(len(part))])
    u4 = np.array([random.uniform(0, c4) for _ in range(len(part))])
    v_u1 = u1 * (part.best - part)
    v_u2 = u2 * (best - part)
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


def tool_n(grid_min, grid_max, generate, updateParticle, size=2, smin=0, smax=0.02, wmin=0.004, wmax=0.009):
    toolbox = base.Toolbox()
    toolbox.register("particle", generate, size=size, pmin=grid_min, pmax=grid_max, smin=smin, smax=smax)
    toolbox.register("population", tools.initRepeat, list, toolbox.particle)
    toolbox.register("update", updateParticle, wmin=wmin, wmax=wmax)
    # toolbox.register("evaluate", benchmarks.bohachevsky)
    return toolbox


def swarm(toolbox, population):
    """

    :type population: object
    """
    pop = toolbox.population(n=population)
    best = pop[0]
    return pop, best
