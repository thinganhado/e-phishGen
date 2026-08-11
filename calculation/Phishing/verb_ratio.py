"""VERB POS density over non-space tokens."""
from common import safe_div


def verb_ratio(pos_tags):
    tags = list(pos_tags)
    return safe_div(sum(tag == "VERB" for tag in tags), len(tags))
