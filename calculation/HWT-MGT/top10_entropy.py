"""Entropy over the top-10 predictive probabilities."""

import torch

from common import logits_2d, scalar


def top10_entropy(logits, k=10, reduction="mean"):
    """Renormalize the top-k probabilities and calculate Shannon entropy."""
    logits = logits_2d(logits)
    if k <= 0 or k > logits.shape[-1]:
        raise ValueError("k must be between 1 and the vocabulary size")
    top_logits = torch.topk(logits, k=k, dim=-1).values
    probabilities = torch.softmax(top_logits, dim=-1)
    entropy = -(probabilities * torch.log(probabilities.clamp_min(1e-12))).sum(-1)
    if reduction == "none":
        return entropy
    if reduction == "mean":
        return scalar(entropy.mean())
    raise ValueError("reduction must be 'none' or 'mean'")
