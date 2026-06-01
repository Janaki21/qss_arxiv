import matplotlib.pyplot as plt
import pandas as pd


def create_state_space():

    synthetic = pd.read_csv(
        "results/summary.csv"
    )

    real = pd.read_csv(
        "results/real_eeg_comparison.csv"
    )

    plt.figure(figsize=(8,6))

    plt.scatter(

        synthetic["dc"],
        synthetic["qss"],
        s=200,
        label="Synthetic"

    )

    for _, row in synthetic.iterrows():

        plt.text(

            row["dc"],
            row["qss"],
            row["state"]

        )

    plt.scatter(

        real["dc"],
        real["qss"],
        s=200,
        marker='x',
        label="Real EEG"

    )

    for _, row in real.iterrows():

        plt.text(

            row["dc"],
            row["qss"],
            row["state"]

        )

    plt.xlabel(
        "Degree of Coherence (DC)"
    )

    plt.ylabel(
        "QSS"
    )

    plt.title(
        "QSS-Coherence State Space"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(

        "figures/state_space.png",
        dpi=300

    )

    plt.close()
    