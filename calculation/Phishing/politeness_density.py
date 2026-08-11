"""Politeness dictionary density per 100 words."""
from common import safe_div

POLITENESS_TERMS = {"please", "kindly", "thank", "thanks", "appreciate", "appreciated", "would", "could", "may", "regards", "sincerely", "respectfully"}


def politeness_density(match_count, word_count):
    return safe_div(match_count * 100, word_count)
