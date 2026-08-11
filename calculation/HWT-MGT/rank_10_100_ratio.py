"""Fraction of observed tokens with zero-based rank in [10, 100)."""

from common import observed_ranks, scalar


def rank_10_100_ratio(logits, labels):
    ranks = observed_ranks(logits, labels, one_based=False)
    return scalar(((ranks >= 10) & (ranks < 100)).float().mean())
