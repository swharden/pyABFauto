import pyABFauto
import pyABFauto.analyses.simple

def meanSweep(abf, fig: pyABFauto.figure.Figure):
    fig.plotMean()

def continuous(abf, fig: pyABFauto.figure.Figure):
    fig.plotContinuous()