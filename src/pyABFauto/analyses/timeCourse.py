
import pyabf
import pyabf.tools
import pyabf.tools.ap
import pyABFauto

import matplotlib.pyplot as plt
import numpy as np


def apFreqOverTime(abf, fig, timeStart=None, timeEnd=None):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    if timeStart is None:
        timeStart = 0
    if timeEnd is None:
        timeEnd = abf.sweepLengthSec

    apFreqPerSweep = np.full(abf.sweepCount, np.nan)
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        points = pyabf.tools.ap.ap_points_currentSweep(abf)
        times = [point/abf.dataRate for point in points]
        times = [t for t in times if t >= timeStart and t <= timeEnd]
        apFreqPerSweep[sweepNumber] = len(times)

    plt.subplot(211)
    fig.plotContinuous(minutes=True)
    fig.addTagLines(minutes=True)
    plt.subplot(212)
    fig.grid()
    plt.plot(abf.sweepTimesMin, apFreqPerSweep, '.-')
    fig.addTagLines(minutes=True)
    plt.xlabel("time (minutes)")
    plt.ylabel("AP Frequency (full sweep) (Hz)")
    plt.margins(0, .1)
    plt.axis([None, None, -5, None])


def leftEdgeOnly():
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)


def leftBottomEdgeOnly():
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)


def gradedFiring(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    apTimes = []

    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, absoluteTime=True)
        apPoints = pyabf.tools.ap.ap_points_currentSweep(abf)
        apTimes.extend(abf.sweepX[apPoints])

        ax1 = plt.subplot(311)
        plt.ylabel("Potential (mV)")
        plt.plot(abf.sweepX, abf.sweepY, 'b-', lw=.25)
        leftEdgeOnly()

        plt.subplot(312, sharex=ax1)
        plt.ylabel("Current (pA)")
        plt.plot(abf.sweepX, abf.sweepC, 'r-', lw=1)
        leftEdgeOnly()

    plt.subplot(313, sharex=ax1)
    plt.grid(alpha=.5, ls='--')
    plt.ylabel("AP Frequency (Hz)")
    plt.xlabel("Time (sec)")

    apFreqs = 1.0/np.diff(apTimes)
    maxSaneFreq = max([x for x in apFreqs if x < 100])
    plt.plot(apTimes[1:], apFreqs, '.', alpha=.5)
    plt.axis([None, None, 0, maxSaneFreq])
    leftBottomEdgeOnly()

    plt.subplot(311)
    plt.margins(0, .1)
    plt.tight_layout()


def wideningStep(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    cmap = plt.cm.get_cmap('viridis')
    for sweepIndex in range(abf.sweepCount):
        abf.setSweep(sweepIndex)

        plt.subplot(2, 2, 1)
        plt.grid(alpha=.5, ls='--')
        plt.plot(abf.sweepX, abf.sweepY,
                 color=cmap(sweepIndex/abf.sweepCount))
        plt.margins(0, .1)

        plt.subplot(2, 2, 3)
        plt.grid(alpha=.5, ls='--')
        offset = abf.sweepIntervalSec * sweepIndex
        plt.plot(abf.sweepX + offset, abf.sweepY,
                 color=cmap(sweepIndex/abf.sweepCount))
        plt.margins(0, .1)

        plt.subplot(1, 2, 2)
        plt.grid(alpha=.5, ls='--')
        plt.plot(abf.sweepX, abf.sweepY,
                 color=cmap(sweepIndex/abf.sweepCount))
        plt.axis([5, 10, -80, 0])
