
import pyabf
import pyabf.filter
import pyabf.tools
import pyabf.tools.ap
import pyABFauto
import pyABFauto.figure

import matplotlib.pyplot as plt
import numpy as np


def doubleStep(abf, fig, timeStartA, timeEndA, timeStartB, timeEndB):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    pointStartA = int(abf.dataRate * timeStartA)
    pointEndA = int(abf.dataRate * timeEndA)
    pointCenterA = int((pointStartA + pointEndA) / 2)
    pointStartB = int(abf.dataRate * timeStartB)
    pointEndB = int(abf.dataRate * timeEndB)
    pointCenterB = int((pointStartB + pointEndB) / 2)

    currentsA = [0]*abf.sweepCount
    currentsB = [0]*abf.sweepCount
    freqsA = [0]*abf.sweepCount
    freqsB = [0]*abf.sweepCount
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        points = pyabf.tools.ap.ap_points_currentSweep(abf)
        pointsA = [x for x in points if x >= pointStartA and x <= pointEndA]
        pointsB = [x for x in points if x >= pointStartB and x <= pointEndB]
        freqsA[sweepNumber] = len(pointsA)/(timeEndA-timeStartA)
        freqsB[sweepNumber] = len(pointsB)/(timeEndB-timeStartB)
        currentsA[sweepNumber] = abf.sweepC[pointCenterA]
        currentsB[sweepNumber] = abf.sweepC[pointCenterB]

    ax1 = plt.subplot(221)
    plt.title("All Sweeps (%d)" % abf.sweepCount)
    fig.plotStacked()
    plt.axvspan(timeStartA, timeEndA, alpha=.1, color='r', lw=0)
    plt.axvspan(timeStartB, timeEndB, alpha=.1, color='b', lw=0)

    ax2 = plt.subplot(222)
    fig.grid()
    plt.title("AP Gain")
    plt.plot(currentsA, freqsA, '.-', ms=10,
             color='r', alpha=.5, label="control")
    plt.plot(currentsB, freqsB, '.-', ms=10, color='b',
             alpha=.5, label="hyperpolarized")
    plt.legend(loc="lower right", fontsize=8)
    plt.ylabel("AP Frequency (Hz)")
    plt.xlabel(abf.sweepLabelC)

    ax1 = plt.subplot(223)
    plt.title("From Rest")
    fig.plotStacked(100, alpha=1)
    plt.ylabel("Stacked Sweeps")
    plt.yticks([], None)
    plt.axvline(timeStartA, alpha=.2, color='k', ls='--')
    plt.axvline(timeEndA, alpha=.2, color='k', ls='--')
    plt.axis([timeStartA-.1, timeEndA+.1, None, None])

    ax1 = plt.subplot(224)
    plt.title("From Hyperpolarization")
    fig.plotStacked(100, alpha=1)
    plt.ylabel("Stacked Sweeps")
    plt.yticks([], None)
    plt.axvline(timeStartB, alpha=.2, color='k', ls='--')
    plt.axvline(timeEndB, alpha=.2, color='k', ls='--')
    plt.axis([timeStartB-.1, timeEndB+.1, None, None])


def singleStep(abf, fig, timeStartA, timeEndA):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    pointStartA = int(abf.dataRate * timeStartA)
    pointEndA = int(abf.dataRate * timeEndA)
    pointCenterA = int((pointStartA + pointEndA) / 2)

    currentsA = [0]*abf.sweepCount
    freqsA = [0]*abf.sweepCount
    freqsB = [0]*abf.sweepCount
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        points = pyabf.tools.ap.ap_points_currentSweep(abf)
        pointsA = [x for x in points if x >= pointStartA and x <= pointEndA]
        freqsA[sweepNumber] = len(pointsA)/(timeEndA-timeStartA)
        currentsA[sweepNumber] = abf.sweepC[pointCenterA]

    ax1 = plt.subplot(221)
    plt.title("All Sweeps (%d)" % abf.sweepCount)
    fig.plotStacked()
    plt.axvline(timeStartA, alpha=.2, color='k', ls='--')
    plt.axvline(timeEndA, alpha=.2, color='k', ls='--')

    ax2 = plt.subplot(222)
    fig.grid()
    plt.title("AP Gain")
    plt.plot(currentsA, freqsA, '.-')
    plt.legend(loc="lower right", fontsize=8)
    plt.ylabel("AP Frequency (Hz)")
    plt.xlabel(abf.sweepLabelC)

    ax1 = plt.subplot(223)
    fig.plotStacked(100, alpha=1)
    plt.ylabel("Stacked Sweeps")
    plt.yticks([], None)
    plt.axis([timeStartA-.1, timeEndA+.1, None, None])

    ax1 = plt.subplot(224)
    plt.title("Full Recording")
    fig.plotContinuous()
    vCenter = abf.sweepY[0]
    vPad = 10
    plt.autoscale()
    plt.grid(alpha=.5)
    plt.axis([None, None, vCenter - vPad, vCenter + vPad])


def restPotential(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyabf.filter.gaussian(abf, 1)
    xs = abf.getAllXs()
    ys = abf.getAllYs()
    rmp = np.nanmean(ys)

    plt.grid(alpha=.5, ls='--')
    plt.plot(xs, ys, alpha=.7)
    plt.axhline(rmp, lw=3, color='r', ls='--')

    t = plt.gca().text(.97, .97, f"RMP = {rmp:.02f} mV",
                       transform=plt.gca().transAxes,
                       verticalalignment='top',
                       horizontalalignment='right',
                       fontsize=22,
                       family='monospace',
                       color='k')

    plt.title(abf.abfID + ".abf")
    plt.ylabel("Membrane Potential (mV)")
    plt.xlabel("Time (seconds)")
    plt.margins(0, .1)
    plt.tight_layout()
