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


def lowpass(data: np.ndarray, cutoff: float, sample_rate: float, poles: int = 5):
    sos = scipy.signal.butter(poles, cutoff, 'lowpass',
                              fs=sample_rate, output='sos')
    filtered_data = scipy.signal.sosfiltfilt(sos, data)
    return filtered_data


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
    max_bin = int(abf.dataLengthMin)
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


def inspect_channel(ax, abf: pyabf.ABF, channel: int):

    # plot the trace
    ys = abf.getAllYs(channel)
    xs = np.arange(len(ys))/abf.sampleRate
    ax.plot(xs/60, ys, color='k', lw=.2)
    ax.grid(alpha=.5, ls='--')

    # auto-scale to fit the majority of data
    ax.margins(0, .1)
    ys_baseline = ys[:abf.sampleRate*5*60]
    ys_baseline_mean = np.mean(ys_baseline)
    ys_baseline_max = np.percentile(ys_baseline, 55)
    ys_baseline_min = np.percentile(ys_baseline, 45)
    ys_baseline_range = (ys_baseline_max - ys_baseline_min) * 200
    view_min = ys_baseline_mean - ys_baseline_range
    view_max = ys_baseline_mean + ys_baseline_range
    ax.axis([None, None, view_min, view_max])
    ax.set_title(f"Channel {channel+1}")


def _bandpass(ys, sample_rate, low, high):
    sos = scipy.signal.butter(6, [low, high], 'bandpass',
                              fs=sample_rate, output='sos')
    return scipy.signal.sosfilt(sos, ys)


def get_binned_stdev(abf: pyabf.ABF, channel: int):
    ys = abf.getAllYs(channel)
    sample_rate = abf.sampleRate
    ys = lowpass(ys, 55, sample_rate)

    binsize_min = .5
    binsize_sec = binsize_min * 60
    binsize_points = int(binsize_sec * sample_rate)
    bin_count = int(abf.dataLengthSec / binsize_sec)
    bin_times = np.arange(bin_count) * binsize_min
    bin_edges = np.arange(bin_count) * binsize_points
    binned_stdev = [None] * bin_count

    for i, bin_edge in enumerate(bin_edges):
        i1 = bin_edge
        i2 = bin_edge + binsize_points
        sample = ys[i1:i2]
        binned_stdev[i] = np.std(sample)

    return bin_times, binned_stdev


def get_binned_power(abf: pyabf.ABF, channel: int, freq_min: float, freq_max: float):
    ys = abf.getAllYs(channel)
    sample_rate = abf.sampleRate

    binsize_min = .5
    binsize_sec = binsize_min * 60
    binsize_points = int(binsize_sec * sample_rate)
    bin_count = int(abf.dataLengthSec / binsize_sec)
    bin_times = np.arange(bin_count) * binsize_min
    bin_edges = np.arange(bin_count) * binsize_points
    binned_power = [None] * bin_count

    for i, bin_edge in enumerate(bin_edges):

        # isolate a segment in time
        i1 = bin_edge
        i2 = bin_edge + binsize_points
        sample = ys[i1:i2]

        # apply a window
        window = scipy.signal.windows.hann(len(sample))
        sample = sample * window

        # calculate the FFT
        fft = scipy.fft.rfft(sample)
        fft[0] = 0
        fft_mag = np.abs(fft)[:-1]
        fft_power = np.log10(1+fft_mag)
        xf = scipy.fft.fftfreq(len(sample), 1/sample_rate)[:len(sample)//2]

        # isolate the frequency range of interest
        i1 = int(freq_min/xf[1])
        i2 = int(freq_max/xf[1])
        xf = xf[i1:i2]
        fft_mag = fft_mag[i1:i2]
        fft_power = fft_power[i1:i2]

        # accumulate
        binned_power[i] = np.sum(fft_mag)

    return bin_times, binned_power


def plot_binned_power(ax, abf: pyabf.ABF, channel: int, freq_min: float, freq_max: float):
    bin_times, binned_power = get_binned_power(abf, channel,
                                               freq_min, freq_max)
    binned_power_norm = binned_power / np.mean(binned_power[1:10]) * 100
    ax.plot(bin_times, binned_power_norm, '.-')
    ax.set_title(f"EEG Activity ({freq_min}-{freq_max} Hz)")
    ax.set_ylabel("Power (%)")
    ax.set_xlabel("Time (minutes)")
    ax.axhline(100, color='k', ls='--')
    ax.grid(alpha=.5, ls='--')
    return binned_power


def plot_breathing_rate(ax, abf: pyabf.ABF, channel: int):
    bins, bpm = get_breaths_per_minute(abf)
    ax.plot(bins, bpm, '.-')
    ax.set_ylabel("BPM")
    ax.set_xlabel("Time (minutes)")
    ax.set_title("Breathing Rate")
    ax.axis([None, None, 0, None])
    ax.grid(alpha=.5, ls='--')
    return bpm


def save_fft_csv(abf: pyabf.ABF):

    column_names = []
    column_names.append("Time (minutes)")
    column_names.append("Respiration (bpm)")
    column_names.append("EEG Delta (0.5-4 Hz)")
    column_names.append("EEG Theta (4-8 Hz)")
    column_names.append("EEG Alpha (8-12 Hz)")
    column_names.append("EEG Beta (12-35 Hz)")
    column_names.append("EEG Gamma (35-55 Hz)")
    column_names.append("EEG Total (0.5-55 Hz)")
    column_names.append("Standard Deviation")

    _, bpm = get_breaths_per_minute(abf, 1)

    _, eeg_delta = get_binned_power(abf, 0, .5, 4)
    _, eeg_theta = get_binned_power(abf, 0, 4, 8)
    _, eeg_alpha = get_binned_power(abf, 0, 8, 12)
    _, eeg_beta = get_binned_power(abf, 0, 12, 35)
    _, eeg_gamma = get_binned_power(abf, 0, 35, 55)
    _, eeg_total = get_binned_power(abf, 0, .5, 55)

    _, stdev = get_binned_stdev(abf, 0)

    # trim to match lengths
    assert len(bpm) <= len(eeg_total)

    # create CSV text
    csv = ", ".join(column_names) + "\n"
    for i in range(len(bpm)):
        line = []
        line.append(f"{i*.5}")
        line.append(f"{bpm[i]}")
        line.append(f"{eeg_delta[i]}")
        line.append(f"{eeg_theta[i]}")
        line.append(f"{eeg_alpha[i]}")
        line.append(f"{eeg_beta[i]}")
        line.append(f"{eeg_gamma[i]}")
        line.append(f"{eeg_total[i]}")
        line.append(f"{stdev[i]}")
        csv += ", ".join(line) + "\n"

    # save CSV file
    csv_folder = pathlib.Path(abf.abfFilePath).parent.joinpath("_autoanalysis")
    csv_folder.mkdir(exist_ok=True)
    csv_file = csv_folder.joinpath(abf.abfID+".csv")
    csv_file.write_text(csv)
    print(f"saved: {csv_file}")


def plot_eeg_power_and_breathing_rate(abf: pyabf.ABF):
    fig, axes = plt.subplots(2, 2, sharex=True, figsize=(8, 6))
    inspect_channel(axes[0][0], abf, 0)
    inspect_channel(axes[0][1], abf, 1)
    plot_binned_power(axes[1][0], abf, 0, .5, 55)
    plot_breathing_rate(axes[1][1], abf, 1)
    save_fft_csv(abf)
    plt.margins(0, .1)
    fig.tight_layout()
