"""Time-pressure dictionary density per 100 words."""
from common import safe_div

TIME_PRESSURE_TERMS = {"24 hours", "48 hours", "72 hours", "today", "tomorrow", "tonight", "within", "before", "by end of", "deadline", "expires", "expire", "expiring", "expired", "closing", "closes", "soon", "shortly", "immediately", "asap"}


def time_pressure_density(match_count, word_count):
    return safe_div(match_count * 100, word_count)
