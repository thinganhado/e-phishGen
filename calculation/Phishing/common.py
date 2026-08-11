"""Shared calculation helpers for the 17 phishing stylometric metrics."""


def safe_div(numerator, denominator):
    return numerator / float(denominator) if denominator else 0.0


def require_nonempty(values, name="values"):
    values = list(values)
    if not values:
        raise ValueError("%s must not be empty" % name)
    return values
