"""Matplotlib visualizations for within- and cross-dataset effect profiles."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Mapping, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _finite_effect(feature: Mapping[str, Any], variant: str, effect: str) -> float | None:
    try:
        value = feature["variants"][variant]["contrasts"][effect]["standardized"]["estimate"]
    except (KeyError, TypeError):
        return None
    return float(value) if value is not None and math.isfinite(float(value)) else None


def plot_within_effect_heatmap(
    features: Sequence[Mapping[str, Any]],
    output: Path,
    variant: str,
    max_features: int = 50,
) -> None:
    scored = []
    for feature in features:
        values = [_finite_effect(feature, variant, effect) for effect in ("G", "P", "I")]
        finite = [abs(value) for value in values if value is not None]
        if finite:
            scored.append((max(finite), feature, values))
    selected = sorted(scored, key=lambda item: item[0], reverse=True)[:max_features]
    if not selected:
        return
    selected.reverse()
    matrix = np.asarray(
        [[np.nan if value is None else value for value in item[2]] for item in selected],
        dtype=float,
    )
    labels = [f"{item[1]['family']}:{item[1]['name']}" for item in selected]
    limit = max(0.2, float(np.nanpercentile(np.abs(matrix), 95)))
    height = max(5.0, 0.28 * len(labels) + 1.5)
    figure, axis = plt.subplots(figsize=(8.5, height))
    image = axis.imshow(matrix, aspect="auto", cmap="coolwarm", vmin=-limit, vmax=limit)
    axis.set_xticks(range(3), ["Generation (G)", "Phishing (P)", "Interaction (I)"])
    axis.set_yticks(range(len(labels)), labels, fontsize=8)
    axis.set_title(f"Signed standardized effects ({variant.replace('_', ' ')})")
    if len(labels) <= 25:
        for row in range(matrix.shape[0]):
            for column in range(matrix.shape[1]):
                if math.isfinite(matrix[row, column]):
                    axis.text(
                        column,
                        row,
                        f"{matrix[row, column]:+.2f}",
                        ha="center",
                        va="center",
                        fontsize=7,
                        color="black",
                    )
    figure.colorbar(image, ax=axis, label="Hedges-standardized adjusted contrast")
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)


def plot_top_interactions(
    features: Sequence[Mapping[str, Any]],
    output: Path,
    variant: str,
    count: int = 12,
) -> None:
    scored = []
    for feature in features:
        interaction = _finite_effect(feature, variant, "I")
        means = feature.get("variants", {}).get(variant, {}).get("adjusted_means")
        if interaction is not None and isinstance(means, Mapping):
            scored.append((abs(interaction), interaction, feature, means))
    selected = sorted(scored, key=lambda item: item[0], reverse=True)[:count]
    if not selected:
        return
    columns = 3
    rows = math.ceil(len(selected) / columns)
    figure, axes = plt.subplots(rows, columns, figsize=(4.6 * columns, 3.4 * rows), squeeze=False)
    for axis, (_, interaction, feature, means) in zip(axes.flat, selected):
        x = np.asarray([0.0, 1.0])
        axis.plot(x, [means["HW-B"], means["MG-B"]], "o-", label="Benign")
        axis.plot(x, [means["HW-P"], means["MG-P"]], "o-", label="Phishing")
        axis.set_xticks(x, ["Human", "Machine"])
        axis.set_title(f"{feature['family']}:{feature['name']}\nI={interaction:+.2f}", fontsize=9)
        axis.grid(alpha=0.2)
    for axis in axes.flat[len(selected) :]:
        axis.set_visible(False)
    handles, labels = axes.flat[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="upper center", ncol=2)
    figure.suptitle("Largest standardized interactions: adjusted four-cell means", y=1.01)
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)


def plot_dataset_feature_heatmap(
    matrix: np.ndarray,
    datasets: Sequence[str],
    features: Sequence[str],
    effect: str,
    output: Path,
    max_features: int = 50,
) -> None:
    matrix = np.asarray(matrix, dtype=float)
    if matrix.size == 0:
        return
    scores = np.nanmedian(np.abs(matrix), axis=0)
    order = np.argsort(np.nan_to_num(scores, nan=-1.0))[::-1][:max_features]
    matrix = matrix[:, order]
    feature_labels = [features[index] for index in order]
    limit = max(0.2, float(np.nanpercentile(np.abs(matrix), 95)))
    figure, axis = plt.subplots(
        figsize=(max(7.0, 0.28 * len(feature_labels) + 2), max(4.0, 0.5 * len(datasets) + 2))
    )
    image = axis.imshow(matrix, aspect="auto", cmap="coolwarm", vmin=-limit, vmax=limit)
    axis.set_xticks(range(len(feature_labels)), feature_labels, rotation=90, fontsize=7)
    axis.set_yticks(range(len(datasets)), datasets)
    axis.set_title(f"Dataset-by-feature signed {effect} effects")
    figure.colorbar(image, ax=axis, label="Standardized effect")
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)


def plot_square_matrix(
    matrix: np.ndarray,
    labels: Sequence[str],
    title: str,
    output: Path,
    vmin: float = -1.0,
    vmax: float = 1.0,
) -> None:
    matrix = np.asarray(matrix, dtype=float)
    if matrix.size == 0:
        return
    size = max(5.0, 0.7 * len(labels) + 2)
    figure, axis = plt.subplots(figsize=(size, size))
    image = axis.imshow(matrix, cmap="coolwarm", vmin=vmin, vmax=vmax)
    axis.set_xticks(range(len(labels)), labels, rotation=45, ha="right")
    axis.set_yticks(range(len(labels)), labels)
    axis.set_title(title)
    if len(labels) <= 12:
        for row in range(len(labels)):
            for column in range(len(labels)):
                if math.isfinite(matrix[row, column]):
                    axis.text(column, row, f"{matrix[row, column]:.2f}", ha="center", va="center", fontsize=8)
    figure.colorbar(image, ax=axis)
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)

