"""DNA-GPT regeneration log-probability score."""

import torch

from common import require_nonempty, scalar


def dna_gpt_score(original_continuation_log_prob, regenerated_log_probs):
    """Return original continuation log-probability minus regenerated mean."""
    original = torch.as_tensor(original_continuation_log_prob, dtype=torch.float32)
    regenerated = require_nonempty(regenerated_log_probs, "regenerated_log_probs")
    return scalar(original - regenerated.mean())
