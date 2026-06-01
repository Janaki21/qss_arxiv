import numpy as np
import pandas as pd

from synthetic_generator import generate_state

from analysis import *


def sensitivity_analysis():

    rows = []

    fit_ranges = [

        (1, 30),
        (2, 40),
        (3, 45)

    ]

    noise_scales = [
        0.8,
        1.0,
        1.2
    ]

    for state in [
        "rest",
        "task",
        "fatigue"
    ]:

        for fit_min, fit_max in fit_ranges:

            for noise_scale in noise_scales:

                signal = generate_state(state)

                signal *= noise_scale

                freqs, psd = compute_psd(signal)

                mask = (
                    (freqs >= fit_min) &
                    (freqs <= fit_max)
                )

                x = np.log10(freqs[mask])
                y = np.log10(psd[mask])

                slope = np.polyfit(x, y, 1)[0]

                beta = -slope

                rows.append({

                    "state": state,
                    "fit_range": f"{fit_min}-{fit_max}",
                    "noise_scale": noise_scale,
                    "beta": beta

                })

    df = pd.DataFrame(rows)

    df.to_csv(
        "results/sensitivity_analysis.csv",
        index=False
    )

    return df