import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def create_composite():

    figures = [

        "figures/rest_psd.png",
        "figures/task_psd.png",
        "figures/fatigue_psd.png",

        "figures/rest_beta_dynamics.png",
        "figures/task_beta_dynamics.png",
        "figures/fatigue_beta_dynamics.png"

    ]

    fig, axes = plt.subplots(
        2,
        3,
        figsize=(18,10)
    )

    axes = axes.flatten()

    for ax, file in zip(axes, figures):

        img = mpimg.imread(file)

        ax.imshow(img)

        ax.axis('off')

    plt.tight_layout()

    plt.savefig(
        "figures/composite_figure.png",
        dpi=300
    )

    plt.close()