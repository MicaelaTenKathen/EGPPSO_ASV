import openpyxl
import numpy as np
import matplotlib.pyplot as plt

def extract(n10, n15, n18, n20, n22, n25, n27):
    q = 0
    meanori = []
    stdori = []
    meangp= []
    stdgp= []
    meannew = []
    stdnew = []
    mult = []
    wb1 = openpyxl.load_workbook(n10)
    hoja1 = wb1.active
    wb2 = openpyxl.load_workbook(n15)
    hoja2 = wb2.active
    wb3 = openpyxl.load_workbook(n18)
    hoja3 = wb3.active
    wb4 = openpyxl.load_workbook(n20)
    hoja4 = wb4.active
    wb5 = openpyxl.load_workbook(n22)
    hoja5 = wb5.active
    wb6 = openpyxl.load_workbook(n25)
    hoja6 = wb6.active
    wb7 = openpyxl.load_workbook(n27)
    hoja7 = wb7.active
    while q < 15:
        q += 1
        cel1 = hoja1.cell(row=1, column=q)
        meanori.append(cel1.value)
        cel2 = hoja2.cell(row=1, column=q)
        stdori.append(cel2.value)
        cel3 = hoja3.cell(row=1, column=q)
        meangp.append(cel3.value)
        cel4 = hoja4.cell(row=1, column=q)
        stdgp.append(cel4.value)
        cel5 = hoja5.cell(row=1, column=q)
        meannew.append(cel5.value)
        cel6 = hoja6.cell(row=1, column=q)
        stdnew.append(cel6.value)
        cel7 = hoja7.cell(row=1, column=q)
        mult.append(cel7.value)

    return meanori, stdori, meangp, stdgp, meannew, stdnew, mult

def comparison(meanori, stdori, meangp, stdgp, meannew, stdnew, mult):
    width = 100
    #y = [0, 1, 2]

    fig, ax = plt.subplots()
    rects1 = ax.bar(mult - 1 * width, meanori, width, color='b', yerr=stdori, label='Original PSO', alpha=0.9)
    rects2 = ax.bar(mult, meangp, width, color='y', yerr=stdgp, label='GP-based PSO', alpha=0.9)
    #rects3 = ax.bar(it_array + 2 * width, meanpso_array3, width, color='g', yerr=stdpso_array3, label='UN + MU(3), PSO', alpha=0.9)
    rects4 = ax.bar(mult + 1 * width, meannew, width, color='c', yerr=stdnew, label='Enhanced GP-based PSO',
                    alpha=0.9)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('MSE', fontsize=12)
    ax.set_xlabel('Iterations', fontsize=12)
    #ax.set_xticks(it)
    #ax.set_yticks(y)
    #ax.set_ylim([0, 0.2])
    #ax.set_yticklabels(fontsize=12)
    #ax.set_xticklabels(fontsize=12)
    ax.legend(loc=1, fontsize=12)
    ax.grid(True)


n10 = str(r'C:\Users\mcjara\OneDrive - Universidad Loyola Andalucía\Documentos\PycharmProjects\PSO_ASVs\Pruebas\Ori\MSE_Mean.xlsx')
n15 = str(r'C:\Users\mcjara\OneDrive - Universidad Loyola Andalucía\Documentos\PycharmProjects\PSO_ASVs\Pruebas\Ori\MSE_Std.xlsx')
n18 = str(r'C:\Users\mcjara\OneDrive - Universidad Loyola Andalucía\Documentos\PycharmProjects\PSO_ASVs\Pruebas\GP\MSE_Mean.xlsx')
n20 = str(r'C:\Users\mcjara\OneDrive - Universidad Loyola Andalucía\Documentos\PycharmProjects\PSO_ASVs\Pruebas\GP\MSE_Std.xlsx')
n22 = str(r'C:\Users\mcjara\OneDrive - Universidad Loyola Andalucía\Documentos\PycharmProjects\PSO_ASVs\Pruebas\NewGP\MSE_Mean.xlsx')
n25 = str(r'C:\Users\mcjara\OneDrive - Universidad Loyola Andalucía\Documentos\PycharmProjects\PSO_ASVs\Pruebas\NewGP\MSE_Std.xlsx')
n27 = str(r'C:\Users\mcjara\OneDrive - Universidad Loyola Andalucía\Documentos\PycharmProjects\PSO_ASVs\Pruebas\Ori\MSE_Mult.xlsx')


meanori, stdori, meangp, stdgp, meannew, stdnew, mult = extract(n10, n15, n18, n20, n22, n25, n27)
mult_array = np.array(mult)
mult_array1 = np.array([400, 800, 1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000, 4400, 4800, 5200, 5600, 6000])
comparison(meanori, stdori, meangp, stdgp, meannew, stdnew, mult_array1)