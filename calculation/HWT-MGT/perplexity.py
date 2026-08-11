"""Perplexity from already-calculated token log-probabilities or NLLs."""

import math

import torch

from common import require_nonempty


def perplexity_from_log_probs(log_probs):
    """Return ``exp(-mean(log_probs))``."""
    return math.exp(float(-require_nonempty(log_probs).mean().item()))


def perplexity_from_nll(nll, token_count=None):
    """Return perplexity from summed or per-token negative log-likelihood."""
    nll = require_nonempty(nll, "nll")
    if token_count is None:
        mean_nll = nll.mean()
    else:
        if token_count <= 0:
            raise ValueError("token_count must be positive")
        mean_nll = nll.sum() / token_count
    return math.exp(float(mean_nll.item()))
