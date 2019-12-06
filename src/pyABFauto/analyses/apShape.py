import pyabf
import pyabf.tools
import pyabf.tools.ap

import pyABFauto
import pyABFauto.figure

import matplotlib.pyplot as plt
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
    plt.xlabel("ms")
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
    plt.xlabel("ms")
