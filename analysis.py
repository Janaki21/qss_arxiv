import numpy as np

from scipy.signal import welch

from specparam import SpectralModel


FS = 250


def compute_psd(signal):

    freqs, psd = welch(

        signal,
        fs=FS,
        nperseg=FS * 4

    )

    return freqs, psd


def estimate_beta(freqs, psd):

    mask = (

        (freqs >= 2) &
        (freqs <= 40)

    )

    fit_freqs = freqs[mask]

    fit_psd = psd[mask]

    fm = SpectralModel(

        peak_width_limits=[1, 8],
        max_n_peaks=6,
        min_peak_height=0.05,
        verbose=False

    )

    fm.fit(

        fit_freqs,
        fit_psd

    )

    # SAFE extraction across versions

    aperiodic_params = fm.get_params(
        'aperiodic'
    )

    intercept = float(
        aperiodic_params[0]
    )

    exponent = float(
        aperiodic_params[1]
    )

    fitted = (

        10 ** intercept *
        (fit_freqs ** (-exponent))

    )

    residual = (

        np.log10(fit_psd) -
        np.log10(fitted)

    )

    return exponent, fitted, residual


def sliding_beta(

    signal,
    window_sec=10,
    step_sec=5

):

    betas = []

    win = FS * window_sec

    step = FS * step_sec

    for start in range(

        0,
        len(signal) - win,
        step

    ):

        segment = signal[
            start:start + win
        ]

        freqs, psd = compute_psd(segment)

        beta, _, _ = estimate_beta(
            freqs,
            psd
        )

        betas.append(beta)

    return np.array(betas)


def compute_qss(beta_series):

    mu = np.mean(beta_series)

    sigma = np.std(beta_series)

    if abs(mu) < 1e-6:

        return 0

    qss = 1 - (sigma / abs(mu))

    qss = np.clip(qss, 0, 1)

    return qss


def temporal_coherence(beta_series):

    beta_series = (
        beta_series -
        np.mean(beta_series)
    )

    autocorr = np.correlate(

        beta_series,
        beta_series,
        mode='full'

    )

    autocorr = autocorr[
        autocorr.size // 2:
    ]

    autocorr = autocorr / autocorr[0]

    threshold = 1 / np.e

    tau = 1

    for i, val in enumerate(autocorr):

        if val < threshold:

            tau = i

            break

    dc = tau / len(beta_series)

    return tau, dc, autocorr