"""Hugging Face fixed-length perplexity input preparation.

Adapted from the Hugging Face perplexity documentation. This produces the
sliding-window input IDs and masked labels; perplexity remains in the
calculation module.
"""


DEFAULT_MODEL = "openai-community/gpt2-large"
DEFAULT_STRIDE = 512


def load_model(model_name: str = DEFAULT_MODEL, cache_dir: str | None = None, device: str | None = None):
    from common import load_causal_model_tokenizer
    return load_causal_model_tokenizer(model_name, cache_dir=cache_dir, device=device)


def encode_text(text: str, tokenizer):
    return tokenizer(text, return_tensors="pt").input_ids


def sliding_windows(input_ids, max_length: int, stride: int = DEFAULT_STRIDE):
    """Yield ``(input_ids_window, labels_window)`` with context labels masked."""
    import torch
    if input_ids.ndim == 1:
        input_ids = input_ids.unsqueeze(0)
    sequence_length = input_ids.size(1)
    if sequence_length == 0:
        return
    previous_end = 0
    for begin in range(0, sequence_length, stride):
        end = min(begin + max_length, sequence_length)
        target_length = end - previous_end
        window = input_ids[:, begin:end]
        labels = window.clone()
        labels[:, :-target_length] = -100
        yield window, labels
        previous_end = end
        if end == sequence_length:
            break


def prepare_text(text: str, tokenizer, model_max_length: int, stride: int = DEFAULT_STRIDE):
    return list(sliding_windows(encode_text(text, tokenizer), model_max_length, stride))


__all__ = ["DEFAULT_MODEL", "DEFAULT_STRIDE", "encode_text", "load_model", "prepare_text", "sliding_windows"]
