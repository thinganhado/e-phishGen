"""NOUN POS density over non-space tokens."""
from common import safe_div


def noun_ratio(pos_tags):
    tags = list(pos_tags)
    return safe_div(sum(tag == "NOUN" for tag in tags), len(tags))
