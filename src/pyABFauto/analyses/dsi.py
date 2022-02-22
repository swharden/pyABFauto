
import pyabf
import pyabf.tools
import pyabf.tools.memtest
import pyabf.filter

import pyABFauto

import matplotlib.pyplot as plt
import numpy as np


def singleSweepWithProtocol(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    ax1 = plt.subplot(211)
    plt.plot(abf.sweepX, abf.sweepY, color='b')
    plt.grid(alpha=.5, ls='--')
    plt.ylabel("Current (pA)")
    fig.drawAxisCenterText("DSI")

    plt.subplot(212, sharex=ax1)
    plt.plot(abf.sweepX, abf.sweepC, color='r')
    plt.grid(alpha=.5, ls='--')
    plt.ylabel("Potential (mV)")
    plt.xlabel("Time (sec)")
    fig.drawAxisCenterText("DSI")


def evokedInwardCurrent(abf: pyabf.ABF, fig: pyABFauto.figure.Figure, stimEpochNumber: int = 4):
    measureOffset1 = .003
    measureOffset2 = .030

    mt = pyabf.tools.memtest.Memtest(abf)

    optoPointOn = abf.sweepEpochs.p1s[stimEpochNumber]
    optoPointOff = abf.sweepEpochs.p2s[stimEpochNumber]

    optoTimeOn = optoPointOn * abf.dataSecPerPoint
    optoTimeOff = optoPointOff * abf.dataSecPerPoint

    displayPoint1 = int(optoPointOn - 0.03 * abf.dataRate)
    displayPoint2 = int(optoPointOff + 0.05 * abf.dataRate)

    baseline = [optoTimeOn - .02, optoTimeOn - .01]

    measure = [optoTimeOff + measureOffset1, optoTimeOff + measureOffset2]
    measureI1 = int(measure[0] * abf.dataRate)
    measureI2 = int(measure[1] * abf.dataRate)
    mins = np.full(abf.sweepCount, np.nan)

    sweepTimesSec = np.arange(abf.sweepCount) * abf.sweepIntervalSec
    sweepTimesMin = sweepTimesSec / 60

    plt.subplot(221)
    fig.grid()
    plt.title("All %d sweeps" % abf.sweepCount)
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, baseline=baseline)
        mins[sweepNumber] = np.min(abf.sweepY[measureI1:measureI2])
        plt.plot(abf.sweepX[displayPoint1:displayPoint2],
                 abf.sweepY[displayPoint1:displayPoint2],
                 alpha=.5,
                 linewidth=.5,
                 color='b')

    plt.axhline(0, color='k', ls='--')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)
    plt.axvspan(optoTimeOn, optoTimeOff, alpha=.5, color='y')
    plt.axvspan(baseline[0], baseline[1], alpha=.2, color='k')
    plt.axvspan(measure[0], measure[1], alpha=.2, color='r')
    plt.axis([None, None, min(mins) * 1.1, -(min(mins)*.1)])

    plt.subplot(222)
    fig.grid()
    plt.title("Peak Evoked Current")
    plt.axhline(0, color='k', ls='--')
    plt.plot(sweepTimesMin, mins, '.-', color='k')
    fig.addTagLines(minutes=True)
    plt.ylabel("Current (pA)")
    plt.xlabel("Time (minutes)")
    plt.margins(.1, .3)
    plt.axis([None, None, min(mins) * 1.1, -(min(mins)*.1)])

    plt.subplot(223)
    fig.grid()
    plt.title(mt.Ih.name)
    plt.ylabel(mt.Ih.units)
    plt.xlabel("Time (minutes)")
    plt.plot(sweepTimesMin, mt.Ih.values, '.-', color='b')
    plt.margins(.1, .3)
    fig.addTagLines(minutes=True)

    plt.subplot(224)
    fig.grid()
    plt.title(mt.Ra.name)
    plt.ylabel(mt.Ra.units)
    plt.xlabel("Time (minutes)")
    plt.plot(sweepTimesMin, mt.Ra.values, '.-', color='r')
    fig.addTagLines(minutes=True)
    plt.margins(.1, .3)
    plt.axis([None, None, 0, max(mt.Ra.values) * 1.1])
