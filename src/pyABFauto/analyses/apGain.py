
import pyabf
import pyabf.filter
import pyabf.tools
import pyabf.tools.ap
import pyABFauto

import matplotlib.pyplot as plt
import numpy as np


def step(abf, fig, timeStartA, timeEndA, timeStartB, timeEndB):
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
    plt.axvspan(timeStartA, timeEndA, alpha=.2, color='r', lw=0)
    plt.axvspan(timeStartB, timeEndB, alpha=.2, color='b', lw=0)

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
    plt.title("From Rest Potential")
    fig.plotStacked()
    plt.axis([timeStartA-.1, timeEndA+.1, None, None])
    
    ax1 = plt.subplot(224)
    plt.title("From Hyperpolarization")
    fig.plotStacked()
    plt.axis([timeStartB-.1, timeEndB+.1, None, None])