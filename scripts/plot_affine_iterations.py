"""Regenerate the animated plot on displayed slide 14 (source slide-16)."""

from pathlib import Path

import matplotlib
import numpy as np
from PIL import Image

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "slide-16-1.gif"


def main():
    # Strict diagonal dominance guarantees Jacobi and Gauss-Seidel convergence.
    # A has eigenvalues 0.4 and 1.4, so the slide's unit Richardson step converges.
    A = np.array([[0.6, 0.4], [0.4, 1.2]])
    solution = np.array([2.0, 1.0])
    b = A @ solution
    start = np.zeros(2)
    identity = np.eye(2)

    # Each method takes the affine step x <- x + M^{-1}(b - Ax).
    methods = [
        ("Jacobi", np.diag(A.diagonal()), "#006995", "--", "o"),
        ("Richardson", identity, "#b44d12", "-", "^"),
        ("Gauss-Seidel", np.tril(A), "#745296", "-.", "s"),
    ]
    # At this plot scale all three paths reach the solution marker in 12 steps.
    steps = 12
    fig, ax = plt.subplots(figsize=(6.5, 5.8), dpi=150)
    fig.subplots_adjust(left=0.10, right=0.98, top=0.86, bottom=0.13)
    ax.set(xlim=(-0.25, 3.0), ylim=(-0.35, 2.3), aspect="equal",
           xlabel=r"$x_1$", ylabel=r"$x_2$", xticks=[0, 1, 2, 3], yticks=[0, 1, 2])
    ax.tick_params(labelsize=13, colors="#45545c", length=3)
    ax.xaxis.label.set_size(17)
    ax.yaxis.label.set_size(17)
    ax.spines[["right", "top"]].set_visible(False)
    for side in ("bottom", "left"):
        ax.spines[side].set_color("#82919a")

    # Contours of the quadratic energy above its minimum at the solution.
    xx, yy = np.meshgrid(np.linspace(*ax.get_xlim(), 300), np.linspace(*ax.get_ylim(), 250))
    dx, dy = xx - solution[0], yy - solution[1]
    energy = (A[0, 0] * dx**2 + 2 * A[0, 1] * dx * dy + A[1, 1] * dy**2) / 2
    ax.contour(xx, yy, energy, levels=[0.04, 0.16, 0.4, 0.8, 1.6, 2.6],
               colors="#d4dee2", linewidths=1)

    traces = []
    for name, M, color, style, marker in methods:
        radius = max(abs(np.linalg.eigvals(identity - np.linalg.solve(M, A))))
        if radius >= 1:
            raise ValueError(f"{name} does not converge (spectral radius {radius:g})")
        path = [start]
        for _ in range(steps):
            x = path[-1]
            path.append(x + np.linalg.solve(M, b - A @ x))
        line, = ax.plot([], [], linestyle=style, color=color, linewidth=2.2, label=name)
        head, = ax.plot([], [], marker=marker, color=color, markersize=6)
        traces.append((np.array(path), line, head))

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.04), ncol=3,
              fontsize=13, frameon=False, handlelength=1.8, columnspacing=0.9,
              handletextpad=0.4)
    ax.scatter(*start, s=36, color="#263844", zorder=5)
    ax.annotate("Start", start, xytext=(2, -18), textcoords="offset points", fontsize=13)
    ax.scatter(*solution, s=120, marker="*", color="#263844", edgecolor="white",
               linewidth=0.7, zorder=5)
    ax.annotate("Solution", solution, xytext=(10, 0), textcoords="offset points",
                fontsize=13, va="center", bbox=dict(facecolor="white", edgecolor="none", pad=1))

    # Use one palette throughout to keep the static contours and labels stable.
    for path, line, head in traces:
        line.set_data(path.T)
        head.set_data(path[-1:].T)
    fig.canvas.draw()
    palette = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())).convert("RGB").quantize()

    # Linear interpolation animates the connecting segments between solver iterates.
    # Sixteen 40 ms frames give every method 640 ms per iteration.
    frames_per_step = 16
    frame_ms = 40
    frames = []
    for frame in range(steps * frames_per_step + 1):
        k, subframe = divmod(frame, frames_per_step)
        for path, line, head in traces:
            trail = path[:k + 1]
            if subframe:
                fraction = subframe / frames_per_step
                point = path[k] + fraction * (path[k + 1] - path[k])
                trail = np.vstack((trail, point))
            line.set_data(trail.T)
            head.set_data(trail[-1:].T)
        fig.canvas.draw()
        rgb = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())).convert("RGB")
        frames.append(rgb.quantize(palette=palette, dither=Image.Dither.NONE))
    plt.close(fig)
    # Pause briefly at the endpoints of the loop.
    durations = [480] + [frame_ms] * (len(frames) - 2) + [1200]
    frames[0].save(OUTPUT, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=False)


if __name__ == "__main__":
    main()
