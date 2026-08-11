"""First-person pronoun ratio."""
from common import safe_div

FIRST_PERSON = {"i", "me", "my", "mine", "we", "us", "our", "ours"}


def first_person_ratio(lower_words):
    words = list(lower_words)
    return safe_div(sum(word in FIRST_PERSON for word in words), len(words))
