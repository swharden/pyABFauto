"""
????????????????????????????
"""

import pyabf
import pyabf.tools
import pyabf.tools.memtest
import pyabf.filter

import pyABFauto

import matplotlib.pyplot as plt
import numpy as np


def optoResponse(abf, fig, optoEpochNumber=3):
    if abf.sweepUnitsY == "pA" and abf.dataLengthMin > 5:
        figureShowOptoResponseOverTime(abf, fig, optoEpochNumber)
    else:
        figureTestOptoResponse(abf, fig, optoEpochNumber)
    pass


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
    optoDuration = optoTimeOff - optoTimeOn

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
    plt.axvspan(optoTimeOn, optoTimeOff, alpha=.5, color='y')

    plt.subplot(212)

    optoPeriod = abf.sweepEpochs.pulsePeriods[optoEpochNumber] / abf.dataRate
    if (optoPeriod == 0):
        optoPeriod = 1
    optoHz = 1 / optoPeriod
    optoDur = abf.sweepEpochs.pulseWidths[optoEpochNumber] / \
        abf.dataRate * 1000

    plt.title(f"Average Sweep ({optoHz}Hz of {optoDur}ms pulses)")
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
    plt.axvspan(optoTimeOn, optoTimeOff, alpha=.5, color='y')


def shadeEpochs(abf: pyabf.ABF, fig: pyABFauto.figure.Figure, epochs: list[int], color: str = 'y'):
    plt.plot(abf.sweepX, abf.sweepY, color='b')
    for epoch in epochs:
        t1 = abf.sweepEpochs.p1s[epoch] * abf.dataSecPerPoint
        t2 = abf.sweepEpochs.p2s[epoch] * abf.dataSecPerPoint
        plt.axvspan(t1, t2, alpha=.5, color=color)
    plt.grid(alpha=.5, ls='--')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)


def figureShowOptoResponseOverTime(abf, fig, optoEpochNumber=3):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    mt = pyabf.tools.memtest.Memtest(abf)

    optoPointOn = abf.sweepEpochs.p1s[optoEpochNumber]
    optoPointOff = abf.sweepEpochs.p2s[optoEpochNumber]

    optoTimeOn = optoPointOn * abf.dataSecPerPoint
    optoTimeOff = optoPointOff * abf.dataSecPerPoint

    dataPadSec = 0.2
    dataPadPoints = int(dataPadSec * abf.dataRate)
    displayPoint1 = int(optoPointOn - dataPadPoints)
    displayPoint2 = int(optoPointOff + dataPadPoints)
    plt.title("Optogenetic Response (%d sweeps)" % abf.sweepCount)

    baseline = [optoTimeOn - .1, optoTimeOn - .05]

    measure = [optoTimeOn, optoTimeOn + .02]
    measureI1 = int(measure[0] * abf.dataRate)
    measureI2 = int(measure[1] * abf.dataRate)
    means = np.full(abf.sweepCount, np.nan)

    sweepTimesSec = np.arange(abf.sweepCount) * abf.sweepIntervalSec
    sweepTimesMin = sweepTimesSec / 60

    plt.subplot(221)
    plt.title("Average Sweep")
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

    plt.subplot(222)
    fig.grid()
    plt.title("Evoked Current")
    plt.axhline(0, color='k', ls='--')
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
    plt.plot(sweepTimesMin, mt.Ih.values, '.-')
    plt.margins(.1, .3)
    fig.addTagLines(minutes=True)

    plt.subplot(224)
    fig.grid()
    plt.title(mt.Ra.name)
    plt.ylabel(mt.Ra.units)
    plt.xlabel("Experiment Time (minutes)")
    plt.plot(sweepTimesMin, mt.Ra.values, '.-')
    fig.addTagLines(minutes=True)
    plt.margins(.1, .3)
    plt.axis([None, None, 0, None])


