"""Call-to-action dictionary density per 100 words."""
from common import safe_div

CTA_TERMS = {"click", "tap", "open", "download", "install", "verify", "confirm", "update", "sign in", "login", "log in", "log-in", "sign-in", "register", "enroll", "submit", "complete", "review", "approve", "respond", "reply", "call", "contact", "follow", "visit", "go to", "proceed"}


def cta_density(match_count, word_count):
    return safe_div(match_count * 100, word_count)
