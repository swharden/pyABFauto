"""
Figures here are for multi-sweep membrane tests intended
to calcaulate mean passive membrane properties.
"""

import pyabf
import pyabf.tools
import pyABFauto

import matplotlib.pyplot as plt
import numpy as np


def figureMemtest(abf, fig):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    mt = pyabf.tools.Memtest(abf)

    plt.title("Membrane Test (%d sweeps)" % abf.sweepCount)

    bbox = dict(facecolor='#FFFFFF66', edgecolor='#00000066',
                boxstyle='round,pad=.4')
    plt.gca().text(0.96, 0.96, mt.summary, verticalalignment='top',
                   horizontalalignment='right',
                   transform=plt.gca().transAxes, fontsize=10,
                   bbox=bbox, family='monospace')

    fig.plotStacked()


def figureOverTime(abf, fig):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    mt = pyabf.tools.Memtest(abf)

    sweepTimesSec = np.arange(abf.sweepCount) * abf.sweepIntervalSec
    sweepTimesMin = sweepTimesSec / 60

    plt.subplot(221)
    fig.grid()
    plt.title(mt.Ih.name)
    plt.ylabel(mt.Ih.units)
    plt.plot(sweepTimesMin, mt.Ih.values, '.', color='b')
    plt.margins(0, .2)
    fig.addTagLines(minutes=True)

    plt.subplot(222)
    fig.grid()
    plt.title(mt.Rm.name)
    plt.ylabel(mt.Rm.units)
    plt.plot(sweepTimesMin, mt.Rm.values, '.', color='r')
    plt.margins(0, .2)
    plt.axis([None, None, 0, None])
    fig.addTagLines(minutes=True)

    plt.subplot(223)
    fig.grid()
    plt.title(mt.Ra.name)
    plt.ylabel(mt.Ra.units)
    plt.plot(sweepTimesMin, mt.Ra.values, '.', color='k')
    plt.margins(0, .2)
    plt.axis([None, None, 0, None])
    fig.addTagLines(minutes=True)

    plt.subplot(224)
    fig.grid()
    plt.title("Full Recording")
    fig.plotContinuous(startAtSec=.5, minutes=True)
    fig.addTagLines(minutes=True)

    return
