"""Mean observed-token rank."""

from common import observed_ranks, scalar


def mean_token_rank(logits, labels, one_based=True):
    return scalar(observed_ranks(logits, labels, one_based=one_based).float().mean())
