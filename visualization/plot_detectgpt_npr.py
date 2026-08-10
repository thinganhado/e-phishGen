"""Create DetectGPT and NPR distribution figures for the four email groups."""

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

COLORS = {
    "HW-B": "#55b9b1",
    "HW-P": "#ed957e",
    "MG-B": "#7da5bd",
    "MG-P": "#9d72b8",
}

PAIRS = [
    ("HW-B", "MG-B"),
    ("HW-P", "MG-P"),
    ("HW-B", "HW-P"),
    ("MG-B", "MG-P"),
    ("HW-B", "MG-P"),
    ("HW-P", "MG-B"),
]


def load_scores(path, field):
    records = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    scores = {}
    for record in records:
        group = next(
            name for name, (origin, label) in GROUPS.items()
            if record.get("origin") == origin and record.get("phishing_label") == label
        )
        scores.setdefault(group, []).append(float(record[field]))
    return scores


def plot_metric(scores, field, ylabel, output, title):
    fig, axes = plt.subplots(2, 3, figsize=(16, 9), constrained_layout=True)
    axes = axes.ravel()

    all_values = np.concatenate([np.asarray(v) for v in scores.values()])
    bins = np.linspace(all_values.min(), all_values.max(), 19)

    for ax, (left, right) in zip(axes, PAIRS):
        left_values = np.asarray(scores[left])
        right_values = np.asarray(scores[right])
        labels = np.r_[np.zeros(len(left_values)), np.ones(len(right_values))]
        values = np.r_[left_values, right_values]
        auc = roc_auc_score(labels, values)
        delta = right_values.mean() - left_values.mean()

        ax.hist(left_values, bins=bins, density=True, alpha=0.58, color=COLORS[left],
                edgecolor=COLORS[left], label=left)
        ax.hist(right_values, bins=bins, density=True, alpha=0.58, color=COLORS[right],
                edgecolor=COLORS[right], label=right)
        ax.axvline(left_values.mean(), color=COLORS[left], linestyle="--", linewidth=1.5)
        ax.axvline(right_values.mean(), color=COLORS[right], linestyle="--", linewidth=1.5)

        ax.set_title(f"{left} vs {right}", fontsize=12, fontweight="bold")
        ax.set_xlabel(ylabel)
        ax.set_ylabel("Density")
        ax.grid(axis="y", alpha=0.22, linestyle=":")
        ax.legend(frameon=False, fontsize=9)
        ax.text(
            0.03, 0.96,
            f"AUROC ({right})={auc:.3f}\nΔ mean={delta:+.3f}",
            transform=ax.transAxes,
            va="top",
            fontsize=9,
            bbox=dict(facecolor="white", alpha=0.78, edgecolor="#bbbbbb"),
        )

    fig.suptitle(title, fontsize=15, y=1.02)
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {output}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--detectgpt", required=True)
    parser.add_argument("--npr", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    detectgpt = load_scores(args.detectgpt, "detectgpt_score")
    npr = load_scores(args.npr, "npr")

    plot_metric(
        detectgpt,
        "detectgpt_score",
        "DetectGPT score (z)",
        output_dir / "detectgpt_score_distributions.png",
        "DetectGPT score distributions across email origin and phishing label",
    )
    plot_metric(
        npr,
        "npr",
        "NPR",
        output_dir / "npr_distributions.png",
        "NPR distributions across email origin and phishing label",
    )


if __name__ == "__main__":
    main()
