"""
Figures here are for multi-sweep membrane tests intended
to calcaulate mean passive membrane properties.
"""

import pyabf
import pyabf.tools
import pyABFauto

import matplotlib.pyplot as plt


def figureMemtest(abf, fig):
    assert isinstance(abf, pyabf.ABF)
    assert isinstance(fig, pyABFauto.figure.Figure)

    mt = pyabf.tools.Memtest(abf)

    plt.title("Membrane Test (%d sweeps)" % abf.sweepCount)

    bbox = dict(facecolor='#FFFFFF66', edgecolor='#00000066', boxstyle='round,pad=.4')
    plt.gca().text(0.96, 0.96, mt.summary, verticalalignment='top',
                   horizontalalignment='right',
                   transform=plt.gca().transAxes, fontsize=10,
                   bbox=bbox, family='monospace')

    fig.plotStacked()
