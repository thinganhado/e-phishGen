"""Urgency dictionary density per 100 words."""
from common import safe_div

URGENCY_TERMS = {"urgent", "urgently", "immediately", "now", "asap", "today", "right away", "emergency", "critical", "important", "deadline", "expire", "expires", "expiring", "expired", "final", "last", "limited", "hurry", "quickly", "soon", "promptly"}


def urgency_density(match_count, word_count):
    return safe_div(match_count * 100, word_count)
