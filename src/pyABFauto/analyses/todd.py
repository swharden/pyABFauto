import pyabf
import pyabf.filter
import pyABFauto
import pyABFauto.figure

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def vc_ican(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    pyabf.filter.gaussian(abf, 20)

    cmap = plt.cm.get_cmap('rainbow')
    for sweepIndex in range(abf.sweepCount):
        fraction = sweepIndex / \
            (abf.sweepCount - 1) if abf.sweepCount > 1 else 0
        abf.setSweep(sweepIndex)
        plt.plot(abf.sweepX, abf.sweepY, color=cmap(
            fraction), label=f"sweep {sweepIndex+1}")

    # plt.legend(loc="upper right")
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.grid(alpha=.5, ls='--')


def vc_ican_dt(abf: pyabf.ABF, fig: pyABFauto.figure.Figure):

    pyabf.filter.gaussian(abf, 25)

    index1 = int(abf.sampleRate * 3.350)
    index2 = index1 + int(abf.sampleRate * 3)
    xs = np.arange(index2-index1) / abf.sampleRate

    cmap = plt.cm.get_cmap('turbo')
    fractions = np.linspace(0, 1, num=abf.sweepCount)
    colors = [cmap(x) for x in fractions]

    stim_times = np.arange(abf.sweepCount) * 25
    iadp_by_sweep = [None] * abf.sweepCount

    for i in range(abf.sweepCount):
        abf.setSweep(i)
        ys = abf.sweepY[index1:index2]
        baseline = np.mean(ys[-int(len(ys)/5):])
        ys = ys - baseline
        iadp_segment_width_sec = 1
        iadp_segment_t1 = index1 / abf.sampleRate
        iadp_segment_t2 = iadp_segment_t1 + iadp_segment_width_sec
        iadp_segment = ys[:int(abf.sampleRate*iadp_segment_width_sec)]
        iadp_by_sweep[i] = -np.sum(iadp_segment) / abf.sampleRate

        plt.subplot(211)
        plt.plot(abf.sweepX, abf.sweepY, color=colors[i], label=f"sweep {i+1}")
        if i == 0:
            plt.axvspan(iadp_segment_t1, iadp_segment_t2, color='k', alpha=.1)

        plt.subplot(223)
        plt.plot(xs, ys, color=colors[i], label=f"sweep {i+1}")

    plt.subplot(211)
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.grid(alpha=.5, ls='--')
    plt.axis([2.5, 5, None, None])

    plt.subplot(223)
    plt.ylabel("IADP (pA)")
    plt.xlabel(abf.sweepLabelX)
    plt.grid(alpha=.5, ls='--')

    plt.subplot(224)
    plt.ylabel("IADP (pA*sec)")
    plt.xlabel("Stimulus (msec)")

    plt.plot(stim_times, iadp_by_sweep, '--', color='k')
    for i in range(abf.sweepCount):
        plt.plot(stim_times[i], iadp_by_sweep[i], "o", color=colors[i], ms=10)
    plt.plot([0, 200], [0, 100], color='k', alpha=.5, ls=':')    
    
    plt.grid(alpha=.5, ls='--')
