

import pyabf
import pyabf.tools
import pyABFauto

import matplotlib.pyplot as plt


def stacked(abf, fig):
    fig.plotStacked()
    fig.shadeBackground()


def continuous(abf, fig):
    fig.plotContinuous()
    fig.addTagLines()
    fig.shadeBackground()


def crash(abf, fig):
    fig.plotContinuous()
    fig.addTagLines()
    fig.shadeBackground("ERROR: crashed analyzing this file")


def badunits():
    message = "SCALE ERROR!"
    for i, ax in enumerate(plt.gcf().axes):
        ax.set_facecolor((1.0, 0.9, 0.9))
        t = ax.text(.5, .95, message,
                    transform=ax.transAxes,
                    verticalalignment='top',
                    horizontalalignment='center',
                    fontsize=16,
                    family='monospace',
                    color='k')
        t.set_bbox(dict(facecolor='#FFFF00', edgecolor='k', lw=2))