def figureTestElectricalResponseVC(abf, fig, stimEpochNumber=3, measureOffset1=.003, measureOffset2=.015):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    mt = pyabf.tools.memtest.Memtest(abf)

    optoPointOn = abf.sweepEpochs.p1s[stimEpochNumber]
    optoPointOff = abf.sweepEpochs.p2s[stimEpochNumber]

    optoTimeOn = optoPointOn * abf.dataSecPerPoint
    optoTimeOff = optoPointOff * abf.dataSecPerPoint

    displayPoint1 = int(optoPointOn - 0.03 * abf.dataRate)
    displayPoint2 = int(optoPointOff + 0.05 * abf.dataRate)

    baseline = [optoTimeOn - .02, optoTimeOn - .01]

    measure = [optoTimeOff + measureOffset1, optoTimeOff + measureOffset2]
    measureI1 = int(measure[0] * abf.dataRate)
    measureI2 = int(measure[1] * abf.dataRate)
    means = np.full(abf.sweepCount, np.nan)

    sweepTimesSec = np.arange(abf.sweepCount) * abf.sweepIntervalSec
    sweepTimesMin = sweepTimesSec / 60

    plt.subplot(221)
    fig.grid()
    plt.title("Electrical Response (%d sweeps)" % abf.sweepCount)
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, baseline=baseline)
        means[sweepNumber] = np.mean(abf.sweepY[measureI1:measureI2])
        plt.plot(abf.sweepX[displayPoint1:displayPoint2],
                 abf.sweepY[displayPoint1:displayPoint2],
                 alpha=.4, color='b')
    # meanSweep = getMeanSweep(abf, baseline=baseline)
    # plt.plot(abf.sweepX[displayPoint1:displayPoint2],
        # meanSweep[displayPoint1:displayPoint2],
        # color='b')
    plt.axhline(0, color='k', ls='--')
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
    plt.plot(sweepTimesMin, mt.Ih.values, '.-')
    plt.margins(.1, .3)
    fig.addTagLines(minutes=True)

    plt.subplot(224)
    fig.grid()
    plt.title(mt.Ra.name)
    plt.ylabel(mt.Ra.units)
    plt.xlabel("Experiment Time (minutes)")
    plt.plot(sweepTimesMin, mt.Ra.values, '.-')
    fig.addTagLines(minutes=True)
    plt.margins(.1, .3)
    plt.axis([None, None, 0, None])


def figureTestElectricalResponseIC(abf: pyabf.ABF, fig: pyABFauto.figure.Figure, stimEpochNumber: int = 3):

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

    sweepTimesSec = np.arange(abf.sweepCount) * abf.sweepIntervalSec
    sweepTimesMin = sweepTimesSec / 60

    plt.subplot(121)
    fig.grid()
    plt.title("Electrical Response (%d sweeps)" % abf.sweepCount)
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, baseline=baseline)
        means[sweepNumber] = np.mean(abf.sweepY[measureI1:measureI2])
        plt.plot(abf.sweepX[displayPoint1:displayPoint2],
                 abf.sweepY[displayPoint1:displayPoint2],
                 alpha=.4, color='b')
    # meanSweep = getMeanSweep(abf, baseline=baseline)
    # plt.plot(abf.sweepX[displayPoint1:displayPoint2],
        # meanSweep[displayPoint1:displayPoint2],
        # color='b')
    plt.axhline(0, color='k', ls='--')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)
    plt.axvspan(optoTimeOn, optoTimeOff, alpha=.5, color='y')
    plt.axvspan(baseline[0], baseline[1], alpha=.2, color='k')
    plt.axvspan(measure[0], measure[1], alpha=.2, color='r')
    plt.axis([None, None, -100, 100])

    plt.subplot(122)
    fig.grid()
    plt.title("Evoked Current")
    plt.axhline(0, color='k', ls='--')
    plt.plot(sweepTimesMin, means, '.-')
    fig.addTagLines(minutes=True)
    plt.ylabel("Evoked Current (mV)")
    plt.xlabel("Experiment Time (minutes)")
    plt.margins(.1, .3)


def figureTestElectricalTrainVC(abf, fig, stimEpochNumber=3):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    mt = pyabf.tools.memtest.Memtest(abf)

    optoPointOn = abf.sweepEpochs.p1s[stimEpochNumber]
    optoTimeOn = optoPointOn * abf.dataSecPerPoint
    optoPointOff = abf.sweepEpochs.p2s[stimEpochNumber]
    optoTimeOff = optoPointOff * abf.dataSecPerPoint
    baseline = [optoTimeOn - .02, optoTimeOn - .01]

    displayPoint1 = int(optoPointOn - 0.03 * abf.dataRate)
    displayPoint2 = displayPoint1 + int(0.3 * abf.dataRate)

    sweepTimesSec = np.arange(abf.sweepCount) * abf.sweepIntervalSec
    sweepTimesMin = sweepTimesSec / 60

    plt.subplot(221)
    fig.grid()
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
    plt.axvspan(optoTimeOn, optoTimeOff, alpha=.5, color='y')
    plt.axvspan(baseline[0], baseline[1], alpha=.2, color='k')
    plt.axis([None, optoTimeOn + .05, -100, 100])

    plt.subplot(222)
    fig.grid()
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
    plt.axvspan(optoTimeOn, optoTimeOff, alpha=.5, color='y')
    plt.axvspan(baseline[0], baseline[1], alpha=.2, color='k')
    plt.axis([None, None, -100, 100])

    plt.subplot(223)
    fig.grid()
    plt.title(mt.Ih.name)
    plt.ylabel(mt.Ih.units)
    plt.xlabel("Experiment Time (minutes)")
    plt.plot(sweepTimesMin, mt.Ih.values, '.-')
    plt.margins(.1, .3)
    fig.addTagLines(minutes=True)

    plt.subplot(224)
    fig.grid()
    plt.title(mt.Ra.name)
    plt.ylabel(mt.Ra.units)
    plt.xlabel("Experiment Time (minutes)")
    plt.plot(sweepTimesMin, mt.Ra.values, '.-')
    fig.addTagLines(minutes=True)
    plt.margins(.1, .3)
    plt.axis([None, None, 0, None])


