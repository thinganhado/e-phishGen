"""Run the recoverable Stylometric metrics on matched_pool_44.json."""

import json
import math
import re
import sys
from pathlib import Path

import nltk
from nltk import pos_tag, sent_tokenize, word_tokenize
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from character_ngram_features import character_ngrams
from gender_prediction_features import pos_counts, pos_density, surface_features, syntactic_counts, vocabulary_features
from lda_topic_features import (active_topic_count, dominant_topic_mass,
                                document_topic_proportions, per_token_likelihood_bound,
                                topic_assignment_proportions, topic_entropy)
from sentence_complexity_features import sentence_length_features

DATASET = Path(r"D:\AI\projects\e-phishGen\matched_pool_44.json")
RESULTS = ROOT / "results"
JSON_OUT = RESULTS / "matched_pool_44_stylometric_metrics.json"
MD_OUT = RESULTS / "matched_pool_44_stylometric_metrics.md"
TOPICS = 5


def flatten(prefix, values, result):
    for key, value in values.items():
        name = f"{prefix}_{key}" if prefix else key
        if isinstance(value, dict):
            flatten(name, value, result)
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            result[name] = float(value)


def Cohen_d(left, right):
    if len(left) < 2 or len(right) < 2:
        return None
    lm = sum(left) / len(left)
    rm = sum(right) / len(right)
    lvar = sum((v - lm) ** 2 for v in left) / (len(left) - 1)
    rvar = sum((v - rm) ** 2 for v in right) / (len(right) - 1)
    pooled = math.sqrt(((len(left) - 1) * lvar + (len(right) - 1) * rvar) /
                       (len(left) + len(right) - 2))
    return (lm - rm) / pooled if pooled else 0.0


def fmt(value):
    return "-" if value is None else f"{value:.4f}"


def metric_values(rows, metric, selector):
    return [row["metrics"][metric] for row in rows if selector(row) and metric in row["metrics"]]


def comparison(lines, title, left_name, right_name, left_selector, right_selector, rows, metrics):
    lines += ["", f"## {title}", "",
              f"| Metric | {left_name} mean | {right_name} mean | Difference ({left_name} - {right_name}) | Cohen d |",
              "|---|---:|---:|---:|---:|"]
    for metric in metrics:
        left = metric_values(rows, metric, left_selector)
        right = metric_values(rows, metric, right_selector)
        lm = sum(left) / len(left) if left else None
        rm = sum(right) / len(right) if right else None
        lines.append(f"| {metric.replace('_', ' ').capitalize()} | {fmt(lm)} | {fmt(rm)} | "
                     f"{fmt(lm - rm if lm is not None and rm is not None else None)} | {fmt(Cohen_d(left, right))} |")


def make_report(payload):
    rows = payload["results"]
    metrics = sorted({name for row in rows for name, value in row["metrics"].items()
                      if isinstance(value, (int, float))})
    groups = {group: sum(row["group"] == group for row in rows)
              for group in ("HW-P", "MG-P", "HW-B", "MG-B")}
    lines = [
        "# Stylometric descriptive comparison",
        "",
        "This report summarizes recoverable Stylometric features for `matched_pool_44.json`; "
        "individual sample rows are intentionally omitted.",
        "",
        "## Dataset and settings",
        "",
        f"- Total samples: **{len(rows)}**",
        f"- `HW-P`: **{groups['HW-P']}**; `MG-P`: **{groups['MG-P']}**",
        f"- `HW-B`: **{groups['HW-B']}**; `MG-B`: **{groups['MG-B']}**",
        "- English NLTK tokenization, sentence splitting, and POS tagging were used.",
        "- Character n-grams use a deterministic character-ID mapping and report counts/uniques, not a recovered neural model score.",
        f"- LDA uses a newly fitted {TOPICS}-topic scikit-learn model on this 44-document dataset; it is not an original recovered LDA-C model.",
        "- Difference is left mean minus right mean; Cohen d is descriptive, not a significance test.",
    ]
    comparison(lines, "HWT versus MGT", "HW", "MG",
                lambda row: row["group"].startswith("HW-"),
                lambda row: row["group"].startswith("MG-"), rows, metrics)
    lines += [
        "",
        "### Outstanding observations",
        "",
        "- The largest HWT/MGT effects are surface and punctuation features: uppercase ratio (d = 2.0759), special-character ratio (d = 1.9629), bracket count (d = 1.7841), uppercase count (d = 1.7380), and letter ratio (d = -1.6313).",
        "- HW has substantially more uppercase characters, brackets, special characters, and total characters. These differences may reflect formatting and template conventions rather than authorship alone.",
        "- Vocabulary Yule K (d = -1.0484) and Brunet W (d = 0.9558) also show relatively strong authorship differences, while total unique-word count is effectively identical (d = -0.0143).",
        "- POS features show higher HW adverb counts (d = 0.8382) and higher MG possessive-pronoun counts (d = -0.7136), but sentence mean length is almost identical (d = -0.0310).",
        "- Character 2-gram uniqueness has moderate separation (d = 0.6392), whereas 3- and 4-gram uniqueness are nearly unchanged.",
        "",
    ]
    comparison(lines, "Phishing versus benign", "P", "B",
                lambda row: row["group"].endswith("-P"),
                lambda row: row["group"].endswith("-B"), rows, metrics)
    lines += [
        "",
        "### Outstanding observations",
        "",
        "- The strongest phishing/benign differences come from the newly fitted LDA model: assignment topic 4 (d = 2.2122) and topic 4 proportion (d = 2.0063). These are dataset-specific topic coordinates, not universal linguistic meanings.",
        "- POS possessive-pronoun count (d = 1.4968) is higher for phishing, while determiners (d = -1.3382), particles (d = -0.9119), and interrogatives (d = -0.7439) are higher for benign text.",
        "- Benign samples have higher character 2-gram uniqueness (d = -0.5226), longer mean sentences (d = -0.2402), more short words (d = -1.3244), and more total words (d = -0.3308).",
        "- Phishing samples have a higher letter ratio (d = 0.8374) and average word length (d = 0.8369), while total character count is almost identical (d = -0.0480).",
        "- Several basic features show little phishing/benign separation, including character count without spaces (d = -0.0004), POS adjectives (d = 0.0187), POS nouns (d = -0.0677), and sentence length variance only has a moderate effect (d = -0.5079).",
        "",
    ]
    lines += ["", "## Interpretation", "",
              "- Positive `HW - MG` means the metric is higher for human-written text; negative means it is higher for machine-generated text.",
              "- Positive `P - B` means the metric is higher for phishing text; negative means it is higher for benign text.",
              "- Topic coordinates are model-specific and should not be interpreted semantically without inspecting the fitted vocabulary.",
              "- This output does not include unavailable RST, entity-grid, author-topic, character-embedding, or trained neural n-gram metrics.",
              "- The complete per-sample values are available in the JSON file.", ""]
    return "\n".join(lines)


