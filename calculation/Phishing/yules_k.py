"""Yule's K vocabulary-concentration statistic."""


def yules_k(token_frequencies):
    counts = list(token_frequencies.values())
    n = sum(counts)
    if n <= 0:
        return 0.0
    m2 = sum(frequency * frequency for frequency in counts)
    return 10000.0 * (m2 - n) / (n * n)
