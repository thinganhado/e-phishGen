"""Mean sentence length in non-space tokens."""
from common import safe_div


def mean_sentence_length(token_count, sentence_count):
    return safe_div(token_count, sentence_count)
