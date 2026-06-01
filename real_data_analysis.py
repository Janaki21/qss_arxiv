import numpy as np

from scipy.signal import welch

from analysis import estimate_beta

from plotting import plot_psd


def analyze_real_eeg(raw):

    data = raw.get_data()

    signal = data[0]

    fs = int(raw.info['sfreq'])

    freqs, psd = welch(
        signal,
        fs=fs,
        nperseg=fs * 4
    )

    beta, fitted, residual = estimate_beta(
        freqs,
        psd
    )

    plot_psd(
        freqs,
        psd,
        fitted,
        "real_eeg"
    )

    return {

        "beta": beta,
        "residual_std": np.std(residual)

    }