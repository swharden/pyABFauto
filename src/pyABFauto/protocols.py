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


def analyze_0111(abf, fig):
    pyABFauto.analyses.apShape.firstAP(abf, fig)


def analyze_1_(abf, fig):  # SS VC memtest
    pyABFauto.analyses.apShape.firstAP(abf, fig)


def analyze_5(abf, fig):  # 5 ramp gain
    pyABFauto.analyses.apShape.firstAP(abf, fig)


def analyze_0110(abf, fig):
    pyABFauto.analyses.apGain.restPotential(abf, fig)


def analyze_0112(abf, fig):
    pyABFauto.analyses.apGain.doubleStep(abf, fig, .14, .65, 1.64, 2.15)


def analyze_0113(abf, fig):
    pyABFauto.analyses.apGain.doubleStep(abf, fig, .14, .65, 1.64, 2.15)


def analyze_0114(abf, fig):
    pyABFauto.analyses.apGain.doubleStep(abf, fig, .14, .65, 1.64, 2.15)


def analyze_0115(abf, fig):
    pyABFauto.analyses.apGain.singleStep(abf, fig, .54685, 1.54685)


def analyze_0119(abf, fig):
    pyABFauto.analyses.apGain.singleStep(abf, fig, 3.15631, 7.15631)


def analyze_0123(abf, fig):
    pyABFauto.analyses.apShape.adp(abf, fig)


def analyze_0127(abf, fig):
    pyABFauto.analyses.apShape.adp2(abf, fig)


def analyze_3(abf, fig):  # 3 SHIV3
    pyABFauto.analyses.apGain.singleStep(abf, fig, 1.07, 1.07+1)


def analyze_3_(abf, fig):  # 3.
    pyABFauto.analyses.apGain.singleStep(abf, fig, .14665, .14665 + .5)


def analyze_0201(abf, fig):
    pyABFauto.analyses.memtest.figureMemtest(abf, fig)


def analyze_0202(abf, fig):
    pyABFauto.analyses.iv.step(abf, fig, 2.3, 2.5, 2.566, 2.7)


def analyze_2_(abf, fig):
    pyABFauto.analyses.iv.step(abf, fig, .8, .8 + .25, 2.566, 2.7)


def analyze_1(abf, fig):  # 1 MTIV3
    pyABFauto.analyses.iv.step(abf, fig, 1.45, 1.45 + .5, 1.07, 1.07 + .2)


def analyze_0203(abf, fig):
    pyABFauto.analyses.iv.step(abf, fig, .5, .95, 2.566, 2.7)


def analyze_0301(abf, fig):
    pyABFauto.analyses.timeCourse.apFreqOverTime(abf, fig)


def analyze_RestMemPotential(abf, fig):
    pyABFauto.analyses.timeCourse.apFreqOverTime(abf, fig)


def analyze_0304(abf, fig):
    pyABFauto.analyses.timeCourse.apFreqOverTime(abf, fig)


def analyze_0313(abf, fig):
    pyABFauto.analyses.timeCourse.gradedFiring(abf, fig)


def analyze_0401(abf, fig):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0402(abf, fig):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0403(abf, fig):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0404(abf, fig):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0405(abf, fig):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0406(abf, fig):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0422(abf, fig):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_0423(abf, fig):
    pyABFauto.analyses.memtest.figureOverTime(abf, fig)


def analyze_6(abf, fig):  # 6 MT-mon
    analyze_0405(abf, fig)


def analyze_MT_mon_2(abf, fig):  # MT-mon_2 (SS)
    analyze_0405(abf, fig)


def analyze_EPSCs(abf, fig):  # SS
    analyze_0405(abf, fig)


def analyze_0501(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=3)


def analyze_0502(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0503(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0504(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0505(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0506(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0507(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0509(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=2)


def analyze_0512(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=3)


def analyze_0513(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=3)


def analyze_0514(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=3)


def analyze_0600(abf, fig):
    pyABFauto.analyses.stimulation.figureTestElectricalTrainVC(
        abf, fig, stimEpochNumber=3)


def analyze_0601(abf, fig):
    pyABFauto.analyses.stimulation.figureVariedPulseTime(abf, fig)


def analyze_0602(abf, fig):
    pyABFauto.analyses.stimulation.figureTestElectricalResponseVC(
        abf, fig, stimEpochNumber=3)


def analyze_0602(abf, fig):
    pyABFauto.analyses.stimulation.figureTestElectricalResponseVC(
        abf, fig, stimEpochNumber=3)


def analyze_0606(abf, fig):
    pyABFauto.analyses.stimulation.figureTestElectricalResponseIC(
        abf, fig, stimEpochNumber=2)


def analyze_0607(abf, fig):
    pyABFauto.analyses.stimulation.figureTestElectricalResponseVC(
        abf, fig, stimEpochNumber=4)


def analyze_0611(abf, fig):
    pyABFauto.analyses.dsi.evokedInwardCurrent(abf, fig)


def analyze_0612(abf, fig):
    pyABFauto.analyses.dsi.singleSweepWithProtocol(abf, fig)


def analyze_0613(abf, fig):
    pyABFauto.analyses.dsi.evokedInwardCurrent(abf, fig)


def analyze_Signal(abf, fig):  # SS spike fidelity
    if abf.sweepUnitsY == "pA":
        pyABFauto.analyses.stimulation.optoResponse(
            abf, fig, optoEpochNumber=4)
    else:
        #pyABFauto.analyses.stimulation.figureTestElectricalResponseVC(abf, fig, stimEpochNumber=4)
        pyABFauto.analyses.timeCourse.apFreqOverTime(abf, fig)


def analyze_xxxx(abf, fig):
    pyABFauto.analyses.stimulation.optoResponse(abf, fig, optoEpochNumber=3)


def analyze_0913(abf, fig):
    pyABFauto.analyses.jeff.tau(abf, fig)
