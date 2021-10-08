from typing import Tuple
import pyabf
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import matplotlib.pyplot as plt


def getAntiPeakIndex(sweep: np.ndarray, sampleRate: int, start: float, end: float) -> int:
    i1 = int(start * sampleRate)
    i2 = int(end * sampleRate)
    segment = sweep[i1:i2]
    minIndex = np.argmin(segment)
    return minIndex + i1


def getMean(sweep: np.ndarray, sampleRate: int, start: float, end: float) -> float:
    i1 = int(start * sampleRate)
    i2 = int(end * sampleRate)
    return np.mean(sweep[i1:i2])


def getCurveIndexes(sweep: np.ndarray, sampleRate: int, antiPeakIndex: int, baselineMean: float,
                    curveEndFraction: float = .2) -> Tuple[int, int]:
    deltaLevel = abs(antipeakLevel - baselineMean)
    tenPercentileLevel = baselineMean - .1 * deltaLevel
    tenPercentileIndex = antipeakIndex
    while (tenPercentileIndex < len(sweep) - 1):
        if sweep[tenPercentileIndex] >= tenPercentileLevel:
            break
        else:
            tenPercentileIndex += 1
    return (antiPeakIndex, tenPercentileIndex)


def monoExp(x, m, t, b):
    return m * np.exp(-t * x) + b


if __name__ == "__main__":
    abfFilePath = "X:/Data/Alchem/Physostigmine/10-08-2021/2021_10_08_DIC1_0003.abf"
    abf = pyabf.ABF(abfFilePath)
    plt.plot(abf.sweepX, abf.sweepY, alpha=.7)
    plt.grid(alpha=.5, ls='--')

    # use epoch table to determine puff times
    puffTimeStart = abf.sweepEpochs.p1s[3] / abf.sampleRate
    puffTimeEnd = abf.sweepEpochs.p2s[3] / abf.sampleRate
    plt.axvspan(puffTimeStart, puffTimeEnd, color='r', alpha=.2)

    # calculate baseline level
    baselineStart = puffTimeStart - .1
    baselineEnd = puffTimeStart
    baselineMean = getMean(abf.sweepY, abf.sampleRate,
                           baselineStart, baselineEnd)
    plt.axvspan(baselineStart, baselineEnd, alpha=.2)
    plt.axhline(baselineMean, ls='--', color='k')

    # find antipeak
    antipeakIndex = getAntiPeakIndex(
        abf.sweepY, abf.sampleRate, puffTimeStart, puffTimeStart + .5)
    antipeakTime = antipeakIndex / abf.sampleRate
    antipeakLevel = abf.sweepY[antipeakIndex]

    # find portion of curve to fit
    curveIndex1, curveIndex2 = getCurveIndexes(
        abf.sweepY, abf.sampleRate, antipeakIndex, baselineMean)
    plt.axvspan(abf.sweepX[curveIndex1],
                abf.sweepX[curveIndex2], color='g', alpha=.2)

    curveYs = -abf.sweepY[curveIndex1:curveIndex2]
    curveXs = np.arange(len(curveYs)) / abf.sampleRate

    p0 = (2000, .1, 50)  # start with values near those we expect
    params, cv = scipy.optimize.curve_fit(monoExp, curveXs, curveYs, None)
    m, t, b = params
    curveYsIdeal = monoExp(curveXs, m, t, b)
    tauMS = 1000 / t
    plt.plot(abf.sweepX[curveIndex1:curveIndex2], -curveYsIdeal, color='k')
    plt.title(f"tau = {tauMS:.02f} ms")

    plt.axis([baselineStart - .1, baselineStart + 1, None, None])
    plt.show()
