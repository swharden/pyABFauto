
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
        times = [t for t in times if t>=timeStart and t<=timeEnd]
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
