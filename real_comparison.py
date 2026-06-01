import pandas as pd

from scipy.signal import welch

from analysis import *

from plotting import *

from real_eeg import *


def analyze_real_states():

    rest_raw = load_rest_data()

    task_raw = load_task_data()

    rest_signal = extract_signal(rest_raw)

    task_signal = extract_signal(task_raw)

    fs = int(rest_raw.info['sfreq'])

    rows = []

    for state, signal in [

        ("real_rest", rest_signal),
        ("real_task", task_signal)

    ]:

        freqs, psd = welch(
            signal,
            fs=fs,
            nperseg=fs * 4
        )

        beta, fitted, residual = estimate_beta(
            freqs,
            psd
        )

        beta_series = sliding_beta(signal)

        qss = compute_qss(beta_series)

        tau, dc, autocorr = temporal_coherence(
            beta_series
        )

        plot_psd(
            freqs,
            psd,
            fitted,
            state
        )

        plot_beta_series(
            beta_series,
            state
        )

        plot_autocorr(
            autocorr,
            state
        )

        rows.append({

            "state": state,
            "beta": beta,
            "qss": qss,
            "tau": tau,
            "dc": dc,
            "residual_std": residual.std()

        })

    df = pd.DataFrame(rows)

    df.to_csv(
        "results/real_eeg_comparison.csv",
        index=False
    )

    return df