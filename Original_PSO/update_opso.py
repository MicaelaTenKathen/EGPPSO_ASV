import numpy as np
import random
import math


def updateParticleOPSO(part, best, phi1=2, phi2=2):
    u1 = np.array([random.uniform(0, phi1) for _ in range(len(part))])
    u2 = np.array([random.uniform(0, phi2) for _ in range(len(part))])
    v_u1 = u1 * (part.best - part)
    v_u2 = u2 * (best - part)
    part.speed = v_u1 + v_u2 + part.speed
    for i, speed in enumerate(part.speed):
        if abs(speed) < part.smin:
            part.speed[i] = math.copysign(part.smin, speed)
        elif abs(speed) > part.smax:
            part.speed[i] = math.copysign(part.smax, speed)
    part[:] = part + part.speed