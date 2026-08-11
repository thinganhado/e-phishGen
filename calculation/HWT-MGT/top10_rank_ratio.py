"""Fraction of observed tokens with rank below 10."""

from common import observed_ranks, scalar


def top10_rank_ratio(logits, labels):
    return scalar((observed_ranks(logits, labels, one_based=False) < 10).float().mean())
