"""Source-compatible imperative count."""


def imperative_count(sentence_first_tokens):
    """Count records whose first token is VB and ROOT or ccomp.

    Each record must provide ``tag`` and ``dep`` for the first non-space
    token. This preserves the source implementation's first-token rule.
    """
    return sum(record.get("tag") == "VB" and record.get("dep") in {"ROOT", "ccomp"}
               for record in sentence_first_tokens)
