"""Full-vocabulary predictive entropy."""

import torch

from common import logits_2d, scalar


def predictive_entropy(logits, reduction="mean"):
    """Calculate ``-sum(p log p)`` over the full vocabulary.

    ``reduction`` is ``"none"`` for one value per position or ``"mean"``
    for the text-level value used by MGTBench/DetectGPT.
    """
    logits = logits_2d(logits)
    entropy = -(torch.softmax(logits, -1) * torch.log_softmax(logits, -1)).sum(-1)
    if reduction == "none":
        return entropy
    if reduction == "mean":
        return scalar(entropy.mean())
    raise ValueError("reduction must be 'none' or 'mean'")
