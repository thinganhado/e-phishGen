"""Mean natural-log observed-token rank."""

import torch

from common import observed_ranks, scalar


def mean_log_rank(logits, labels, one_based=True):
    ranks = observed_ranks(logits, labels, one_based=one_based).float()
    return scalar(torch.log(ranks).mean())
