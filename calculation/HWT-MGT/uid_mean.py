"""GPT-Who mean token surprisal."""

from common import require_nonempty, scalar


def uid_mean(surprisal):
    return scalar(require_nonempty(surprisal, "surprisal").mean())
