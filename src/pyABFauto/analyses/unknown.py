

import pyabf
import pyabf.tools
import pyABFauto

import matplotlib.pyplot as plt

def stacked(abf, fig):
    fig.plotStacked()
    fig.shadeBackground()

def continuous(abf, fig):
    fig.plotContinuous()
    fig.addTagLines()
    fig.shadeBackground()