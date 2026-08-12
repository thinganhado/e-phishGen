"""GPT-Who CSV/model preparation.

Adapted from ``gpt-who/get_uid_features.py``. This adapter stops after
producing token-level surprisals so the UID aggregate metrics stay in the
calculation modules.
"""

from __future__ import annotations

import csv
from pathlib import Path


DEFAULT_MODEL = "gpt2-xl"


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def load_model(model_name: str = DEFAULT_MODEL, cache_path: str | None = None, device: str = "cuda"):
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    kwargs = {} if cache_path is None else {"cache_dir": cache_path}
    tokenizer = GPT2Tokenizer.from_pretrained(model_name, **kwargs)
    model = GPT2LMHeadModel.from_pretrained(model_name, **kwargs).to(device)
    tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    return model, tokenizer


def prepare_text(text: str, tokenizer):
    import torch
    # Original GPT-Who prepends the tokenizer EOS token before scoring.
    # GPT-2-family models have a 1024-token context window.  The old adapter
    # allowed longer inputs through, which can trigger a CUDA device assert.
    encoded = tokenizer(
        tokenizer.eos_token + text,
        return_tensors="pt",
        truncation=True,
        max_length=1024,
    )
    return {key: value for key, value in encoded.items()}


def token_surprisals(text: str, model, tokenizer, device: str = "cuda"):
    """Return the raw positive surprisal vector used by UID features."""
    import torch
    import torch.nn.functional as F
    encoded = {key: value.to(device) for key, value in prepare_text(text, tokenizer).items()}
    with torch.no_grad():
        logits = model(**encoded).logits[0]
    labels = encoded["input_ids"][0]
    log_probs = F.log_softmax(logits[:-1], dim=-1)
    return (-log_probs.gather(1, labels[1:, None]).squeeze(1)).cpu()


__all__ = ["DEFAULT_MODEL", "load_model", "prepare_text", "read_csv", "token_surprisals"]
