"""Sampling and analytic Fast-DetectGPT criteria."""

import torch

from common import aligned_logits_labels, scalar


def sampling_discrepancy(logits_reference, logits_scoring, labels, samples):
    """Score reference-sampled token sequences with a scoring model."""
    _, labels = aligned_logits_labels(logits_scoring, labels)
    score_log_probs = torch.log_softmax(torch.as_tensor(logits_scoring).float(), -1)
    if score_log_probs.ndim == 3:
        score_log_probs = score_log_probs[0]
    observed = score_log_probs.gather(-1, labels[:, None]).squeeze(-1).mean()
    samples = torch.as_tensor(samples, dtype=torch.long)
    if samples.ndim == 3 and samples.shape[0] == 1:
        samples = samples[0]
    if samples.ndim != 2:
        raise ValueError("samples must have shape [T, S] or [1, T, S]")
    sampled = score_log_probs.gather(-1, samples).mean(dim=0)
    return scalar((observed - sampled.mean()) / sampled.std(unbiased=True))


def analytic_sampling_discrepancy(logits_reference, logits_scoring, labels):
    """Calculate Fast-DetectGPT's reference-expectation criterion."""
    score, labels = aligned_logits_labels(logits_scoring, labels)
    reference = torch.as_tensor(logits_reference).float()
    if reference.ndim == 3 and reference.shape[0] == 1:
        reference = reference[0]
    if reference.shape[-1] != score.shape[-1]:
        vocabulary = min(reference.shape[-1], score.shape[-1])
        reference, score = reference[:, :vocabulary], score[:, :vocabulary]
        labels = labels.clamp_max(vocabulary - 1)
    score_log_probs = torch.log_softmax(score, -1)
    reference_probs = torch.softmax(reference, -1)
    observed = score_log_probs.gather(-1, labels[:, None]).squeeze(-1)
    mean = (reference_probs * score_log_probs).sum(-1)
    variance = (reference_probs * score_log_probs.square()).sum(-1) - mean.square()
    return scalar((observed.sum() - mean.sum()) / variance.sum().clamp_min(1e-12).sqrt())
