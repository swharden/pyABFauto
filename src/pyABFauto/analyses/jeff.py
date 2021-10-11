
import pyABFauto
from typing import Tuple
import pyabf
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import matplotlib.axes


def getAntiPeakIndex(sweep: np.ndarray, sampleRate: int, start: float, end: float) -> int:
    i1 = int(start * sampleRate)
    i2 = int(end * sampleRate)
    segment = sweep[i1:i2]
    minIndex = np.argmin(segment)
    return minIndex + i1


def getMean(abf: pyabf.ABF, start: float, end: float, baseline: float = 0) -> float:
    i1 = int(start * abf.sampleRate)
    i2 = int(end * abf.sampleRate)
    subtracted = abf.sweepY - baseline
    return np.mean(subtracted[i1:i2])


def getCurveIndexes(sweep: np.ndarray, antipeakIndex: int, baselineMean: float,
                    curveEndFraction: float = .05) -> Tuple[int, int]:
    antipeakLevel = sweep[antipeakIndex]
    deltaLevel = abs(antipeakLevel - baselineMean)
    cutoffLevel = baselineMean - curveEndFraction * deltaLevel
    curveStartIndex = antipeakIndex
    curveEndIndex = antipeakIndex
    while (curveEndIndex < len(sweep) - 1):
        if sweep[curveEndIndex] >= cutoffLevel:
            break
        else:
            curveEndIndex += 1
    return (curveStartIndex, curveEndIndex)


def monoExp(x, m, t, b):
    return m * np.exp(-t * x) + b


def measureTau(abf: pyabf.ABF, sweep: int, epoch: int = 3,
               percentile: float = .05, ax: plt.Axes = None):

    abf.setSweep(sweep)

    # use epoch table to determine puff times
    puffTimeStart = abf.sweepEpochs.p1s[epoch] / abf.sampleRate
    puffTimeEnd = abf.sweepEpochs.p2s[epoch] / abf.sampleRate

    # calculate baseline level
    baselineStart = puffTimeStart - .1
    baselineEnd = puffTimeStart
    baselineMean = getMean(abf, baselineStart, baselineEnd)

    # find antipeak
    antipeakIndex = getAntiPeakIndex(
        abf.sweepY, abf.sampleRate, puffTimeStart, puffTimeStart + .5)
    antipeakLevel = abf.sweepY[antipeakIndex]

    # find portion of curve to fit
    curveIndex1, curveIndex2 = getCurveIndexes(
        abf.sweepY, antipeakIndex, baselineMean, percentile)
    curveYs = -abf.sweepY[curveIndex1:curveIndex2]
    curveXs = np.arange(len(curveYs)) / abf.sampleRate

    try:
        p0 = (500, 15, 0)  # start with values near those we expect
        params, cv = scipy.optimize.curve_fit(monoExp, curveXs, curveYs, p0)
    except:
        print(f"FIT FAILED (sweep {sweep})")
        return None
    m, t, b = params
    curveYsIdeal = monoExp(curveXs, m, t, b)
    tauMS = 1000 / t
    if (tauMS < 0):
        return None

    if ax:
        yPad = abs(antipeakLevel - baselineMean) * .1
        ax.plot(abf.sweepX, abf.sweepY, alpha=.5)
        ax.grid(alpha=.5, ls='--')
        ax.axhline(baselineMean, ls='--', color='k')
        ax.plot(abf.sweepX[curveIndex1:curveIndex2], -curveYsIdeal, color='k')
        ax.set(title=f"first sweep tau = {tauMS:.02f} ms")
        ax.axis([baselineStart - .1, baselineStart + 1,
                antipeakLevel-yPad, baselineMean+yPad])
        ax.axvspan(puffTimeEnd, puffTimeEnd+.5, color='g', alpha=.1)
        ax.axvspan(puffTimeEnd+.5, puffTimeEnd+.6, color='m', alpha=.1)

    return tauMS


def plotTauBySweep(abf: pyabf.ABF, ax: matplotlib.axes.Axes):
    times = abf.sweepTimesMin
    taus = [measureTau(abf, x) for x in range(abf.sweepCount)]
    ax.plot(times, taus, '.-', color='k')
    ax.set_ylabel("tau (ms)")
    ax.set_xlabel("Time (minutes)")
    ax.grid(alpha=.5, ls='--')
    addTagLines(abf, ax)


def plotAreaBySweep(abf: pyabf.ABF, ax: matplotlib.axes.Axes, epoch: int = 3):

    puffTimeStart = abf.sweepEpochs.p1s[epoch] / abf.sampleRate
    puffTimeEnd = abf.sweepEpochs.p2s[epoch] / abf.sampleRate

    baselineStart = puffTimeStart - .1
    baselineEnd = puffTimeStart
    baselineMean = getMean(abf, baselineStart, baselineEnd)

    values = []
    for i in range(abf.sweepCount):
        abf.setSweep(i)
        mean = getMean(abf, puffTimeEnd, puffTimeEnd+.5, baselineMean)
        values.append(mean)

    ax.plot(abf.sweepTimesMin, values, '.-', color='g')
    ax.set_ylabel("Mean pA over 1s")
    ax.set_xlabel("Time (minutes)")
    ax.grid(alpha=.5, ls='--')
    addTagLines(abf, ax)


def plotTimeAfterBySweep(abf: pyabf.ABF, ax: matplotlib.axes.Axes, epoch: int = 3):

    puffTimeStart = abf.sweepEpochs.p1s[epoch] / abf.sampleRate
    puffTimeEnd = abf.sweepEpochs.p2s[epoch] / abf.sampleRate

    baselineStart = puffTimeStart - .1
    baselineEnd = puffTimeStart
    baselineMean = getMean(abf, baselineStart, baselineEnd)

    values = []
    for i in range(abf.sweepCount):
        abf.setSweep(i)
        mean = getMean(abf, puffTimeEnd+.5, puffTimeEnd+.6, baselineMean)
        values.append(mean)

    ax.plot(abf.sweepTimesMin, values, '.-', color='m')
    ax.set_ylabel("pA after 1s")
    ax.set_xlabel("Time (minutes)")
    ax.grid(alpha=.5, ls='--')
    addTagLines(abf, ax)


def addTagLines(abf: pyabf.ABF, ax: matplotlib.axes.Axes):
    for tagTime in abf.tagTimesMin:
        print(tagTime)
        ax.axvline(tagTime, linewidth=2, color='r', alpha=.5, linestyle='--')


def tau(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    fig, axs = plt.subplots(2, 2, figsize=(8, 6))
    measureTau(abf, 0, ax=axs[0, 0])
    plotTauBySweep(abf, axs[0, 1])
    plotAreaBySweep(abf, axs[1, 0])
    plotTimeAfterBySweep(abf, axs[1, 1])

    #plt.plot(abf.sweepX, abf.sweepY)
