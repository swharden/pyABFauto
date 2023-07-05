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


def plotStevOverTime(abf: pyabf.ABF, channel: int):
    # calculate binned standard deviation
    signal1 = abf.getAllYs(channel)
    binSizeSec = 30
    binCount = int(len(signal1) / abf.sampleRate / binSizeSec)
    binStarts = np.arange(binCount) * binSizeSec / 60
    stdevs1 = np.zeros(binCount)
    for i in range(binCount):
        i1 = int(binSizeSec * abf.sampleRate * i)
        i2 = i1 + int(binSizeSec * abf.sampleRate)
        stdevs1[i] = np.std(signal1[i1:i2])

    # normalize to first 5 minutes
    baseline = np.percentile(stdevs1[:10], 50)
    stdevs1 = stdevs1 / baseline * 100

    plt.axhline(100, color='k', ls='--')
    plt.grid(alpha=.5, ls='--')
    plt.plot(binStarts, stdevs1, '.-', color='C0')
    plt.ylabel("Standard Deviation (%)")
    plt.xlabel("Time (minutes)")
    addCommentTimes(abf)
    ymax = max(stdevs1) * 1.2
    ymax = min(ymax, 1_000)
    plt.axis([None, None, 0, ymax])


def plotSpectrogramAndPowerOverTime(abf: pyabf.ABF, ax: matplotlib.axes.Axes):

    # calculate spectrogram
    (spectrogram1, times, freqs) = getSpectrogram(abf, 0)
    (spectrogram2, times, freqs) = getSpectrogram(abf, 1)

    # top left
    ax1 = plt.subplot(221)
    plt.title(f"Channel 1")
    plt.ylabel("Frequency (Hz)")
    plotSpectrogram(spectrogram1, times, freqs)
    addCommentTimes(abf)

    # top right
    ax2 = plt.subplot(222, sharex=ax1)
    plt.title(f"Channel 2")
    plt.ylabel("Frequency (Hz)")
    plotSpectrogram(spectrogram2, times, freqs)
    addCommentTimes(abf)

    # bottom left
    plt.subplot(223, sharex=ax1)
    plotStevOverTime(abf, 0)

    # bottom right
    plt.subplot(224, sharex=ax2)
    plotStevOverTime(abf, 1)

    plt.tight_layout()
