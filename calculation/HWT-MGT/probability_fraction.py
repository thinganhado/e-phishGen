"""Observed-token probability divided by top-1 probability."""

import torch

from common import aligned_logits_labels, scalar


def probability_fraction(logits, labels, reduction="mean"):
    logits, labels = aligned_logits_labels(logits, labels)
    probabilities = torch.softmax(logits, -1)
    observed = probabilities.gather(1, labels[:, None]).squeeze(1)
    fraction = observed / probabilities.max(dim=-1).values
    if reduction == "none":
        return fraction
    if reduction == "mean":
        return scalar(fraction.mean())
    raise ValueError("reduction must be 'none' or 'mean'")
