import pyABFauto
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyabf
import pathlib
import pyabf


def getSpectrogram(abf: pyabf.ABF, channel: int, stepLength=5, windowLength=30, rowCount=400):
    signal = abf.getAllYs(channelIndex=channel)
    windowSize = int(abf.sampleRate * windowLength)
    window = np.hanning(windowSize)
    stepSize = int(abf.sampleRate * stepLength)
    segmentCount = (len(signal) - windowSize) // stepSize + 1
    times = np.arange(segmentCount) * stepLength
    freqs = np.fft.fftfreq(windowSize, 1.0/abf.dataRate)[:rowCount]
    spectrogramData = np.empty((rowCount, segmentCount))
    for i in range(segmentCount):
        i1 = i * stepSize
        i2 = i1 + windowSize
        segment = signal[i1:i2]
        segment = segment * window
        fft = np.fft.fft(segment)
        fft = np.abs(fft) * 2 / len(segment)
        spectrogramData[:, i] = fft[:rowCount]
        spectrogramData[0, i] = 0  # blank the DC component
        spectrogramData[1, i] = 0  # blank the DC component
    return (spectrogramData, times, freqs)


def plotSpectrogram(spectrogramData: np.ndarray, times: np.ndarray, freqs: np.ndarray):
    vmax = np.percentile(spectrogramData, 95)
    plt.imshow(spectrogramData, cmap='viridis', aspect='auto', interpolation='nearest',
               origin='lower', extent=[0, times[-1] / 60, 0, freqs[-1]], vmax=vmax)
    plt.ylabel("Frequency (Hz)")


def plotSpectralPowerOverTime(spectrogramData: np.ndarray, times: np.ndarray):
    ys = np.sum(spectrogramData, axis=0)
    xs = times / 60
    plt.plot(xs, ys)
    plt.ylabel("Magnitude (mV)")
    plt.xlabel("Time (minutes)")
    plt.grid(ls='--', alpha=.5)


def addCommentTimes(abf: pyabf.ABF):
    for i, comment in enumerate(abf.tagComments):
        plt.axvline(abf.tagTimesMin[i], linewidth=2,
                    color='w', alpha=.5, linestyle='--')


def plotSpectrogramAndPowerOverTime(abf: pyabf.ABF, ax: matplotlib.axes.Axes):

    (dataEEG, times, freqs) = getSpectrogram(abf, 0)
    (dataBreath, times, freqs) = getSpectrogram(abf, 1)

    ax1 = plt.subplot(211)
    plt.title(f"EEG")
    plotSpectrogram(dataEEG, times, freqs)
    addCommentTimes(abf)

    ax2 = plt.subplot(212, sharex=ax1)
    plt.title(f"Breathing")
    plotSpectrogram(dataBreath, times, freqs)
    addCommentTimes(abf)

    plt.tight_layout()
