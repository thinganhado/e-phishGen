"""Small calculation helpers shared by HWT/MGT metric modules.

Inputs are expected to be preprocessed already. In particular, this module
does not tokenize text, load models, or read files.
"""

import math

import torch


def logits_2d(logits):
    """Return logits as ``[time, vocabulary]`` for a single sequence."""
    logits = torch.as_tensor(logits)
    if logits.ndim == 3 and logits.shape[0] == 1:
        logits = logits[0]
    if logits.ndim != 2:
        raise ValueError("logits must have shape [T, V] or [1, T, V]")
    return logits.float()


def labels_1d(labels):
    """Return labels as ``[time]`` for a single sequence."""
    labels = torch.as_tensor(labels, dtype=torch.long)
    if labels.ndim == 2 and labels.shape[0] == 1:
        labels = labels[0]
    if labels.ndim != 1:
        raise ValueError("labels must have shape [T] or [1, T]")
    return labels


def aligned_logits_labels(logits, labels):
    logits = logits_2d(logits)
    labels = labels_1d(labels)
    if logits.shape[0] != labels.shape[0]:
        raise ValueError("logits and labels must have the same number of positions")
    return logits, labels


def observed_log_probs(logits, labels):
    logits, labels = aligned_logits_labels(logits, labels)
    return torch.log_softmax(logits, dim=-1).gather(1, labels[:, None]).squeeze(1)


def observed_ranks(logits, labels, one_based=True):
    """Return descending-probability ranks of observed labels."""
    logits, labels = aligned_logits_labels(logits, labels)
    order = torch.argsort(logits, dim=-1, descending=True)
    matches = order.eq(labels[:, None])
    if not matches.all(dim=1).all():
        raise ValueError("every observed label must be present in the vocabulary")
    ranks = matches.float().argmax(dim=1)
    return ranks + 1 if one_based else ranks


def finite_mean(values):
    values = torch.as_tensor(values, dtype=torch.float32)
    values = values[torch.isfinite(values)]
    if values.numel() == 0:
        raise ValueError("cannot calculate a mean from no finite values")
    return values.mean()


def scalar(value):
    return float(torch.as_tensor(value).detach().cpu().item())


def require_nonempty(values, name="values"):
    values = torch.as_tensor(values, dtype=torch.float32)
    if values.numel() == 0:
        raise ValueError(f"{name} must not be empty")
    return values.flatten()


def require_same_length(a, b):
    if len(a) != len(b):
        raise ValueError("inputs must have the same length")


def safe_std(values):
    values = require_nonempty(values)
    if values.numel() < 2:
        raise ValueError("at least two values are required to calculate a standard deviation")
    return values.std(unbiased=True)


def log_or_zero(probabilities):
    probabilities = torch.as_tensor(probabilities, dtype=torch.float32)
    return torch.where(probabilities > 0, probabilities * torch.log(probabilities), torch.zeros_like(probabilities))


__all__ = [
    "aligned_logits_labels", "finite_mean", "labels_1d", "log_or_zero",
    "logits_2d", "observed_log_probs", "observed_ranks", "require_nonempty",
    "require_same_length", "safe_std", "scalar",
]
