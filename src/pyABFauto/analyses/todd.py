import pyabf
import pyabf.filter
import pyABFauto
import pyABFauto.figure

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def vc_ican(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    pyabf.filter.gaussian(abf, 20)

    cmap = plt.cm.get_cmap('rainbow')
    for sweepIndex in range(abf.sweepCount):
        fraction = sweepIndex / (abf.sweepCount - 1) if abf.sweepCount > 1 else 0
        abf.setSweep(sweepIndex)
        plt.plot(abf.sweepX, abf.sweepY, color=cmap(fraction), label=f"sweep {sweepIndex+1}")

    #plt.legend(loc="upper right")
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.grid(alpha=.5, ls='--')
