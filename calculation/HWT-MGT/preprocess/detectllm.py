"""DetectLLM-specific preprocessing defaults."""

from detectgpt import load_models as _load_models, perturb_texts
from common import load_causal_model_tokenizer, tokenize_texts


BASE_MODEL = "gpt2-medium"
MASK_MODEL = "t5-small"


def load_models(base_model_name: str = BASE_MODEL, mask_model_name: str = MASK_MODEL,
                cache_dir: str | None = None, device: str | None = None):
    return _load_models(base_model_name, mask_model_name, cache_dir, device)


def prepare_base_text(text: str, tokenizer, device: str | None = None):
    # DetectLLM's base scorer does not specify truncation or padding.
    return tokenize_texts(text, tokenizer, truncation=False, padding=False, device=device)


__all__ = ["BASE_MODEL", "MASK_MODEL", "load_models", "prepare_base_text", "perturb_texts"]
