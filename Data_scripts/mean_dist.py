import openpyxl
import numpy as np

def mean_distance(d, n):
    wb1 = openpyxl.load_workbook(n)
    hoja1 = wb1.active
    q = 0
    d = list()
    while q < 4:
        q += 1
        cel1 = hoja1.cell(row=1, column=q)
        d.append(cel1.value)
    d = np.array(d)
    d = np.mean(d)
    return d

seed = [20, 3, 12, 57, 65, 89, 95, 123, 145, 147, 156, 158, 159, 258, 321, 357, 369, 456, 541, 654, 741, 753, 756, 789, 852, 951, 963, 987, 4875, 8462]
dist = list()

for i in range(len(seed)):
    d = mean_distance(dist, str(r'C:\Users\mcjara\OneDrive - Universidad Loyola Andalucía\Documentos\PycharmProjects\PSO_ASVs\Pruebas\NewGP\Distance'+str(seed[i])+'.xlsx'))
    dist.append(d)
dist = np.array(dist)
mean_dist = np.mean(dist)