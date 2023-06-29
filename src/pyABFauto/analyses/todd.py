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
        fraction = sweepIndex / \
            (abf.sweepCount - 1) if abf.sweepCount > 1 else 0
        abf.setSweep(sweepIndex)
        plt.plot(abf.sweepX, abf.sweepY, color=cmap(
            fraction), label=f"sweep {sweepIndex+1}")

    #plt.legend(loc="upper right")
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.grid(alpha=.5, ls='--')


def vc_ican_dt(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    pyabf.filter.gaussian(abf, 25)

    index1 = int(abf.sampleRate * 3.350)
    index2 = index1 + int(abf.sampleRate * 5)
    xs = np.arange(index2-index1) / abf.sampleRate

    cmap = plt.cm.get_cmap('turbo')
    fractions = np.linspace(0, 1, num=abf.sweepCount)
    colors = [cmap(x) for x in fractions]

    stim_times = np.arange(abf.sweepCount) * 50
    iadp_by_sweep = [None] * abf.sweepCount

    plt.subplot(121)
    for i in range(abf.sweepCount):
        abf.setSweep(i)
        ys = abf.sweepY[index1:index2]
        baseline = np.mean(ys[-int(len(ys)/5):])
        ys = ys - baseline
        iadp_by_sweep[i] = -np.mean(ys[:int(abf.sampleRate*3)])
        plt.plot(xs, ys, color=colors[i], label=f"sweep {i+1}")

    plt.ylabel("$I_{ADP} (pA)$")
    plt.xlabel(abf.sweepLabelX)
    plt.grid(alpha=.5, ls='--')

    plt.subplot(122)
    plt.ylabel("$I_{ADP} (pA)$")
    plt.xlabel("Stimulation Time (msec)")

    plt.plot(stim_times, iadp_by_sweep, '--', color='k')
    for i in range(abf.sweepCount):
        plt.plot(stim_times[i], iadp_by_sweep[i], "o", color=colors[i], ms=15)
    plt.grid(alpha=.5, ls='--')
