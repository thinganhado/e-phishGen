"""Sentence-complexity calculations on pre-segmented sentences."""

from stylometric_common import mean, population_variance, safe_div


def sentence_length_features(sentence_lengths):
    lengths = list(sentence_lengths)
    return {"mean_sentence_length": mean(lengths), "variance_of_sentence_length": population_variance(lengths)}


def relative_clause_features(sentence_relative_clause_lengths, has_relative_clause):
    lengths = list(sentence_relative_clause_lengths)
    flags = list(has_relative_clause)
    sentence_count = len(flags)
    return {
        "mean_length_relative_clause": mean(lengths) if lengths else 0.0,
        "freq_sentence_with_relative_clause": safe_div(sum(flags), sentence_count, "sentence count"),
    }
