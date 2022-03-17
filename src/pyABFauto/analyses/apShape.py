import pyabf
import pyabf.filter
import pyabf.tools
import pyabf.tools.ap

import pyABFauto
import pyABFauto.figure

import matplotlib.pyplot as plt
import matplotlib.axes
import numpy as np


def get_threshold_and_rheobase(abf: pyabf.ABF):

    for sweep in range(abf.sweepCount):
        abf.setSweep(sweep)
        apPoints = pyabf.tools.ap.ap_points_currentSweep(abf)
        if len(apPoints):
            firstPoint = apPoints[0]
            break
    else:
        return (None, None)

    # back up 5ms from peak depolarization
    firstPoint -= 5 * abf.dataPointsPerMs

    voltage = abf.sweepY[firstPoint]
    current = abf.sweepC[firstPoint]
    return (voltage, current)


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

    threshold, rheobase = get_threshold_and_rheobase(abf)

    if threshold:
        summary = f"Threshold:\n{threshold:.01f} mV\n\nRheobase:\n{rheobase:.01f} pA"
    else:
        summary = "no AP detected"

    bbox = dict(facecolor='#DDDDDD66', edgecolor='#00000000',
                boxstyle='round,pad=.4')
    plt.gca().text(0.04, 0.94, summary, verticalalignment='top',
                   horizontalalignment='left',
                   transform=plt.gca().transAxes, fontsize=10,
                   bbox=bbox, family='monospace')

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
    adpAbsolute = abf.sweepY[adpStartIndex:adpEndIndex] - baseline
    adpArea = np.mean(adpAbsolute) * (adpEndTime - adpStartTime)  # mV * sec

    return adpArea


def plotFirstSweepADP(abf: pyabf.ABF, ax: matplotlib.axes.Axes):

    baseline1 = 1.2
    baseline2 = 1.4
    baselineIndex1 = int(baseline1 * abf.sampleRate)
    baselineIndex2 = int(baseline2 * abf.sampleRate)
    baseline = np.mean(abf.sweepY[baselineIndex1:baselineIndex2])
    ax.axhline(baseline, ls='--', color='k',
               label=f"{baseline:.03f} mV")

    adpStartIndex = abf.sweepEpochs.p1s[3]
    adpStartTime = adpStartIndex / abf.sampleRate
    adpEndTime = adpStartTime + .5
    adpArea = getAdp(abf, 0, baseline1, baseline2, adpStartTime, adpEndTime)

    # shade area under ADP
    adpStartIndex = int(abf.sampleRate * adpStartTime)
    adpEndIndex = int(abf.sampleRate * adpEndTime)
    adpXs = abf.sweepX[adpStartIndex:adpEndIndex]
    adpYs = abf.sweepY[adpStartIndex:adpEndIndex]
    ax.fill_between(adpXs, adpYs, baseline, alpha=.2, color='r',
                    label=f"{adpArea:.03f} mV∙s")

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
    ax.legend(loc="upper left")


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


def adp2(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    baseline1 = 3
    baseline2 = 5
    baselineIndex1 = int(baseline1 * abf.sampleRate)
    baselineIndex2 = int(baseline2 * abf.sampleRate)
    plt.axhline(0, ls='--', color='k')

    pyabf.filter.gaussian(abf, 10)
    cmap = plt.cm.get_cmap('viridis')
    for sweepIndex in abf.sweepList[::-1]:
        abf.setSweep(sweepIndex)
        color = cmap(sweepIndex/abf.sweepCount)
        baseline = np.mean(abf.sweepY[baselineIndex1:baselineIndex2])
        plt.plot(abf.sweepX, abf.sweepY - baseline, color=color,
                 alpha=1, label=f"sweep {sweepIndex+1}")

    plt.grid(alpha=.5, ls='--')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Δ Potential (mV)")
    plt.margins(0, .1)
    plt.legend(loc="upper right")
    plt.axis([None, None, -10, 20])
