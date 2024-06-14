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
    # plt.legend(loc="upper left", fontsize=10)

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
    # plt.legend(loc="upper left", fontsize=10)
    plt.axis([timeSteadyStart - .05, timeTailEnd + .05, None, None])

    ax2 = plt.subplot(224)
    fig.grid()
    plt.title("Tail Current")
    plt.plot(voltagesA, currentsB, '.-', ms=10, color='b')
    plt.axhline(0, color='k', alpha=.2, ls='--')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelC)


def step_fast(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    currents = [np.nan]*abf.sweepCount
    voltages = [np.nan]*abf.sweepCount

    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        i1 = int(len(abf.sweepY) * .75)
        currents[sweepNumber] = np.mean(abf.sweepY[i1:])
        voltages[sweepNumber] = abf.sweepC[i1]

    plt.plot(currents, voltages, '.-', color='k', lw=2, ms=10)
    plt.grid(alpha=.5, ls='--')
    plt.ylabel("Current (pA)")
    plt.xlabel("Voltage (mV)")
    plt.axvline(0, color='k', ls='--')
    plt.axhline(0, color='k', ls='--')


def iv_over_time_4(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    def plotMean(t1, t2):
        i1 = int(t1 * abf.sampleRate)
        i2 = int(t2 * abf.sampleRate)

        sweepCurrents = [np.nan]*abf.sweepCount
        sweepTimes = np.arange(abf.sweepCount) * abf.sweepLengthSec / 60

        voltage = abf.sweepC[i1]
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            sweepCurrents[sweepNumber] = np.mean(abf.sweepY[i1:i2])

        plt.plot(sweepTimes, sweepCurrents, '.-', label=str(voltage))

    plt.grid(alpha=.5, ls='--')
    plotMean(39.5, 40.5)
    plotMean(29.5, 30.5)
    plotMean(24.5, 25.5)
    plotMean(9.5, 10.5)
    plt.ylabel("Current (pA)")
    plt.xlabel("Time (min)")
    plt.legend()


def iv_over_time_4b(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    def plotMean(ax, t1, t2):
        plt.sca(ax)
        i1 = int(t1 * abf.sampleRate)
        i2 = int(t2 * abf.sampleRate)

        sweepCurrents = [np.nan]*abf.sweepCount
        sweepTimes = np.arange(abf.sweepCount) * abf.sweepLengthSec / 60

        voltage = abf.sweepC[i1]
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            sweepCurrents[sweepNumber] = np.mean(abf.sweepY[i1:i2])

        plt.title(f"{voltage} mV")
        plt.grid(alpha=.5, ls='--')
        plt.plot(sweepTimes, sweepCurrents, '.-')
        plt.ylabel("Current (pA)")
        plt.xlabel("Time (min)")

    fig2, axs2 = plt.subplots(2, 2)
    plotMean(axs2[0, 0], 9.5, 10.5)
    plotMean(axs2[0, 1], 24.5, 25.5)
    plotMean(axs2[1, 0], 29.5, 30.5)
    plotMean(axs2[1, 1], 39.5, 40.5)
