"""Authority-appeal dictionary density per 100 words."""
from common import safe_div

AUTHORITY_TERMS = {"irs", "police", "fbi", "government", "tax authority", "court", "legal", "compliance", "audit", "regulator", "regulatory", "official", "administrator", "admin", "manager", "executive", "ceo", "director", "headquarters", "corporate", "department", "agency", "bureau"}


def authority_density(match_count, word_count):
    return safe_div(match_count * 100, word_count)
