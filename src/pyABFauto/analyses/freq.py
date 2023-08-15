import pyABFauto
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyabf
import pathlib
import pyabf
import scipy
import scipy.signal


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


def smooth(signal: np.ndarray, level: float) -> np.ndarray:
    b, a = scipy.signal.butter(3, 1/level)
    return scipy.signal.filtfilt(b, a, signal)


def get_binned_counts(times: list[float], bins: np.ndarray):
    counts = np.empty(len(bins)-1) * np.nan
    for i in range(len(counts)):
        bin_start = bins[i]
        bin_end = bins[i+1]
        bin_indexes = [x for x in times
                       if x >= bin_start and x < bin_end]
        counts[i] = len(bin_indexes)
    return counts


def get_breaths_per_minute(abf: pyabf.ABF, channel=1):

    # get original signal
    ys = abf.getAllYs(channel)

    # low-pass filter
    ys = smooth(ys, 250)

    # center at zero
    ys = ys - smooth(ys, 5_000)

    # detect crossings
    zero_crossings = np.diff((ys < 0) * 1)
    zero_crossings = np.where(zero_crossings > 0)[0]
    breaths = []
    for i in range(len(zero_crossings) - 1):
        i1 = zero_crossings[i]+1
        i2 = zero_crossings[i+1]
        segment = ys[i1:i2]
        time = i1 / abf.sampleRate
        amplitude = max(segment) - min(segment)
        breath = (time, amplitude)
        breaths.append(breath)

    # remove small breaths
    baseline_breath_amplitudes = [x[1] for x in breaths[:50]]
    amplitude_threshold = np.mean(baseline_breath_amplitudes) * .05
    breaths = [x for x in breaths if x[1] >= amplitude_threshold]
    breath_times = [x[0]/60 for x in breaths]

    # get binned breathing rate
    max_bin = 25
    bin_size = .5
    bin_count = max_bin // bin_size
    bins = np.arange(bin_count + 1) * bin_size
    bin_edges = bins[:-1]
    counts = get_binned_counts(breath_times, bins)
    bpm = counts / bin_size

    return (bin_edges, bpm)


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
    bins, bpm = get_breaths_per_minute(abf)
    plt.subplot(224, sharex=ax2)
    plt.plot(bins, bpm, '.-')
    plt.ylabel("Breaths per Minute")
    plt.xlabel("Time (minutes)")
    plt.axis([None, None, 0, None])
    plt.grid(alpha=.5, ls='--')
    plt.tight_layout()
