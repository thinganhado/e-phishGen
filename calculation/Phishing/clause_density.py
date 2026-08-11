"""Clause density from dependency labels."""
from common import safe_div

CLAUSE_DEPENDENCIES = {"ROOT", "ccomp", "advcl", "relcl", "xcomp"}


def clause_density(dependency_labels, sentence_count):
    count = sum(label in CLAUSE_DEPENDENCIES for label in dependency_labels)
    return safe_div(count, sentence_count)
