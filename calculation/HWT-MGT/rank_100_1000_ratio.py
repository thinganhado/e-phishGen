"""Fraction of observed tokens with zero-based rank in [100, 1000)."""

from common import observed_ranks, scalar


def rank_100_1000_ratio(logits, labels):
    ranks = observed_ranks(logits, labels, one_based=False)
    return scalar(((ranks >= 100) & (ranks < 1000)).float().mean())
