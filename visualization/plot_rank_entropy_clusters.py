"""Visualize rank/entropy clusters for the four email groups."""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse


GROUPS = {
    "MG-B": ("machine", 0, "#4c78a8"),
    "MG-P": ("machine", 1, "#9467bd"),
    "HW-B": ("human", 0, "#2ca6a4"),
    "HW-P": ("human", 1, "#e76f51"),
}


def load_results(path):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        data = data.get("results", data.get("samples", data))
    return data


def add_ellipse(ax, x, y, color):
    if len(x) < 3:
        return
    covariance = np.cov(x, y)
    if not np.all(np.isfinite(covariance)):
        return
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = eigenvalues.argsort()[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
    angle = np.degrees(np.arctan2(*eigenvectors[:, 0][::-1]))
    # sqrt(chi2.ppf(.95, 2)) = 2.4477: approximate 95% bivariate ellipse.
    width, height = 2 * 2.4477 * np.sqrt(np.maximum(eigenvalues, 0))
    ellipse = Ellipse(
        (np.mean(x), np.mean(y)), width, height, angle=angle,
        facecolor=color, edgecolor=color, alpha=0.12, linewidth=2,
    )
    ax.add_patch(ellipse)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = load_results(args.input)
    groups = {}
    for group, (origin, label, color) in GROUPS.items():
        rows = [
            r for r in data
            if r.get("origin") == origin and int(r.get("phishing_label")) == label
            and r.get("average_rank_one_based") is not None
            and r.get("average_entropy_topk") is not None
        ]
        groups[group] = {
            "x": np.asarray([r["average_rank_one_based"] for r in rows], dtype=float),
            "y": np.asarray([r["average_entropy_topk"] for r in rows], dtype=float),
            "color": color,
        }

    fig, ax = plt.subplots(figsize=(12, 8), constrained_layout=True)
    for group, values in groups.items():
        x, y, color = values["x"], values["y"], values["color"]
        ax.scatter(x, y, s=28, alpha=0.48, color=color, edgecolors="none", label=f"{group} (n={len(x)})")
        ax.scatter(x.mean(), y.mean(), s=150, marker="X", color=color, edgecolor="black", linewidth=0.8, zorder=4)
        add_ellipse(ax, x, y, color)
        ax.annotate(group, (x.mean(), y.mean()), xytext=(7, 7), textcoords="offset points", fontsize=11, fontweight="bold")

    ax.set_xlabel("Average observed-token rank (1-based)", fontsize=12)
    ax.set_ylabel("Average top-10 entropy", fontsize=12)
    ax.set_title("Rank–entropy clusters by email origin and phishing label", fontsize=15, pad=14)
    ax.grid(alpha=0.22, linestyle=":")
    ax.legend(frameon=True, loc="best")
    fig.savefig(args.output, dpi=240, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
