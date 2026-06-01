import numpy as np


def generate_colored_noise(beta, samples, fs):

    freqs = np.fft.rfftfreq(
        samples,
        d=1/fs
    )

    scaling = np.zeros_like(freqs)

    scaling[1:] = 1 / (
        freqs[1:] ** (beta / 2)
    )

    random_phases = np.exp(
        2j * np.pi * np.random.rand(len(freqs))
    )

    spectrum = scaling * random_phases

    signal = np.fft.irfft(
        spectrum,
        n=samples
    )

    signal = signal / np.std(signal)

    return signal


def add_oscillations(
    signal,
    fs,
    alpha_amp,
    theta_amp,
    gamma_amp
):

    t = np.arange(len(signal)) / fs

    alpha = alpha_amp * np.sin(
        2 * np.pi * 10.2 * t
    )

    theta = theta_amp * np.sin(
        2 * np.pi * 5.8 * t
    )

    gamma = gamma_amp * np.sin(
        2 * np.pi * 38.0 * t
    )

    return signal + alpha + theta + gamma


def generate_state(state):

    fs = 250

    duration = 180

    samples = fs * duration

    params = {

        "rest": {

            "beta": 1.7,
            "alpha": 4.5,
            "theta": 0.6,
            "gamma": 0.15,
            "noise": 0.35

        },

        "task": {

            "beta": 1.05,
            "alpha": 1.8,
            "theta": 1.9,
            "gamma": 0.95,
            "noise": 0.55

        },

        "fatigue": {

            "beta": 2.1,
            "alpha": 2.2,
            "theta": 2.8,
            "gamma": 0.1,
            "noise": 0.28

        }

    }

    p = params[state]

    signal = generate_colored_noise(
        p["beta"],
        samples,
        fs
    )

    signal = add_oscillations(
        signal,
        fs,
        p["alpha"],
        p["theta"],
        p["gamma"]
    )

    signal += np.random.normal(
        0,
        p["noise"],
        samples
    )

    return signal