"""Second-person pronoun ratio."""
from common import safe_div

SECOND_PERSON = {"you", "your", "yours", "yourself", "yourselves"}


def second_person_ratio(lower_words):
    words = list(lower_words)
    return safe_div(sum(word in SECOND_PERSON for word in words), len(words))
