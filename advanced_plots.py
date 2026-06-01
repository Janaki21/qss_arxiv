import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid")


def plot_statistics():

    df = pd.read_csv(
        "results/statistics.csv"
    )

    metrics = [
        "beta",
        "qss",
        "tau",
        "dc"
    ]

    for metric in metrics:

        plt.figure(figsize=(8,5))

        sns.boxplot(
            data=df,
            x="state",
            y=metric
        )

        sns.stripplot(
            data=df,
            x="state",
            y=metric,
            alpha=0.5
        )

        plt.title(
            f"{metric.upper()} Across States"
        )

        plt.tight_layout()

        plt.savefig(
            f"figures/{metric}_boxplot.png",
            dpi=300
        )

        plt.close()


def plot_sensitivity():

    df = pd.read_csv(
        "results/sensitivity_analysis.csv"
    )

    plt.figure(figsize=(10,6))

    sns.lineplot(
        data=df,
        x="noise_scale",
        y="beta",
        hue="state",
        style="fit_range",
        markers=True
    )

    plt.title(
        "Sensitivity Analysis of Beta Estimates"
    )

    plt.tight_layout()

    plt.savefig(
        "figures/sensitivity_analysis.png",
        dpi=300
    )

    plt.close()