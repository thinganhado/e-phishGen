"""DetectGPT/DetectLLM masked-span preprocessing.

The masking, fill extraction, and fill application follow the original
``detect-gpt/run.py`` and ``DetectLLM/baselines/detectGPT.py`` helpers. These
functions prepare perturbed text; they do not calculate a detection score.
"""

from __future__ import annotations

import re

import numpy as np


MASK_PATTERN = re.compile(r"<extra_id_\d+>")


def load_models(base_model_name: str = "gpt2-medium", mask_model_name: str = "t5-large",
                cache_dir: str | None = None, device: str | None = None):
    import torch
    from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer

    kwargs = {} if cache_dir is None else {"cache_dir": cache_dir}
    base_model = AutoModelForCausalLM.from_pretrained(base_model_name, **kwargs)
    base_tokenizer = AutoTokenizer.from_pretrained(base_model_name, **kwargs)
    base_tokenizer.pad_token_id = base_tokenizer.eos_token_id
    mask_model = AutoModelForSeq2SeqLM.from_pretrained(mask_model_name, **kwargs)
    mask_tokenizer = AutoTokenizer.from_pretrained(mask_model_name, **kwargs)
    if device is not None:
        base_model.to(device)
        mask_model.to(device)
    base_model.eval()
    mask_model.eval()
    return base_model, base_tokenizer, mask_model, mask_tokenizer


def tokenize_and_mask(text: str, span_length: int = 2, pct_words_masked: float = 0.3,
                      buffer_size: int = 1, ceil_pct: bool = False, rng=None) -> str:
    tokens = text.split(" ")
    if len(tokens) <= span_length:
        raise ValueError("text must contain more words than span_length")
    rng = np.random if rng is None else rng
    n_spans = pct_words_masked * len(tokens) / (span_length + buffer_size * 2)
    n_spans = int(np.ceil(n_spans) if ceil_pct else n_spans)
    n_masks = 0
    while n_masks < n_spans:
        start = rng.randint(0, len(tokens) - span_length)
        end = start + span_length
        search_start = max(0, start - buffer_size)
        search_end = min(len(tokens), end + buffer_size)
        if "<<<mask>>>" not in tokens[search_start:search_end]:
            tokens[start:end] = ["<<<mask>>>"]
            n_masks += 1
    number = 0
    for index, token in enumerate(tokens):
        if token == "<<<mask>>>":
            tokens[index] = f"<extra_id_{number}>"
            number += 1
    return " ".join(tokens)


def count_masks(texts: list[str]) -> list[int]:
    return [sum(token.startswith("<extra_id_") for token in text.split()) for text in texts]


def fill_masked_texts(masked_texts: list[str], mask_model, mask_tokenizer, device: str | None = None,
                      mask_top_p: float = 1.0, max_length: int = 150) -> list[str]:
    import torch

    expected = count_masks(masked_texts)
    if not expected or max(expected) == 0:
        return list(masked_texts)
    stop_id = mask_tokenizer.encode(f"<extra_id_{max(expected)}>")[0]
    tokens = mask_tokenizer(masked_texts, return_tensors="pt", padding=True)
    if device is not None:
        tokens = {key: value.to(device) for key, value in tokens.items()}
    with torch.no_grad():
        outputs = mask_model.generate(**tokens, max_length=max_length, do_sample=True,
                                       top_p=mask_top_p, num_return_sequences=1,
                                       eos_token_id=stop_id)
    raw = mask_tokenizer.batch_decode(outputs, skip_special_tokens=False)
    raw = [item.replace("<pad>", "").replace("</s>", "").strip() for item in raw]
    fills = [[part.strip() for part in MASK_PATTERN.split(item)[1:-1]] for item in raw]
    words = [item.split(" ") for item in masked_texts]
    for tokens_i, fills_i, n_expected in zip(words, fills, expected):
        if len(fills_i) < n_expected:
            tokens_i[:] = []
            continue
        for fill_index in range(n_expected):
            tokens_i[tokens_i.index(f"<extra_id_{fill_index}>")] = fills_i[fill_index]
    return [" ".join(item) for item in words]


def perturb_texts(texts: list[str], mask_model, mask_tokenizer, span_length: int = 2,
                  pct_words_masked: float = 0.3, buffer_size: int = 1,
                  mask_top_p: float = 1.0, max_length: int = 150, device: str | None = None,
                  seed: int | None = None) -> list[str]:
    if seed is not None:
        np.random.seed(seed)
    masked = [tokenize_and_mask(text, span_length, pct_words_masked, buffer_size) for text in texts]
    return fill_masked_texts(masked, mask_model, mask_tokenizer, device, mask_top_p, max_length)


__all__ = ["count_masks", "fill_masked_texts", "load_models", "perturb_texts", "tokenize_and_mask"]
