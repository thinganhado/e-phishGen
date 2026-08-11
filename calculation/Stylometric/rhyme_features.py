"""RhymeTagger calculations from supplied IPA components and probabilities."""


def final_character_ngram(word, n=3):
    return word[-n:] if len(word) >= n else word


def rhyme_score(component_pairs, probability_lookup, length1, length2, length_penalty=0.0):
    """Calculate the RhymeTagger component-pair score."""
    length_coef = 1.0 - length_penalty if length1 % 2 != length2 % 2 else 1.0
    if not component_pairs:
        return length_coef
    p_product = 1.0
    q_product = 1.0
    for index, pair in enumerate(component_pairs):
        key = tuple(sorted(pair))
        if key in probability_lookup.get(index, {}):
            probability = probability_lookup[index][key]
        elif pair[0] == pair[1]:
            probability = 0.99
        else:
            probability = 0.0001
        p_product *= probability
        q_product *= 1.0 - probability
    return length_coef * p_product / float(p_product + q_product) if p_product + q_product else 0.0


def ngram_rhyme_score(ngram1, ngram2, probability_lookup, length1, length2, length_penalty=0.0):
    length_coef = 1.0 - length_penalty if length1 % 2 != length2 % 2 else 1.0
    key = tuple(sorted((ngram1, ngram2)))
    if key in probability_lookup:
        return probability_lookup[key] * length_coef
    return (0.99 if ngram1 == ngram2 else 0.0001) * length_coef


def rhyme_detected(score, threshold=0.95):
    return score > threshold
