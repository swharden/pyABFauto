
import pyabf
import pyabf.filter
import pyABFauto
import pyABFauto.figure

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize


def expAssoc(x, y0, plateau, K):
    return y0 + (plateau - y0) * (1 - np.exp(-K*x))


def showRamp(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyabf.filter.gaussian(abf, 3)

    cmap = matplotlib.colormaps["turbo"]
    colors = [cmap(x/abf.sweepCount) for x in range(abf.sweepCount)]

    measureTime = 9.79779
    measurePoint = int(9.79779 * abf.dataRate)
    baselineRange = [13.5, 14.5]

    plt.subplot(221)
    for i in range(abf.sweepCount):
        abf.setSweep(i)
        plt.plot(abf.sweepX, abf.sweepY, color=colors[i])
    plt.title(abf.abfID + ".abf")
    plt.ylabel("Current (pA)")
    plt.xlabel("Time (seconds)")
    plt.margins(0, .1)
    plt.axvline(measureTime, color='r', ls='--', alpha=.5)
    plt.axvspan(baselineRange[0], baselineRange[1], alpha=.2, color='r')

    plt.subplot(222)
    for i in range(abf.sweepCount):
        abf.setSweep(i, baseline=baselineRange)
        plt.plot(abf.sweepX, abf.sweepY, color=colors[i])
    plt.title("Ramp")
    plt.ylabel("Current (pA)")
    plt.xlabel("Time (seconds)")
    plt.margins(0, .1)
    plt.axis([9, 11, None, None])
    plt.axvline(measureTime, color='r', ls='--', alpha=.5)

    plt.subplot(223)
    for i in range(abf.sweepCount):
        abf.setSweep(i, baseline=baselineRange)
        i1 = int(measurePoint - abf.dataRate * .02)
        i2 = int(measurePoint + abf.dataRate * .02)
        xs = abf.sweepX[i1:i2]
        ys = abf.sweepY[i1:i2]
        plt.plot(xs, ys, color=colors[i])
    plt.title("Current at -20 mV")
    plt.ylabel("Current (pA)")
    plt.xlabel("Time (seconds)")
    plt.margins(0, .1)
    plt.axvline(measureTime, color='r', ls='--', alpha=.5)

    plt.subplot(224)
    xs = [.025 + .25 * x for x in range(abf.sweepCount)]
    ys = [None] * abf.sweepCount
    for i in range(abf.sweepCount):
        abf.setSweep(i, baseline=baselineRange)
        ys[i] = abf.sweepY[measurePoint]
        plt.plot(xs[i], ys[i], '.', ms=15, color=colors[i])
    plt.xlabel("Δt (sec)")
    plt.ylabel("Current (pA)")

    p0 = (ys[0], ys[-1], 1)  # start with values near those we expect
    params, cv = scipy.optimize.curve_fit(expAssoc, xs, ys, p0)
    y0, plateau, K = params
    span = plateau - y0
    tau = 1 / K

    xs2 = np.arange(0, 4, .1)
    ys2 = [expAssoc(x, y0, plateau, K) for x in xs2]
    plt.plot(xs2, ys2, color='k', ls='--')
    plt.title(f"Span = {span:.02f} pA, τ = {tau:.02f} sec")

    plt.tight_layout()
