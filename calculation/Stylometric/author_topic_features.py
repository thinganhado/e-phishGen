"""Author-topic model calculations from Gibbs assignment counts."""


def author_topic_proportions(nak, naksum, alpha, topic_count=None):
    """Return theta[a][k] = (n_ak + alpha)/(n_a + K*alpha)."""
    if alpha < 0:
        raise ValueError("alpha must be non-negative")
    topic_count = topic_count or (len(nak[0]) if nak else 0)
    return [[(row[k] + alpha) / float(naksum[a] + topic_count * alpha) for k in range(topic_count)] for a, row in enumerate(nak)]


def topic_word_probabilities(nkw, nksum, beta, vocabulary_size=None):
    """Return phi[k][w] = (n_kw + beta)/(n_k + V*beta)."""
    vocabulary_size = vocabulary_size or (len(nkw[0]) if nkw else 0)
    return [[(row[w] + beta) / float(nksum[k] + vocabulary_size * beta) for w in range(vocabulary_size)] for k, row in enumerate(nkw)]


def topic_author_ranking(theta, top_n):
    """Return author indices ranked by each topic's theta value."""
    if not theta:
        return []
    topic_count = len(theta[0])
    return [sorted(range(len(theta)), key=lambda author: theta[author][topic], reverse=True)[:top_n] for topic in range(topic_count)]
