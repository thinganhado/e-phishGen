"""LDA-C topic features from already inferred arrays and assignments."""

from stylometric_common import entropy, safe_div


def normalize_gamma(gamma):
    total = sum(gamma)
    return [safe_div(value, total, "gamma sum") for value in gamma]


def document_topic_proportions(gamma):
    return normalize_gamma(gamma)


def topic_assignment_proportions(assignments, topic_count):
    counts = [0] * topic_count
    for topic in assignments:
        counts[int(topic)] += 1
    total = sum(counts)
    return [count / float(total) for count in counts] if total else [0.0] * topic_count


def topic_entropy(gamma, base=None):
    return entropy(normalize_gamma(gamma), base=base)


def dominant_topic_mass(gamma):
    return max(normalize_gamma(gamma))


def active_topic_count(gamma, epsilon):
    return sum(value >= epsilon for value in normalize_gamma(gamma))


def per_token_likelihood_bound(bound, token_count):
    return safe_div(bound, token_count, "token count")
