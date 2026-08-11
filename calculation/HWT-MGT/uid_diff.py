"""GPT-Who average absolute adjacent-surprisal difference."""

from common import require_nonempty, scalar


def uid_diff(surprisal):
    values = require_nonempty(surprisal, "surprisal")
    if values.numel() < 2:
        raise ValueError("at least two surprisal values are required")
    return scalar((values[1:] - values[:-1]).abs().sum() / values.numel())
