"""Mean word length in characters."""
from common import safe_div


def mean_word_length(word_tokens):
    words = list(word_tokens)
    return safe_div(sum(len(word) for word in words), len(words))
