"""Fraction of observed tokens with zero-based rank at least 1000."""

from common import observed_ranks, scalar


def rank_gt1000_ratio(logits, labels):
    return scalar((observed_ranks(logits, labels, one_based=False) >= 1000).float().mean())
