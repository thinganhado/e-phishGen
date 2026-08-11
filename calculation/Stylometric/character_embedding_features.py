"""Calculation-only character embedding operation.

The embedding matrix and integer character IDs must be supplied by the caller;
vocabulary creation, lowercasing, truncation, padding, and model loading are
preprocessing/model steps and are intentionally excluded.
"""


def character_embedding(token_ids, embedding_matrix):
    """Return the embedding vector for every supplied character ID."""
    return [embedding_matrix[int(token_id)] for token_id in token_ids]
