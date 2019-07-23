"""
????????????????????????????
"""

import pyabf
import pyabf.tools

import pyABFauto

import matplotlib.pyplot as plt
import numpy as np


def getMeanSweep(abf, baseline=None):
    assert isinstance(abf, pyabf.ABF)
    meanSweep = np.zeros(len(abf.sweepY))
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, baseline=baseline)
        meanSweep += abf.sweepY
    meanSweep /= abf.sweepCount
    return meanSweep


def figureTestOptoResponse(abf, fig, optoEpochNumber=3):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    optoPointOn = abf.sweepEpochs.p1s[optoEpochNumber]
    optoPointOff = abf.sweepEpochs.p2s[optoEpochNumber]

    optoTimeOn = optoPointOn * abf.dataSecPerPoint
    optoTimeOff = optoPointOff * abf.dataSecPerPoint

    dataPadSec = 0.2
    dataPadPoints = int(dataPadSec * abf.dataRate)
    displayPoint1 = int(optoPointOn - dataPadPoints)
    displayPoint2 = int(optoPointOff + dataPadPoints)
    plt.title("Optogenetic Response (%d sweeps)" % abf.sweepCount)

    baseline = [optoTimeOn - dataPadSec, optoTimeOn]

    plt.subplot(211)
    plt.title("Stacked Sweeps")
    yOffset = 100
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, baseline=baseline)
        plt.plot(abf.sweepX[displayPoint1:displayPoint2],
                 abf.sweepY[displayPoint1:displayPoint2] + sweepNumber*yOffset,
                 color='b')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)
    plt.axvspan(optoTimeOn, optoTimeOff, color='y', edgecolor='y')

    plt.subplot(212)
    plt.title("Average Sweep")
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, baseline=baseline)
        plt.plot(abf.sweepX[displayPoint1:displayPoint2],
                 abf.sweepY[displayPoint1:displayPoint2],
                 alpha=.2, color='.5')
    meanSweep = getMeanSweep(abf, baseline=baseline)
    plt.plot(abf.sweepX[displayPoint1:displayPoint2],
             meanSweep[displayPoint1:displayPoint2],
             color='b')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)
    plt.axvspan(optoTimeOn, optoTimeOff, alpha=.5, color='y', edgecolor='y')


def figureTestElectricalResponseVC(abf, fig, stimEpochNumber=3):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)
    
    mt = pyabf.tools.Memtest(abf)

    optoPointOn = abf.sweepEpochs.p1s[stimEpochNumber]
    optoPointOff = abf.sweepEpochs.p2s[stimEpochNumber]

    optoTimeOn = optoPointOn * abf.dataSecPerPoint
    optoTimeOff = optoPointOff * abf.dataSecPerPoint

    displayPoint1 = int(optoPointOn - 0.03 * abf.dataRate)
    displayPoint2 = int(optoPointOff + 0.05 * abf.dataRate)

    baseline = [optoTimeOn - .02, optoTimeOn - .01]

    measure = [optoTimeOff + .003, optoTimeOff + .015]
    measureI1 = int(measure[0] * abf.dataRate)
    measureI2 = int(measure[1] * abf.dataRate)
    means = np.full(abf.sweepCount, np.nan)

    plt.subplot(221)
    fig.grid()
    plt.title("Electrical Response (%d sweeps)" % abf.sweepCount)
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, baseline=baseline)
        means[sweepNumber] = np.mean(abf.sweepY[measureI1:measureI2])
        plt.plot(abf.sweepX[displayPoint1:displayPoint2],
                 abf.sweepY[displayPoint1:displayPoint2],
                 alpha=.2, color='.5')
    meanSweep = getMeanSweep(abf, baseline=baseline)
    plt.plot(abf.sweepX[displayPoint1:displayPoint2],
             meanSweep[displayPoint1:displayPoint2],
             color='b')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)
    plt.axvspan(optoTimeOn, optoTimeOff, alpha=.5, color='y')
    plt.axvspan(baseline[0], baseline[1], alpha=.2, color='k')
    plt.axvspan(measure[0], measure[1], alpha=.2, color='r')
    plt.axis([None, None, -100, 100])

    plt.subplot(222)
    fig.grid()
    plt.title("Evoked Current")
    plt.axhline(0, color='k', ls='--')
    sweepTimesSec = np.arange(abf.sweepCount) * abf.sweepIntervalSec
    sweepTimesMin = sweepTimesSec / 60
    plt.plot(sweepTimesMin, means, '.-')
    fig.addTagLines(minutes=True)
    plt.ylabel("Evoked Current (pA)")
    plt.xlabel("Experiment Time (minutes)")
    plt.margins(.1, .3)

    plt.subplot(223)
    fig.grid()
    plt.title(mt.Ih.name)
    plt.ylabel(mt.Ih.units)
    plt.xlabel("Experiment Time (minutes)")
    plt.plot(mt.Ih.values, '.-')
    plt.margins(.1, .3)
    fig.addTagLines(minutes=True)

    plt.subplot(224)
    fig.grid()
    plt.title(mt.Ra.name)
    plt.ylabel(mt.Ra.units)
    plt.xlabel("Experiment Time (minutes)")
    plt.plot(mt.Ra.values, '.-')
    fig.addTagLines(minutes=True)
    plt.margins(.1, .3)
    plt.axis([None, None, 0, None])