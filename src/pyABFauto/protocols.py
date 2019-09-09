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
import pyABFauto.analyses.timeCourse


def analyze_0111(abf, fig):
    pyABFauto.analyses.apShape.firstAP(abf, fig)


def analyze_0112(abf, fig):
    pyABFauto.analyses.apGain.step(abf, fig, .14, .65, 1.64, 2.15)


def analyze_0113(abf, fig):
    pyABFauto.analyses.apGain.step(abf, fig, .14, .65, 1.64, 2.15)


def analyze_0114(abf, fig):
    pyABFauto.analyses.apGain.step(abf, fig, .14, .65, 1.64, 2.15)


def analyze_0201(abf, fig):
    pyABFauto.analyses.memtest.figureMemtest(abf, fig)


def analyze_0202(abf, fig):
    pyABFauto.analyses.iv.step(abf, fig, 2.3, 2.5, 2.566, 2.59)


def analyze_0203(abf, fig):
    pyABFauto.analyses.iv.step(abf, fig, .5, .95, 2.566, 2.59)


def analyze_0304(abf, fig):
    pyABFauto.analyses.timeCourse.apFreqOverTime(abf, fig)


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


def analyze_0602(abf, fig):
    pyABFauto.analyses.stimulation.figureTestElectricalResponseVC(
        abf, fig, stimEpochNumber=3)
