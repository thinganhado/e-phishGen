"""Fast-DetectGPT's negative average rank convention."""

from mean_token_rank import mean_token_rank


def negative_mean_token_rank(logits, labels):
    return -mean_token_rank(logits, labels, one_based=True)
