"""URL density per 100 words."""
from common import safe_div


def url_density(url_count, word_count):
    return safe_div(url_count * 100, word_count)
