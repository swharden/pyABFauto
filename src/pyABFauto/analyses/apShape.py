import pyabf
import pyabf.tools
import pyabf.tools.ap

import pyABFauto
import pyABFauto.figure

import matplotlib.pyplot as plt
import matplotlib.axes
import numpy as np


def firstAP(abf, fig):

    if False:  # helps intellisense
        abf = pyabf.ABF(abf)
        #fig = pyABFauto.figure.Figure()

    apPadMsec = 50
    v = pyabf.tools.ap.extract_first_ap(abf, apPadMsec)

    # if no AP was detected, just use the first few milliseconds
    if v is None:
        v = abf.sweepY[:int(apPadMsec * abf.dataPointsPerMs)]

    t = np.arange(len(v))/abf.dataPointsPerMs
    t = t - t[int(len(t)/2)]
    dv = np.diff(v) * abf.dataRate / 1000

    plt.subplot(221)
    plt.title("First AP (V)")
    fig.grid()
    plt.plot(t, v, color='b')
    plt.margins(0, .1)
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel("Time (ms)")

    plt.subplot(222)
    plt.title("First AP ($\\Delta$V/$\\Delta$t)")
    fig.grid()
    plt.plot(t[:-1], dv, color='r')
    plt.margins(0, .1)
    plt.ylabel("mV/ms")
    plt.xlabel("mV")
    plt.axis([-10, 10, None, None])

    plt.subplot(223)
    plt.title("Full ABF")
    fig.grid()
    fig.plotContinuous()
    plt.margins(0, .1)

    plt.subplot(224)
    plt.title("First AP ($\\Delta$V/$\\Delta$t)")
    fig.grid()
    plt.plot(v[1:], dv, '.-', color='C1')
    plt.ylabel("mV/ms")
    plt.xlabel("mV")


def getAdp(abf: pyabf.ABF, sweep: int,
           baseline1: float, baseline2: float,
           adpStartTime: float, adpEndTime: float):

    abf.setSweep(sweep)

    baselineIndex1 = int(baseline1 * abf.sampleRate)
    baselineIndex2 = int(baseline2 * abf.sampleRate)
    baseline = np.mean(abf.sweepY[baselineIndex1:baselineIndex2])

    adpStartIndex = int(adpStartTime * abf.sampleRate)
    adpEndIndex = int(adpEndTime * abf.sampleRate)
    adpSpanMSec = (adpEndTime - adpStartTime) / 1000
    adpAbsolute = abf.sweepY[adpStartIndex:adpEndIndex] - baseline
    adpArea = np.sum(adpAbsolute) * adpSpanMSec  # mV * ms

    return adpArea


def plotFirstSweepADP(abf: pyabf.ABF, ax: matplotlib.axes.Axes):

    baseline1 = 1.2
    baseline2 = 1.4
    baselineIndex1 = int(baseline1 * abf.sampleRate)
    baselineIndex2 = int(baseline2 * abf.sampleRate)
    baseline = np.mean(abf.sweepY[baselineIndex1:baselineIndex2])

    adpStartIndex = abf.sweepEpochs.p1s[3]
    adpStartTime = adpStartIndex / abf.sampleRate
    adpEndTime = adpStartTime + .5
    adpArea = getAdp(abf, 0, baseline1, baseline2, adpStartTime, adpEndTime)

    ax.axvspan(adpStartTime, adpEndTime, alpha=.1,
               color='r', label=f"ADP {adpArea:.02f} mV∙ms")
    ax.axhline(baseline, ls='--', color='k', label="baseline")
    ax.legend()

    # only show a small portion of the sweep
    time1 = 1
    time2 = 3
    i1 = int(time1 * abf.sampleRate)
    i2 = int(time2 * abf.sampleRate)
    xs = abf.sweepX[i1:i2]
    ys = abf.sweepY[i1:i2]
    ax.plot(xs, ys, alpha=.5)

    ax.grid(alpha=.5, ls='--')
    ax.set_title("First Sweep")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Potential (mV)")
    ax.margins(0, .1)


def plotAdpOverTime(abf: pyabf.ABF, ax: matplotlib.axes.Axes):

    baseline1 = 1.2
    baseline2 = 1.4

    adpStartIndex = abf.sweepEpochs.p1s[3]
    adpStartTime = adpStartIndex / abf.sampleRate
    adpEndTime = adpStartTime + .5

    areas = []
    for sweepIndex in range(abf.sweepCount):
        adpArea = getAdp(abf, sweepIndex,
                         baseline1, baseline2,
                         adpStartTime, adpEndTime)
        areas.append(adpArea)

    ax.plot(abf.sweepTimesMin, areas, '.-')
    plt.axis([None, None, 0, None])

    ax.grid(alpha=.5, ls='--')
    ax.set_title("ADP Area over Time")
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("ADP Area (mV∙ms)")

    for tagTime in abf.tagTimesMin:
        ax.axvline(tagTime, linewidth=2, color='r', alpha=.5, linestyle='--')


def adp(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    plotFirstSweepADP(abf, axs[0])
    plotAdpOverTime(abf, axs[1])
    plt.tight_layout()
