import numpy as np
import pandas as pd

from synthetic_generator import generate_state

from analysis import *

from config import *


def run_statistics():

    rows = []

    for state in [
        "rest",
        "task",
        "fatigue"
    ]:

        for seed in range(N_SIMULATIONS):

            np.random.seed(seed)

            signal = generate_state(state)

            freqs, psd = compute_psd(signal)

            beta, fitted, residual = estimate_beta(
                freqs,
                psd
            )

            beta_series = sliding_beta(signal)

            qss = compute_qss(beta_series)

            tau, dc, _ = temporal_coherence(
                beta_series
            )

            rows.append({

                "state": state,
                "seed": seed,
                "beta": beta,
                "qss": qss,
                "tau": tau,
                "dc": dc,
                "residual_std": np.std(residual)

            })

    return pd.DataFrame(rows)