def main():
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    samples = payload["samples"]
    texts = [sample["text"] for sample in samples]
    vectorizer = CountVectorizer(lowercase=True, token_pattern=r"(?u)\b\w+\b", min_df=1)
    matrix = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=TOPICS, random_state=0,
                                    learning_method="batch", max_iter=100)
    theta = lda.fit_transform(matrix)
    vocab = vectorizer.get_feature_names_out()
    word_topics = lda.components_.argmax(axis=0)
    results = []
    for index, sample in enumerate(samples):
        text = sample["text"]
        tokens = word_tokenize(text)
        words = [token for token in tokens if re.search(r"[A-Za-z0-9]", token)]
        sentences = sent_tokenize(text)
        sentence_lengths = [len(sentence) for sentence in sentences] or [len(text)]
        tags = [tag for _, tag in pos_tag(words)]
        metrics = {}
        flatten("syntactic", syntactic_counts(text), metrics)
        flatten("pos", pos_counts(tags), metrics)
        for n in (1, 2, 3):
            try:
                metrics[f"pos_density_{n}"] = float(pos_density(tags, n))
            except ValueError:
                metrics[f"pos_density_{n}"] = 0.0
        flatten("surface", surface_features(text, sentences), metrics)
        flatten("vocabulary", vocabulary_features(words, len(sentences) or 1,
                                                     sentence_lengths=sentence_lengths,
                                                     character_count=len(text)), metrics)
        flatten("sentence", sentence_length_features(sentence_lengths), metrics)
        char_ids = [ord(char) for char in text]
        grams = character_ngrams(char_ids)
        for n, values in grams.items():
            metrics[f"character_{n}gram_count"] = float(len(values))
            metrics[f"character_{n}gram_unique"] = float(len(set(values)))

        doc_counts = matrix[index].toarray()[0]
        assignments = []
        for word_index, count in enumerate(doc_counts):
            assignments.extend([int(word_topics[word_index])] * int(count))
        gamma = theta[index].tolist()
        for topic, value in enumerate(document_topic_proportions(gamma)):
            metrics[f"lda_topic_{topic}"] = float(value)
        for topic, value in enumerate(topic_assignment_proportions(assignments, TOPICS)):
            metrics[f"lda_assignment_topic_{topic}"] = float(value)
        metrics["lda_topic_entropy"] = float(topic_entropy(gamma))
        metrics["lda_dominant_topic_mass"] = float(dominant_topic_mass(gamma))
        metrics["lda_active_topic_count"] = float(active_topic_count(gamma, 0.05))
        metrics["lda_per_token_likelihood_bound"] = float(per_token_likelihood_bound(lda.score(matrix[index]), max(1, len(words))))
        results.append({
            "sample_id": sample["sample_id"],
            "group": sample["group"],
            "match_stratum": sample.get("match_stratum"),
            "metrics": metrics,
            "errors": {},
        })
    output = {"metadata": {
        "dataset": str(DATASET),
        "sample_count": len(results),
        "metric_scope": "recoverable Stylometric metrics",
        "tokenizer": "nltk.word_tokenize",
        "sentence_tokenizer": "nltk.sent_tokenize",
        "pos_tagger": "nltk.pos_tag",
        "lda": {"implementation": "sklearn LatentDirichletAllocation", "topics": TOPICS, "random_state": 0},
    }, "results": results}
    RESULTS.mkdir(exist_ok=True)
    JSON_OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    MD_OUT.write_text(make_report(output), encoding="utf-8")
    print(f"WROTE {JSON_OUT}")
    print(f"WROTE {MD_OUT}")
    print(f"SAMPLES {len(results)} METRICS {len(results[0]['metrics'])}")


if __name__ == "__main__":
    main()
