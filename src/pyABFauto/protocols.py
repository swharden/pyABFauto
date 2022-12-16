"""
Code in this file defines how ABFs are analyzed by their protocol identifier. 
Core analyses are coded in the analyses folder whenever possible.
"""

import pyabf
import pyabf.tools

import pyABFauto
import pyABFauto.analyses.memtest
import pyABFauto.analyses.iv
import pyABFauto.analyses.apShape
import pyABFauto.analyses.apGain
import pyABFauto.analyses.stimulation
import pyABFauto.analyses.dsi
import pyABFauto.analyses.timeCourse
import pyABFauto.analyses.jeff
import pyABFauto.analyses.unknown
import pyABFauto.analyses.amy
import pyABFauto.analyses.freq
import pyABFauto.analyses.todd


def warnIfBadUnits(abf: pyabf.ABF):
    if (abf.adcUnits[0] != "mV"):
        pyABFauto.analyses.unknown.badunits()


def analyze_0111(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apShape.firstAP(abf, fig)
    warnIfBadUnits(abf)


def analyze_1_(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):  # SS VC memtest
    pyABFauto.analyses.apShape.firstAP(abf, fig)


def analyze_5(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):  # 5 ramp gain
    pyABFauto.analyses.apShape.firstAP(abf, fig)


def analyze_0110(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apGain.restPotential(abf, fig)
    warnIfBadUnits(abf)


def analyze_0112(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apGain.doubleStep(abf, fig, .14, .65, 1.64, 2.15)
    warnIfBadUnits(abf)


def analyze_0113(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apGain.doubleStep(abf, fig, .14, .65, 1.64, 2.15)
    warnIfBadUnits(abf)


def analyze_0114(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apGain.doubleStep(abf, fig, .14, .65, 1.64, 2.15)
    warnIfBadUnits(abf)


def analyze_0115(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apGain.singleStep(abf, fig, .54685, 1.54685)
    warnIfBadUnits(abf)


def analyze_0119(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apGain.singleStep(abf, fig, 3.15631, 7.15631)
    warnIfBadUnits(abf)


def analyze_0119b(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apGain.singleStep(abf, fig, 3.15631, 7.15631)
    warnIfBadUnits(abf)


def analyze_0123(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apShape.adp(abf, fig)
    warnIfBadUnits(abf)


def analyze_0127(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apShape.adp2(abf, fig)
    warnIfBadUnits(abf)


def analyze_0128(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apShape.adp2(abf, fig)
    warnIfBadUnits(abf)


def analyze_0129(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.apShape.firstAP(abf, fig)
    warnIfBadUnits(abf)


def analyze_0130(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    fig.plotContinuous()
    fig.addTagLines()
    warnIfBadUnits(abf)


def analyze_0131(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    fig.plotContinuous()
    fig.addTagLines()
    warnIfBadUnits(abf)


def analyze_3(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):  # 3 SHIV3
    pyABFauto.analyses.apGain.singleStep(abf, fig, 1.07, 1.07+1)


def analyze_3_(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):  # 3.
    pyABFauto.analyses.apGain.singleStep(abf, fig, .14665, .14665 + .5)


def analyze_0201(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.memtest.figureMemtest(abf, fig)


def analyze_0202(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.iv.step(abf, fig, 2.3, 2.5, 2.566, 2.7)


def analyze_2_(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.iv.step(abf, fig, .8, .8 + .25, 2.566, 2.7)


def analyze_1(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):  # 1 MTIV3
    pyABFauto.analyses.iv.step(abf, fig, 1.45, 1.45 + .5, 1.07, 1.07 + .2)


def analyze_0203(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.iv.step(abf, fig, .5, .95, 2.566, 2.7)


def analyze_0301(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.timeCourse.apFreqOverTime(abf, fig)


def analyze_RestMemPotential(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.timeCourse.apFreqOverTime(abf, fig)


def analyze_0304(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.timeCourse.apFreqOverTime(abf, fig)


def analyze_0313(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.timeCourse.gradedFiring(abf, fig)


def analyze_0315(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.timeCourse.wideningStep(abf, fig)


def analyze_0401(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0402(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0403(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0404(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0405(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0406(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0422(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0423(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0425(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.amy.showRamp(abf, fig)


def analyze_6(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):  # 6 MT-mon
    analyze_0405(abf, fig)


def analyze_MT_mon_2(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):  # MT-mon_2 (SS)
    analyze_0405(abf, fig)


def analyze_EPSCs(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):  # SS
    analyze_0405(abf, fig)


def analyze_0501(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=3)


def analyze_0502(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0503(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0504(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0505(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0506(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0507(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0509(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0512(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=3)


def analyze_0513(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=3)


def analyze_0514(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=3)


def analyze_0516(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.swichr(abf, fig, 2, 4)


def analyze_0517(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.swichr(abf, fig, 3, 5)


def analyze_0518(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.swichrStacked(abf, fig, 5, 7, 100)


def analyze_0600(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.figureTestElectricalTrainVC(
        abf, fig, stimEpochNumber=3)


def analyze_0601(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.figureVariedPulseTime(abf, fig)


def analyze_0602(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.figureTestElectricalResponseVC(
        abf, fig, stimEpochNumber=3)


def analyze_0602(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.figureTestElectricalResponseVC(
        abf, fig, stimEpochNumber=3)


def analyze_0606(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.figureTestElectricalResponseIC(
        abf, fig, stimEpochNumber=2)


def analyze_0607(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.figureTestElectricalResponseVC(
        abf, fig, stimEpochNumber=4)


def analyze_0611(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.dsi.evokedInwardCurrent(abf, fig)


def analyze_0612(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.dsi.singleSweepWithProtocol(abf, fig)


def analyze_0613(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.dsi.evokedInwardCurrent(abf, fig)


def analyze_0804(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.bpAP(abf, fig)


def analyze_0807(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.uncaging(abf, fig)


def analyze_0913(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.jeff.tau(abf, fig)


def analyze_0915(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.todd.vc_ican(abf, fig)


def analyze_Signal(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):  # SS spike fidelity
    if abf.sweepUnitsY == "pA":
        pyABFauto.analyses.stimulation.optoResponse(
            abf, fig, optoEpochNumber=4)
    else:
        #pyABFauto.analyses.stimulation.figureTestElectricalResponseVC(abf, fig, stimEpochNumber=4)
        pyABFauto.analyses.timeCourse.apFreqOverTime(abf, fig)


def analyze_xxxx(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=3)


def analyze_EEG_2_Channel_Protocol(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):
    pyABFauto.analyses.freq.plotSpectrogramAndPowerOverTime(abf, fig)
