"""DetectLLM Normalized Log-Rank Perturbation."""

import torch


def npr(original_log_rank, perturbed_log_ranks):
    if original_log_rank == 0:
        raise ValueError("original_log_rank must not be zero")
    return float(torch.as_tensor(perturbed_log_ranks, dtype=torch.float32).mean().item() / original_log_rank)
