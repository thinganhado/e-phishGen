"""GPT-Who total token surprisal."""

from common import require_nonempty, scalar


def total_surprisal(surprisal):
    return scalar(require_nonempty(surprisal, "surprisal").sum())
