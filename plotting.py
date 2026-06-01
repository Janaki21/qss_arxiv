import matplotlib.pyplot as plt
import numpy as np


def plot_psd(
    freqs,
    psd,
    fitted,
    state
):

    plt.figure(figsize=(9,6))

    plt.loglog(
        freqs,
        psd,
        linewidth=2,
        label="PSD"
    )

    mask = (
        (freqs >= 2) &
        (freqs <= 40)
    )

    plt.loglog(
        freqs[mask],
        10 ** fitted,
        '--',
        linewidth=2,
        label="Aperiodic Fit"
    )

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Spectral Density")

    plt.title(
        f"{state.capitalize()} EEG Spectrum"
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"figures/{state}_psd.png",
        dpi=300
    )

    plt.close()


def plot_beta_series(
    beta_series,
    state
):

    plt.figure(figsize=(10,5))

    plt.plot(
        beta_series,
        linewidth=2
    )

    plt.axhline(
        np.mean(beta_series),
        linestyle='--'
    )

    plt.xlabel("Window Index")
    plt.ylabel("Beta Exponent")

    plt.title(
        f"{state.capitalize()} Temporal Beta Dynamics"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"figures/{state}_beta_dynamics.png",
        dpi=300
    )

    plt.close()


def plot_autocorr(
    autocorr,
    state
):

    plt.figure(figsize=(8,5))

    plt.plot(
        autocorr,
        linewidth=2
    )

    plt.axhline(
        1/np.e,
        linestyle='--'
    )

    plt.xlabel("Lag")
    plt.ylabel("Autocorrelation")

    plt.title(
        f"{state.capitalize()} Temporal Coherence"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"figures/{state}_autocorr.png",
        dpi=300
    )

    plt.close()