def figureVariedPulseTime(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    epoch = 3
    stimTimeStart = abf.sweepEpochs.p1s[epoch] / abf.sampleRate
    viewIndex1 = int((stimTimeStart-.1) * abf.sampleRate)
    viewIndex2 = int((stimTimeStart+.2) * abf.sampleRate)
    plt.axhline(0, color='k', ls='--')

    pyabf.filter.gaussian(abf, 1)
    plt.grid(alpha=.5, ls='--')
    for sweepIndex in range(abf.sweepCount):
        abf.setSweep(sweepIndex, baseline=[stimTimeStart-.1, stimTimeStart])
        xs = abf.sweepX[viewIndex1:viewIndex2]
        ys = abf.sweepY[viewIndex1:viewIndex2]
        plt.plot(xs, ys, alpha=.5, color='b')

    plt.ylabel("Δ Current (pA)")
    plt.xlabel("Time (seconds)")
    plt.margins(0, .1)


def shadeEpoch(abf: pyabf.ABF, epochIndex: int, color: str):
    t1 = abf.sweepEpochs.p1s[epochIndex] / abf.sampleRate
    t2 = abf.sweepEpochs.p2s[epochIndex] / abf.sampleRate
    plt.axvspan(t1, t2, alpha=.2, color=color)


def swichr(abf: pyabf.ABF, fig: pyABFauto.figure.Figure, blueEpoch: int, redEpoch: int):

    plt.grid(alpha=.5, ls='--')
    shadeEpoch(abf, blueEpoch, 'b')
    shadeEpoch(abf, redEpoch, 'r')

    for sweepIndex in range(abf.sweepCount):
        abf.setSweep(sweepIndex)
        plt.plot(abf.sweepX, abf.sweepY, color='b')

    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)


def swichrStacked(abf: pyabf.ABF, fig: pyABFauto.figure.Figure, blueEpoch: int, redEpoch: int, stackDelta: float):

    plt.grid(alpha=.5, ls='--')
    shadeEpoch(abf, blueEpoch, 'b')
    shadeEpoch(abf, redEpoch, 'r')

    pyabf.filter.gaussian(abf, 10)

    for sweepIndex in range(abf.sweepCount):
        abf.setSweep(sweepIndex)
        ys = abf.sweepY + sweepIndex * stackDelta
        ys[:abf.sweepEpochs.p2s[blueEpoch - 2]] = np.nan
        plt.plot(abf.sweepX, ys, color='b', lw=.5)

    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)


def bpAP(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    for sweepIndex in range(abf.sweepCount):
        abf.setSweep(sweepIndex)
        plt.plot(abf.sweepX, abf.sweepY, color='b', lw=.5)
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)
    plt.grid(alpha=.5, ls='--')


def uncaging(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    uncagingEpoch = 5
    uncagingIndex = abf.sweepEpochs.p1s[uncagingEpoch]
    uncagingTime = uncagingIndex / abf.sampleRate
    viewStart = uncagingTime - .5
    viewEnd = uncagingTime + 1
    viewStartIndex = int(viewStart * abf.sampleRate)
    viewEndIndex = int(viewEnd * abf.sampleRate)

    # show everything
    plt.subplot(211)
    for sweepIndex in range(abf.sweepCount):
        abf.setSweep(sweepIndex)
        plt.plot(abf.sweepX, abf.sweepY, color='b', lw=.5)
    plt.axvline(uncagingTime, color='r', ls='--')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)
    plt.grid(alpha=.5, ls='--')

    # show uncaging point
    plt.subplot(212)
    for sweepIndex in range(abf.sweepCount):
        abf.setSweep(sweepIndex)
        ys = abf.sweepY[viewStartIndex:viewEndIndex]
        xs = abf.sweepX[viewStartIndex:viewEndIndex]
        plt.plot(xs, ys, color='b', lw=.5, alpha=.5)
    plt.axvline(uncagingTime, color='r', ls='--')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.margins(0, .1)
    plt.grid(alpha=.5, ls='--')


