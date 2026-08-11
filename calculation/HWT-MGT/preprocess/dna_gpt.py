"""DNA-GPT input and continuation-prompt preparation.

Adapted from ``DNA-GPT-dist.py`` and ``openai_generate/utils.py``. API calls
are intentionally not made here; the output is a set of prompts for the
chosen OpenAI-compatible generation client.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


def read_jsonl(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def truncate_words(text: str, max_words: int = 350) -> str:
    words = text.split()
    return text if len(words) <= max_words else " ".join(words[:max_words])


def build_prompt(text: str, max_words: int = 350, truncate_ratio: float = 0.5) -> dict[str, str]:
    text = truncate_words(text, max_words)
    cut = int(truncate_ratio * len(text))
    return {"text": text, "prefix": text[:cut], "continuation": text[cut:]}


def tokenize_for_ngrams(text: str, stemmer=None, stopwords: set[str] | None = None) -> list[str]:
    """Match DNA-GPT's lowercase/non-alphanumeric/Porter-stemming path."""
    text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    tokens = re.split(r"\s+", text)
    stopwords = stopwords or set()
    if stemmer is None:
        try:
            from nltk.stem.porter import PorterStemmer
            stemmer = PorterStemmer()
        except ImportError:
            stemmer = None
    if stemmer:
        tokens = [stemmer.stem(token) if len(token) > 3 else token
                  for token in tokens if token not in stopwords]
    return [token for token in tokens if re.fullmatch(r"[a-z0-9]+", token)]


def prepare_records(records: list[dict], text_column: str = "text", max_words: int = 350,
                    truncate_ratio: float = 0.5) -> list[dict[str, str]]:
    return [build_prompt(str(record[text_column]), max_words, truncate_ratio) for record in records]


__all__ = ["build_prompt", "prepare_records", "read_jsonl", "tokenize_for_ngrams", "truncate_words"]
