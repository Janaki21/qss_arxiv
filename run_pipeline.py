import os
import pandas as pd

from synthetic_generator import generate_state

from analysis import *

from plotting import *

from statistics_validation import run_statistics

from real_eeg import *

from real_comparison import analyze_real_states

from sensitivity_analysis import sensitivity_analysis

from advanced_plots import *

from composite_figures import create_composite

from state_space import create_state_space


os.makedirs(
    "figures",
    exist_ok=True
)

os.makedirs(
    "results",
    exist_ok=True
)


states = [

    "rest",
    "task",
    "fatigue"

]


summary_rows = []


for state in states:

    print(f"\nRunning {state}")

    signal = generate_state(state)

    freqs, psd = compute_psd(signal)

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

    summary_rows.append({

        "state": state,
        "beta": beta,
        "qss": qss,
        "tau": tau,
        "dc": dc,
        "residual_std": residual.std()

    })


summary = pd.DataFrame(summary_rows)

summary.to_csv(
    "results/summary.csv",
    index=False
)


print("\nRunning statistical validation")

stats_df = run_statistics()

stats_df.to_csv(
    "results/statistics.csv",
    index=False
)


print("\nDownloading EEG dataset")

download_dataset()


print("\nRunning real EEG comparison")

real_df = analyze_real_states()

print(real_df)


print("\nRunning sensitivity analysis")

sensitivity_analysis()


print("\nGenerating advanced figures")

plot_statistics()

plot_sensitivity()

create_composite()

print("\nGenerating state-space figure")

create_state_space()
print("\nPIPELINE COMPLETE")