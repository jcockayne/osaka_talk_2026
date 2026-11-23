"""Render the two Gauss–Seidel steps and their matching solution reveal."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter


ASSETS = Path(__file__).resolve().parents[1] / "assets"


def main():
    A = np.array([[1.0, 0.8], [0.8, 1.0]])
    solution = np.array([2.0, 1.0])
    b = A @ solution
    points = [np.zeros(2)]
    for _ in range(2):
        x = points[-1]
        points.append(x + np.linalg.solve(np.tril(A), b - A @ x))

    plt.rcParams.update({"text.usetex": True, "font.family": "serif",
                         "font.serif": ["Computer Modern Roman"]})
    fig, ax = plt.subplots(figsize=(9, 5.6), dpi=200)
    fig.subplots_adjust(left=0.12, bottom=0.13, right=0.96, top=0.97)
    ax.set(xlim=(-0.3, 3.25), ylim=(-0.3, 1.55), aspect="equal",
           xticks=[0, 1, 2, 3], yticks=[0, 1])
    ax.tick_params(labelsize=17, colors="#506069")
    ax.spines[["top", "right"]].set_visible(False)
    for spine in ("bottom", "left"):
        ax.spines[spine].set_color("#88979e")

    blue = "#005880"
    for i, (point, offset) in enumerate(zip(points, [(0, 12), (8, -21), (8, 12)])):
        ax.annotate(rf"$x_{i}$", point, xytext=offset, textcoords="offset points",
                    fontsize=22, color=blue, visible=(i == 0))
    labels = list(ax.texts)
    path, = ax.plot([], [], color=blue, lw=3)
    markers, = ax.plot([], [], "o", color=blue, ms=9)
    fps = 24
    writer = FFMpegWriter(fps=fps, codec="libx264",
                          extra_args=["-pix_fmt", "yuv420p", "-crf", "16",
                                      "-movflags", "+faststart"])
    with writer.saving(fig, ASSETS / "stopped-solve.mp4", dpi=fig.dpi):
        for step in range(2):
            for frame in range(fps * 2):
                # Hold each iterate for half a second before moving.
                t = np.clip((frame - fps / 2) / fps, 0, 1)
                tip = (1 - t) * points[step] + t * points[step + 1]
                path.set_data(*np.array([*points[:step + 1], tip]).T)
                arrived = step + int(t == 1)
                markers.set_data(*np.array(points[:arrived + 1]).T)
                labels[arrived].set_visible(True)
                writer.grab_frame()

    ax.annotate("", xy=solution, xytext=points[-1], arrowprops=dict(
        arrowstyle="-|>", lw=3, color="#ad491c", mutation_scale=24,
        shrinkA=4, shrinkB=8))
    ax.plot(*solution, marker="*", color="#ad491c", ms=17)
    ax.annotate(r"$x^\star$", solution, xytext=(-14, 15), textcoords="offset points",
                fontsize=22, color="#ad491c")
    fig.savefig(ASSETS / "stopped-solve-reveal.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
