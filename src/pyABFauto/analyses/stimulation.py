"""
????????????????????????????
"""

import pyabf
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


def figureTestElectricalResponse(abf, fig, stimEpochNumber=3):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    optoPointOn = abf.sweepEpochs.p1s[stimEpochNumber]
    optoPointOff = abf.sweepEpochs.p2s[stimEpochNumber]

    optoTimeOn = optoPointOn * abf.dataSecPerPoint
    optoTimeOff = optoPointOff * abf.dataSecPerPoint

    dataPadSec = 0.1
    dataPadPoints = int(dataPadSec * abf.dataRate)
    displayPoint1 = int(optoPointOn - dataPadPoints)
    displayPoint2 = int(optoPointOff + dataPadPoints)

    baseline = [optoTimeOn - dataPadSec, optoTimeOn - dataPadSec/2]

    plt.title("Electrical Response (%d sweeps)" % abf.sweepCount)
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
    plt.axis([None, None, -100, 100])