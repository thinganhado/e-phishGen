"""Pure calculation helpers for the stylometric metric scripts.

These helpers intentionally do not tokenize, normalize, read files, or load
models. Callers must provide the representation required by each metric.
"""

from collections import Counter
from math import log


def require_nonempty(values, name="values"):
    values = list(values)
    if not values:
        raise ValueError("%s must not be empty" % name)
    return values


def safe_div(numerator, denominator, name="denominator"):
    if denominator == 0:
        raise ValueError("%s must be non-zero" % name)
    return numerator / float(denominator)


def mean(values):
    values = require_nonempty(values)
    return sum(values) / float(len(values))


def population_variance(values):
    values = require_nonempty(values)
    average = mean(values)
    return sum((value - average) ** 2 for value in values) / float(len(values))


def entropy(probabilities, base=None):
    probabilities = require_nonempty(probabilities)
    result = 0.0
    for probability in probabilities:
        if probability > 0:
            result -= probability * log(probability)
    return result if base is None else result / log(base)


def normalized_counts(values):
    values = list(values)
    counts = Counter(values)
    total = sum(counts.values())
    if total == 0:
        return {key: 0.0 for key in counts}
    return {key: count / float(total) for key, count in counts.items()}
