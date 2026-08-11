"""DetectGPT perturbation curvature/discrepancy calculations."""

import torch

from common import require_nonempty, scalar, safe_std


def detectgpt_discrepancy(original_log_prob, perturbed_log_probs, normalized=False):
    """Calculate ``LL(original) - mean(LL(perturbed))`` or its z-score."""
    original = torch.as_tensor(original_log_prob, dtype=torch.float32)
    perturbed = require_nonempty(perturbed_log_probs, "perturbed_log_probs")
    difference = original - perturbed.mean()
    if normalized:
        difference = difference / safe_std(perturbed)
    return scalar(difference)
