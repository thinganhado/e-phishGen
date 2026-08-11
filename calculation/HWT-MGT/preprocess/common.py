"""Shared input readers and Hugging Face model helpers.

This file is preprocessing only. It does not calculate an HWT/MGT metric.
The model/tokenizer defaults are kept in the source-specific adapters.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable


def read_records(path: str | Path, text_column: str = "text", label_column: str = "label") -> list[dict[str, Any]]:
    """Read TXT, CSV, JSON, or JSONL into records without changing text."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            return list(csv.DictReader(stream))
    if suffix == ".jsonl":
        with path.open("r", encoding="utf-8") as stream:
            return [json.loads(line) for line in stream if line.strip()]
    if suffix == ".json":
        with path.open("r", encoding="utf-8") as stream:
            value = json.load(stream)
        if isinstance(value, list):
            return [item if isinstance(item, dict) else {text_column: item} for item in value]
        if isinstance(value, dict) and isinstance(value.get(text_column), list):
            texts = value[text_column]
            labels = value.get(label_column, [None] * len(texts))
            return [{text_column: text, label_column: label} for text, label in zip(texts, labels)]
        if isinstance(value, dict):
            return [value]
        return [{text_column: value}]
    with path.open("r", encoding="utf-8") as stream:
        return [{text_column: line.rstrip("\n")} for line in stream]


def read_texts(path: str | Path, text_column: str = "text") -> list[str]:
    return [str(record[text_column]) for record in read_records(path, text_column=text_column)]


def read_original_sampled(path: str | Path) -> dict[str, list[str]]:
    """Read the ``original``/``sampled`` JSON structure used by DetectGPT variants."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict) or not {"original", "sampled"}.issubset(data):
        raise ValueError("expected a JSON object with 'original' and 'sampled' lists")
    if len(data["original"]) != len(data["sampled"]):
        raise ValueError("original and sampled lists must have the same length")
    return {"original": list(data["original"]), "sampled": list(data["sampled"])}


def write_jsonl(records: Iterable[dict[str, Any]], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_causal_model_tokenizer(model_name: str, cache_dir: str | None = None, device: str | None = None):
    """MGTBench/DetectLLM-style causal model loading with PAD=EOS."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    kwargs = {} if cache_dir is None else {"cache_dir": cache_dir}
    model = AutoModelForCausalLM.from_pretrained(model_name, **kwargs)
    tokenizer = AutoTokenizer.from_pretrained(model_name, **kwargs)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    if device is not None:
        model.to(device)
    model.eval()
    return model, tokenizer


def tokenize_texts(texts: str | list[str], tokenizer, *, max_length: int | None = None,
                   truncation: bool = False, padding: bool | str = True, device: str | None = None):
    """Tokenize prepared text; no metric computation is performed."""
    import torch

    batch = [texts] if isinstance(texts, str) else texts
    kwargs = dict(return_tensors="pt", padding=padding, truncation=truncation)
    if max_length is not None:
        kwargs["max_length"] = max_length
    encoded = tokenizer(batch, **kwargs)
    if device is not None:
        encoded = {key: value.to(device) for key, value in encoded.items()}
    return encoded


def causal_next_token_inputs(encoded):
    """Return the source repositories' shifted logits/label shapes."""
    return encoded["input_ids"][:, 1:], encoded["input_ids"][:, :-1]


def save_torch(value, path: str | Path) -> None:
    import torch

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(value, path)


__all__ = [
    "causal_next_token_inputs", "load_causal_model_tokenizer", "read_original_sampled",
    "read_records", "read_texts", "save_torch", "tokenize_texts", "write_jsonl",
]
