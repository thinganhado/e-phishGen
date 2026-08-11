"""Fast-DetectGPT's negative average log-rank convention."""

from mean_log_rank import mean_log_rank


def negative_mean_log_rank(logits, labels):
    return -mean_log_rank(logits, labels, one_based=True)
