"""Average observed next-token log-probability."""

from common import finite_mean, observed_log_probs, scalar


def average_log_probability(logits, labels):
    """Calculate ``mean(log p(label_t | context_t))``."""
    return scalar(finite_mean(observed_log_probs(logits, labels)))
