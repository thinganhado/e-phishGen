"""MGTBench-compatible model and input preparation.

Adapted from ``MGTBench/methods/metric_based.py`` and ``methods/utils.py``.
"""

from common import load_causal_model_tokenizer, read_records, tokenize_texts


DEFAULT_MODEL = "gpt2-medium"


def load_model(model_name: str = DEFAULT_MODEL, cache_dir: str | None = None, device: str | None = None):
    return load_causal_model_tokenizer(model_name, cache_dir=cache_dir, device=device)


def prepare_text(text: str, tokenizer, metric: str):
    """Apply MGTBench's metric-specific context settings."""
    if metric in {"entropy", "predictive_entropy"}:
        return tokenize_texts(text, tokenizer, max_length=512, truncation=True, padding=True)
    if metric in {"ll", "average_log_probability", "rank", "logrank", "gltr"}:
        return tokenize_texts(text, tokenizer, max_length=1024, truncation=True, padding=True)
    raise ValueError(f"unknown MGTBench metric preparation: {metric}")


def prepare_file(path: str, metric: str, text_column: str = "text",
                 model_name: str = DEFAULT_MODEL, cache_dir: str | None = None,
                 device: str | None = None):
    """Read a MGTBench-style file and return records plus prepared token batches."""
    records = read_records(path, text_column=text_column)
    _, tokenizer = load_model(model_name, cache_dir=cache_dir, device=device)
    return records, [prepare_text(str(record[text_column]), tokenizer, metric) for record in records]


__all__ = ["DEFAULT_MODEL", "load_model", "prepare_file", "prepare_text"]
