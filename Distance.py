import math

part1x = []
part1y = []
part2x = []
part2y = []
part3x = []
part3y = []
part4x = []
part4y = []

def distance(g, n_data, part, dist1, dist2, dist3, dist4):
    b = g - 1
    if n_data == 1.0:
        part1x.append(part[0])
        part1y.append(part[1])
        dist1 = math.sqrt((part1x[g] - part1x[b]) ** 2 + (part1y[g] - part1y[b]) ** 2) + dist1
    elif n_data == 2.0:
        part2x.append(part[0])
        part2y.append(part[1])
        dist2 = math.sqrt((part2x[g] - part2x[b]) ** 2 + (part2y[g] - part2y[b]) ** 2) + dist2
    elif n_data == 3.0:
        part3x.append(part[0])
        part3y.append(part[1])
        dist3 = math.sqrt((part3x[g] - part3x[b]) ** 2 + (part3y[g] - part3y[b]) ** 2) + dist3
    elif n_data == 4.0:
        part4x.append(part[0])
        part4y.append(part[1])
        dist4 = math.sqrt((part4x[g] - part4x[b]) ** 2 + (part4y[g] - part4y[b]) ** 2) + dist4
    return dist1, dist2, dist3, dist4