"""GPT-Who UID variance."""

from common import require_nonempty, scalar


def uid_variance(surprisal):
    values = require_nonempty(surprisal, "surprisal")
    return scalar(((values - values.mean()) ** 2).sum() / values.numel())
