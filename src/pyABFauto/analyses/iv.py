"""
Figures here voltage-clamp IV plots
"""

import pyabf
import pyabf.filter
import pyabf.tools
import pyABFauto

import matplotlib.pyplot as plt
import numpy as np


def step(abf, fig, timeSteadyStart, timeSteadyEnd, timeTailStart, timeTailEnd):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    i1A = int(abf.dataRate * timeSteadyStart)
    i2A = int(abf.dataRate * timeSteadyEnd)
    i1B = int(abf.dataRate * timeTailStart)
    i2B = int(abf.dataRate * timeTailEnd)
    iCenterA = int((i1A+i2A)/2)
    iCenterB = int((i1B+i2B)/2)

    currentsA = [np.nan]*abf.sweepCount
    currentsB = [np.nan]*abf.sweepCount
    voltagesA = [np.nan]*abf.sweepCount

    pyabf.filter.gaussian(abf, 2)

    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        currentsA[sweepNumber] = np.mean(abf.sweepY[i1A:i2A])
        currentsB[sweepNumber] = np.mean(abf.sweepY[i1B:i2B])
        voltagesA[sweepNumber] = abf.sweepC[iCenterA]

    if (abf.sweepLengthSec < 2):
        subplotNumberA = 121
        subplotNumberB = 122
    else:
        subplotNumberA = 221
        subplotNumberB = 222

    ax1 = plt.subplot(subplotNumberA)
    plt.title("All Sweeps (%d)" % abf.sweepCount)
    fig.plotStacked(alpha=1)
    plt.axvspan(timeSteadyStart, timeSteadyEnd,
                alpha=.1, color='r', lw=0,
                label="steady")
    plt.axvspan(timeTailStart, timeTailEnd,
                alpha=.1, color='b', lw=0,
                label="tail")
    #plt.legend(loc="upper left", fontsize=10)

    ax2 = plt.subplot(subplotNumberB)
    fig.grid()
    plt.title("Steady State Current")
    plt.plot(voltagesA, currentsA, '.-', ms=10, color='r')
    plt.axhline(0, color='k', alpha=.2, ls='--')
    plt.axvline(-70, color='k', alpha=.2, ls='--')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelC)

    if (abf.sweepLengthSec < 2):
        return

    ax1 = plt.subplot(223)
    plt.title("Steady and Tail Currents")
    fig.plotStacked(alpha=1)
    plt.axvspan(timeSteadyStart, timeSteadyEnd, alpha=.1,
                color='r', lw=0, label="steady")
    plt.axvspan(timeTailStart, timeTailEnd, alpha=.1,
                color='b', lw=0, label="tail")
    #plt.legend(loc="upper left", fontsize=10)
    plt.axis([timeSteadyStart - .05, timeTailEnd + .05, None, None])

    ax2 = plt.subplot(224)
    fig.grid()
    plt.title("Tail Current")
    plt.plot(voltagesA, currentsB, '.-', ms=10, color='b')
    plt.axhline(0, color='k', alpha=.2, ls='--')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelC)
