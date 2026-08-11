"""Variance of the maximum-variance complete UID span."""

from uid_min_span import uid_span_candidates


def uid_max_span(surprisal, span_size=50):
    spans, variances = uid_span_candidates(surprisal, span_size)
    return spans[variances.argmax()]