def getAverageOfSweeps(abf: pyabf.abf, baseline: list[int], sweeps: list[int], i1: int, i2: int):
    sweep_count = len(sweeps)
    point_count = i2 - i1
    data = np.empty((sweep_count, point_count))
    for i, sweep in enumerate(sweeps):
        abf.setSweep(sweep, baseline=baseline)
        data[i, :] = abf.sweepY[i1:i2]
    mean = np.mean(data, axis=0)
    return mean


def figurePPR(abf: pyabf.ABF, fig: pyABFauto.figure.Figure, stimEpochNumber=3):

    mt = pyabf.tools.memtest.Memtest(abf)

    optoPointOn = abf.sweepEpochs.p1s[stimEpochNumber]
    optoPointOff = abf.sweepEpochs.p2s[stimEpochNumber]

    optoTimeOn = optoPointOn * abf.dataSecPerPoint
    optoTimeOff = optoPointOff * abf.dataSecPerPoint

    displayPoint1 = int(optoPointOn - 0.03 * abf.dataRate)
    displayPoint2 = displayPoint1 + int(.15 * abf.dataRate)

    baseline = [optoTimeOn - .02, optoTimeOn - .01]

    measureOffset1 = .003
    measureOffset2 = .015
    measure = [optoTimeOff + measureOffset1, optoTimeOff + measureOffset2]
    measureI1 = int(measure[0] * abf.dataRate)
    measureI2 = int(measure[1] * abf.dataRate)

    sweepTimesSec = np.arange(abf.sweepCount) * abf.sweepIntervalSec
    sweepTimesMin = sweepTimesSec / 60

    p1_i1 = int(abf.sweepEpochs.p1s[3] + .005 * abf.dataRate)
    p1_i2 = int(abf.sweepEpochs.p1s[3] + .035 * abf.dataRate)
    p2_i1 = int(abf.sweepEpochs.p1s[5] + .005 * abf.dataRate)
    p2_i2 = int(abf.sweepEpochs.p1s[5] + .035 * abf.dataRate)

    pyabf.filter.gaussian(abf, .25)
    plt.subplot(221)

    average_sweep_count = abf.sweepCount // 5
    baseline_sweeps = range(average_sweep_count)
    drug_sweeps = range(abf.sweepCount - 1 - average_sweep_count,
                        abf.sweepCount - 1)

    segment_xs = abf.sweepX[displayPoint1:displayPoint2]

    baseline_ys = getAverageOfSweeps(abf, baseline, baseline_sweeps,
                                     displayPoint1, displayPoint2)

    drug_ys = getAverageOfSweeps(abf, baseline, drug_sweeps,
                                 displayPoint1, displayPoint2)

    for epoch in [3, 5]:
        blank1 = abf.sweepEpochs.p1s[epoch] - displayPoint1 - 10
        blank2 = blank1 + 40
        baseline_ys[blank1:blank2] = np.NaN
        drug_ys[blank1:blank2] = np.NaN

    plt.plot(segment_xs, baseline_ys,
             label=f"baseline (n={average_sweep_count})")
    plt.plot(segment_xs, drug_ys,
             label=f"drug (n={average_sweep_count})")
    plt.legend(fontsize=8)
    plt.axhline(0, color='k', ls='--')
    fig.grid()

    plt.subplot(222)

    means1 = np.full(abf.sweepCount, np.nan)
    means2 = np.full(abf.sweepCount, np.nan)

    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, baseline=baseline)
        means1[sweepNumber] = np.mean(abf.sweepY[p1_i1:p1_i2])
        means2[sweepNumber] = np.mean(abf.sweepY[p2_i1:p2_i2])

    plt.scatter(sweepTimesMin, means1, s=40,
                facecolors='k', edgecolors='k', label="pulse 1")
    plt.scatter(sweepTimesMin, means2, s=40,
                facecolors='w', edgecolors='k', label="pulse 2")

    plt.legend(fontsize=8)

    fig.addTagLines(minutes=True)
    fig.grid()
    plt.axhline(0, color='k', ls='--')
    plt.ylabel("Mean Current (pA)")
    plt.xlabel("Time (minutes)")
    plt.margins(.1, .3)

    plt.subplot(223)
    fig.grid()
    plt.title(mt.Ih.name)
    plt.ylabel("MΩ")
    plt.xlabel("Time (minutes)")
    plt.plot(sweepTimesMin, mt.Ih.values, '.-')
    plt.margins(.1, .3)
    fig.addTagLines(minutes=True)

    plt.subplot(224)
    fig.grid()
    plt.title(mt.Ra.name)
    plt.ylabel(mt.Ra.units)
    plt.xlabel("Time (minutes)")
    plt.plot(sweepTimesMin, mt.Ra.values, '.-')
    fig.addTagLines(minutes=True)
    plt.margins(.1, .3)
    plt.axis([None, None, 0, None])
