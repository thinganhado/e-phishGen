"""N-gram overlap calculations for DNA-GPT."""

from collections import Counter


def ngram_counts(tokens, n):
    if n <= 0:
        raise ValueError("n must be positive")
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def ngram_overlap_ratio(target_tokens, generated_tokens, n):
    target = ngram_counts(target_tokens, n)
    generated = ngram_counts(generated_tokens, n)
    denominator = max(sum(target.values()), 1)
    overlap = sum(min(count, generated.get(gram, 0)) for gram, count in target.items())
    return overlap / denominator
