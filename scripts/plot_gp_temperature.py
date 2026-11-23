"""Generate the three views of the temperature prediction used in the GP slides."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ASSETS = Path(__file__).resolve().parents[1] / "assets"


def kernel(x, z):
    return 4 * np.exp(-0.5 * (np.subtract.outer(x, z) / 24) ** 2)


def main():
    rng = np.random.default_rng(22)
    grid = np.linspace(0, 100, 201)
    locations = np.array([8, 24, 40, 68, 80, 94])
    measurements = np.array([-1.2, -0.3, 1.1, 1.75, 0.7, -0.4])
    noise = 0.18
    t = 54
    cross = kernel(grid, locations)
    A = kernel(locations, locations) + noise**2 * np.eye(len(locations))
    weights = np.linalg.solve(A, measurements)
    mean = cross @ weights
    k_t = kernel(locations, [t]).ravel()
    variance = kernel([t], [t]).item() - k_t @ np.linalg.solve(A, k_t)

    # Condition each prior draw on the same six noisy measurements.
    grid_cov = kernel(grid, grid)
    prior = np.linalg.cholesky(grid_cov + 1e-10 * np.eye(len(grid))) @ rng.normal(size=(len(grid), 5))
    observed_draws = prior[np.searchsorted(grid, locations)] + noise * rng.normal(size=(len(locations), 5))
    conditional = prior + cross @ np.linalg.solve(A, measurements[:, None] - observed_draws)

    # Push N(0, A^{-1}) through two Gauss–Seidel sweeps on the weights.
    G = np.eye(len(A)) - np.linalg.solve(np.tril(A), A)
    G2 = G @ G
    early_weights = weights - G2 @ weights
    solver_draws = G2 @ np.linalg.solve(np.linalg.cholesky(A).T, rng.normal(size=(len(A), 5)))
    early_curves = conditional + cross @ (early_weights[:, None] - weights[:, None] + solver_draws)
    projected = G2.T @ k_t
    early_variance = variance + projected @ np.linalg.solve(A, projected)

    plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.serif": ["Computer Modern Roman"]})
    states = [
        ("prior", "Prior draws", prior, None, None),
        ("conditioned", "Conditional draws", conditional, k_t @ weights, variance),
        ("two-steps", "After two solver steps", early_curves, k_t @ early_weights, early_variance),
    ]
    for name, label, curves, centre, var in states:
        fig, ax = plt.subplots(figsize=(11.5, 4.7))
        fig.subplots_adjust(left=0.10, bottom=0.21, right=0.98, top=0.83)
        ax.set(xlim=(0, 100), ylim=(-5, 5), yticks=[-4, -2, 0, 2, 4],
               xlabel="Distance along transect (km)", ylabel=r"Temperature anomaly ($^\circ$C)")
        ax.set_xticks([0, 25, t, 75, 100], ["0", "25", r"$t$", "75", "100"])
        ax.tick_params(labelsize=15, colors="#45545c", length=3)
        ax.xaxis.label.set_size(17)
        ax.yaxis.label.set_size(17)
        ax.spines[["right", "top"]].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color("#82919a")
        ax.axvline(t, color="#667b85", lw=1.2, ls=(0, (3, 3)))
        paths = ax.plot(grid, curves, color="#387892", lw=1.65, alpha=0.73)
        paths[0].set_label(label)
        if centre is not None:
            ax.scatter(locations, measurements, s=50, color="#202f37", marker="D",
                       edgecolors="white", linewidths=0.9, zorder=4, label="Measurements")
            ax.errorbar(t, centre, yerr=1.96 * np.sqrt(var), fmt="o", color="#af4819",
                        lw=2.8, capsize=8, capthick=2.5, zorder=5, label=r"Mean and 95\% interval")
        ax.legend(loc="lower left", bbox_to_anchor=(0, 1.02), ncol=3, borderaxespad=0,
                  fontsize=15, frameon=False, handlelength=1.7, columnspacing=1.6)
        fig.savefig(ASSETS / f"temperature-{name}.svg", metadata={"Date": None})
        plt.close(fig)


if __name__ == "__main__":
    main()
