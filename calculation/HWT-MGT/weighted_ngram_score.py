"""Weighted DNA-GPT N-gram overlap score."""

import math

from ngram_overlap_ratio import ngram_overlap_ratio


def weighted_ngram_score(target_tokens, generated_tokens, min_n=1, max_n=24):
    ratios = [ngram_overlap_ratio(target_tokens, generated_tokens, n) for n in range(min_n, max_n + 1)]
    nonzero = [n for n, ratio in zip(range(min_n, max_n + 1), ratios) if n > 3 and ratio != 0]
    if not nonzero:
        return 0.0
    numerator = sum(n * math.log(n) * ratio for n, ratio in zip(range(min_n, max_n + 1), ratios) if n > 3)
    return numerator / sum(nonzero)
