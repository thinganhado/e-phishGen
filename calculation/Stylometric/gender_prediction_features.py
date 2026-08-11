"""Calculation-only implementation of the GenderPrediction-JAVA features.

The functions accept the text/tags/tokens after any project-specific input
selection has been completed. They do not tokenize or run a POS tagger.
"""

import re
from collections import Counter
from math import log

from stylometric_common import mean, safe_div


def syntactic_counts(text):
    groups = {
        "apostrophe": "'’",
        "brackets": "[](){}<>",
        "colon": ":",
        "comma": ",",
        "dash": "-",
        "ellipsis": "…",
        "exclamation": "!",
        "full_stop": ".",
        "question_mark": "?",
        "semicolon": ";",
        "slash": "/\\",
    }
    result = {name: sum(text.count(char) for char in chars) for name, chars in groups.items()}
    result["ellipsis"] += int("..." in text)
    return result


def pos_counts(pos_tags):
    tags = list(pos_tags)
    groups = {
        "nouns": {"NN", "NNS", "NNP", "NNPS"},
        "adjectives": {"JJ", "JJR"},
        "adverbs": {"RB", "RBS", "RBR"},
        "verbs": {"VB", "VBD", "VBG", "VBN", "VBP", "VBZ"},
        "cardinal_numbers": {"CD"}, "prepositions": {"IN", "TO"},
        "particles": {"RP"}, "symbols": {"SYM"}, "conjunctions": {"CC"},
        "determiners": {"DT"}, "interrogatives": {"WDT", "WP", "WRB"},
        "foreign_words": {"FW"}, "possessive_pronouns": {"PRP$"},
    }
    return {name: sum(tag in accepted for tag in tags) for name, accepted in groups.items()}


def pos_density(pos_tags, n):
    tags = list(pos_tags)
    grams = [tuple(tags[i:i + n]) for i in range(len(tags) - n + 1)]
    return safe_div(len(set(grams)), len(grams), "POS n-gram count") * 100.0


def surface_features(text, sentence_tokens=None):
    """Calculate character/surface values using source-compatible definitions."""
    denominator = len(text.replace("\r", "").replace("\n", ""))
    if denominator == 0:
        raise ValueError("character denominator must be non-zero")
    tokens = list(sentence_tokens) if sentence_tokens is not None else []
    sentence_count = sum(any(mark in token for mark in ".?!") for token in tokens)
    special = len(re.findall(r"[^A-Za-z0-9\\s]", text))
    digits = sum(char.isdigit() for char in text)
    letters = sum(('A' <= char <= 'Z') or ('a' <= char <= 'z') for char in text)
    uppercase = sum('A' <= char <= 'Z' for char in text)
    result = {
        "character_count": denominator,
        "character_count_without_spaces": len(text.replace("\r", "").replace("\n", "").replace(" ", "")),
        "digit_ratio": 100.0 * digits / denominator,
        "letter_ratio": 100.0 * letters / denominator,
        "uppercase_ratio": 100.0 * uppercase / denominator,
        "whitespace_ratio": 100.0 * text.count(" ") / denominator,
        "tab_ratio": 100.0 * text.count("\t") / denominator,
        "special_character_ratio": 100.0 * special / denominator,
        "uppercase_count": uppercase,
        "digit_count": digits,
        "space_count": text.count(" "),
        "tab_count": text.count("\t"),
        "punctuation_percentage": 100.0 * sum(char in '\\";:!.,' for char in text) / denominator,
        "semicolon_percentage": 100.0 * text.count(";") / denominator,
        "comma_percentage": 100.0 * text.count(",") / denominator,
    }
    result["question_sentence_percentage"] = 100.0 * sum("?" in token for token in tokens) / sentence_count if sentence_count else 0.0
    return result


def vocabulary_features(tokens, sentence_count, sentence_lengths=None, character_count=None):
    words = list(tokens)
    frequencies = Counter(words)
    total = len(words)
    vocabulary = len(frequencies)
    result = {
        "total_words": total,
        "total_unique_words": vocabulary,
        "hapax_legomena": sum(value == 1 for value in frequencies.values()),
        "average_word_length": safe_div(character_count if character_count is not None else sum(len(word) for word in words), total, "word count"),
        "ratio_short_words": 100.0 * sum(len(word) <= 3 for word in words) / total,
    }
    if sentence_lengths is not None:
        result["average_sentence_length_characters"] = mean(sentence_lengths)
    result["average_sentence_length_words"] = safe_div(total, sentence_count, "sentence count")
    s2 = sum((frequency ** 2) * sum(value == frequency for value in frequencies.values()) for frequency in frequencies.values())
    result["yule_k"] = 10000.0 * (s2 - total) / (total ** 2)
    result["simpson_d"] = sum(value * (frequency / float(total)) * ((frequency - 1) / float(total - 1)) for frequency, value in Counter(frequencies.values()).items()) if total > 1 else 0.0
    result["sichel_s"] = safe_div(sum(value == 2 for value in frequencies.values()), vocabulary, "vocabulary")
    result["brunet_w"] = total ** (vocabulary ** -0.1654)
    v1 = result["hapax_legomena"]
    result["honore_r"] = 100.0 * log(total) / (1.0 - v1 / float(vocabulary)) if vocabulary and v1 < vocabulary else 0.0
    return result
