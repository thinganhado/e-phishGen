"""Calculate source-defined time-pressure density."""

from common import safe_div


def time_pressure_density(match_count, alphabetic_word_count):
    """Return time-pressure dictionary matches per 100 alphabetic words."""
    return 100.0 * safe_div(match_count, alphabetic_word_count)

