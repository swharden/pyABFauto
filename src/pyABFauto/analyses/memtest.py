"""
Figures here are for multi-sweep membrane tests intended
to calcaulate mean passive membrane properties.
"""

import pyabf
import pyabf.tools
import pyABFauto

import matplotlib.pyplot as plt
import numpy as np


def figureMemtest(abf, fig):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    mt = pyabf.tools.Memtest(abf)
    summary = mt.summary.replace("+/-", "±").replace("MOhm", "MΩ")

    # calculate RMS noise
    lastPreSweepIndex = abf.sweepEpochs.p2s[0]
    rmsNoiseBySweep = np.zeros(abf.sweepCount)
    for sweepIndex in range(abf.sweepCount):
        abf.setSweep(sweepIndex)
        preSweepValues = abf.sweepY[0:lastPreSweepIndex]
        sweepStdev = np.std(preSweepValues)
        rmsNoiseBySweep[sweepIndex] = sweepStdev
    rmsNoise = np.min(rmsNoiseBySweep)
    summary += f"\nRMS Noise: {round(rmsNoise, 3)} pA"

    # determine lowpass filter
    filterHz = abf._adcSection.fTelegraphFilter[0]
    summary += f"\nLowpass Filter: {filterHz/1000:.02f} kHz"

    plt.title(f"{abf.sweepCount} Sweep Membrane Test")

    bbox = dict(facecolor='#DDDDDD66', edgecolor='#00000000',
                boxstyle='round,pad=.4')
    plt.gca().text(0.96, 0.96, summary, verticalalignment='top',
                   horizontalalignment='right',
                   transform=plt.gca().transAxes, fontsize=10,
                   bbox=bbox, family='monospace')

    fig.plotStacked()


def figureOverTime(abf, fig):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    mt = pyabf.tools.Memtest(abf)

    sweepTimesSec = np.arange(abf.sweepCount) * abf.sweepIntervalSec
    sweepTimesMin = sweepTimesSec / 60

    plt.subplot(221)
    fig.grid()
    plt.title(mt.Ih.name)
    plt.ylabel(mt.Ih.units)
    plt.plot(sweepTimesMin, mt.Ih.values, '.', color='b')
    plt.margins(0, .2)
    fig.addTagLines(minutes=True)

    plt.subplot(222)
    fig.grid()
    plt.title(mt.Rm.name)
    plt.ylabel(mt.Rm.units)
    plt.plot(sweepTimesMin, mt.Rm.values, '.', color='r')
    plt.margins(0, .2)
    plt.axis([None, None, 0, None])
    fig.addTagLines(minutes=True)

    plt.subplot(223)
    fig.grid()
    plt.title(mt.Ra.name)
    plt.ylabel(mt.Ra.units)
    plt.plot(sweepTimesMin, mt.Ra.values, '.', color='k')
    plt.margins(0, .2)
    plt.axis([None, None, 0, None])
    fig.addTagLines(minutes=True)

    plt.subplot(224)
    fig.grid()
    plt.title("Full Recording")
    fig.plotContinuous(startAtSec=.5, minutes=True)
    fig.addTagLines(minutes=True)

    return
