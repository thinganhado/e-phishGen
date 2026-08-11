"""Type-token ratio."""
from common import safe_div


def ttr(word_tokens):
    words = list(word_tokens)
    return safe_div(len(set(words)), len(words))
