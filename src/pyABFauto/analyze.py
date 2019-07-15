import os
import glob
import pyabf
import pyABFauto
import matplotlib.pyplot as plt

def analyzeFolder(folderPath):
    abfs = glob.glob(folderPath+"/*.abf")
    for abfPath in abfs:
        analyzeAbf(abfPath)


def analyzeAbf(abfPath):
    print("auto-analyzing", abfPath)
    abf = pyabf.ABF(abfPath)
    fig = pyABFauto.figure.Figure(abf)
    pyABFauto.protocols.figureByProtocol(abf, fig)
    fig.save()
