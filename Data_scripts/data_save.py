import openpyxl
import numpy as np


def savexlsx(MSE_data, sigma_data, mu_data, distances, e1, e2, e3, e4):
    wb1 = openpyxl.Workbook()
    wb2 = openpyxl.Workbook()
    wb3 = openpyxl.Workbook()
    wb4 = openpyxl.Workbook()
    hoja1 = wb1.active
    hoja1.append(MSE_data)
    wb1.save(e1)
    hoja2 = wb2.active
    hoja2.append(sigma_data)
    wb2.save(e2)
    hoja3 = wb3.active
    hoja3.append(mu_data)
    wb3.save(e3)
    hoja4 = wb4.active
    hoja4.append(list(distances))
    wb4.save(e4)