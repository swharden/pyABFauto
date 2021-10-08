
import pyabf
import pyabf.tools
import pyABFauto

import matplotlib.pyplot as plt

def tau(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    abf.setSweep(0)
    plt.plot(abf.sweepX, abf.sweepY)