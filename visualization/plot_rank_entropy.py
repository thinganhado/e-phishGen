"""Create GLTR-style distribution figures for average rank and entropy."""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_auc_score


GROUPS = {
    "HW-B": ("human", 0),
    "HW-P": ("human", 1),
    "MG-B": ("machine", 0),
    "MG-P": ("machine", 1),
}
COLORS = {"HW-B": "#55b9b1", "HW-P": "#ed957e", "MG-B": "#7da5bd", "MG-P": "#9d72b8"}
PAIRS = [("HW-B", "MG-B"), ("HW-P", "MG-P"), ("HW-B", "HW-P"),
         ("MG-B", "MG-P"), ("HW-B", "MG-P"), ("HW-P", "MG-B")]


def load_metric(path, field):
    records = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    values = {key: [] for key in GROUPS}
    for record in records:
        for group, (origin, label) in GROUPS.items():
            if record.get("origin") == origin and record.get("phishing_label") == label:
                values[group].append(float(record[field]))
                break
    return values


def plot_metric(values, xlabel, title, output):
    figure, axes = plt.subplots(2, 3, figsize=(16, 9), constrained_layout=True)
    all_values = np.concatenate([np.asarray(v) for v in values.values()])
    bins = np.linspace(all_values.min(), all_values.max(), 19)

    for ax, (left, right) in zip(axes.ravel(), PAIRS):
        a, b = np.asarray(values[left]), np.asarray(values[right])
        labels = np.r_[np.zeros(len(a)), np.ones(len(b))]
        auc = roc_auc_score(labels, np.r_[a, b])
        delta = b.mean() - a.mean()
        ax.hist(a, bins=bins, density=True, alpha=.58, color=COLORS[left], edgecolor=COLORS[left], label=left)
        ax.hist(b, bins=bins, density=True, alpha=.58, color=COLORS[right], edgecolor=COLORS[right], label=right)
        ax.axvline(a.mean(), color=COLORS[left], linestyle="--", linewidth=1.5)
        ax.axvline(b.mean(), color=COLORS[right], linestyle="--", linewidth=1.5)
        ax.set_title(f"{left} vs {right}", fontsize=12, fontweight="bold")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Density")
        ax.grid(axis="y", alpha=.22, linestyle=":")
        ax.legend(frameon=False, fontsize=9)
        ax.text(.03, .96, f"AUROC ({right})={auc:.3f}\nΔ mean={delta:+.3f}",
                transform=ax.transAxes, va="top", fontsize=9,
                bbox=dict(facecolor="white", alpha=.78, edgecolor="#bbbbbb"))

    figure.suptitle(title, fontsize=15, y=1.02)
    figure.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(figure)
    print(f"Saved {output}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_metric(
        load_metric(args.input, "average_rank_one_based"),
        "Average observed-token rank (1-based)",
        "Average rank distributions across email origin and phishing label",
        output_dir / "rank_distributions.png",
    )
    plot_metric(
        load_metric(args.input, "average_entropy_topk"),
        "Average top-10 entropy",
        "Average top-10 entropy distributions across email origin and phishing label",
        output_dir / "entropy_distributions.png",
    )


if __name__ == "__main__":
    main()
