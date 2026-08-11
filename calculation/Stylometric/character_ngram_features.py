"""Calculation for continuous character n-gram representations.

Input is an already encoded character sequence. Vocabulary learning and
padding belong in preprocessing/model code and are intentionally absent.
"""


def character_ngrams(character_ids, n_values=(2, 3, 4)):
    """Return contiguous n-gram ID tuples and their frequencies."""
    sequence = list(character_ids)
    return {
        int(n): [tuple(sequence[i:i + n]) for i in range(len(sequence) - n + 1)]
        for n in n_values
        if n > 0
    }


def ngram_presence_vector(character_ids, vocabulary):
    """Return a binary vector for a supplied, already-fitted n-gram vocabulary."""
    sequence = list(character_ids)
    return [int(any(tuple(sequence[i:i + len(ngram)]) == tuple(ngram)
                    for i in range(max(0, len(sequence) - len(ngram) + 1))))
            for ngram in vocabulary]
