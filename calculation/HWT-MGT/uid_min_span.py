"""Variance of the minimum-variance complete UID span."""

import torch

from common import require_nonempty, scalar


def uid_span_candidates(surprisal, span_size=50):
    values = require_nonempty(surprisal, "surprisal")
    if span_size <= 0 or values.numel() < span_size:
        raise ValueError("surprisal must contain at least one complete span")
    spans = [values[i:i + span_size] for i in range(0, values.numel(), span_size) if values[i:i + span_size].numel() == span_size]
    spans = torch.stack(spans)
    variances = spans.var(dim=1, unbiased=False)
    return spans, variances


def uid_min_span(surprisal, span_size=50):
    spans, variances = uid_span_candidates(surprisal, span_size)
    return spans[variances.argmin()]
