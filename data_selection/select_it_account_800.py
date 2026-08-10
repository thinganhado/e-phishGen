import csv
import json
import random
import re
import sys
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

csv.field_size_limit(100_000_000)

MGT_PATH = Path(r"C:\Users\donga\Documents\GitHub\e-phishGen\ephishLLM.json")
HWT_PATH = Path(r"C:\Users\donga\Downloads\meajor_cleaned_preprocessed.parquet.gzip")
OUTPUT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("800_dataset.json")
SEED = 42
N_PER_GROUP = 200

SECURITY = re.compile(
    r"\b(password|passcode|credential|login|log[- ]?in|sign[- ]?in|account|"
    r"verify|verification|security|authentication|access|identity)\b", re.I
)
TECHNOLOGY = re.compile(
    r"\b(software|system|network|cloud|technology|technical|helpdesk|support|"
    r"server|application|platform|device)\b", re.I
)
ACTION = re.compile(
    r"\b(reset|update|confirm|change|click|link|install|download|unlock|"
    r"suspend|blocked|alert|unusual|suspicious)\b", re.I
)


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def relevance(text):
    return len(SECURITY.findall(text)) + len(TECHNOLOGY.findall(text))


def is_it_related(text):
    return sum(bool(pattern.search(text)) for pattern in (SECURITY, TECHNOLOGY, ACTION)) >= 2


def choose_machine(records, seed):
    # Exact duplicates are not useful for a diversity-oriented sample.
    unique = {}
    for record in records:
        unique.setdefault(record["text"].lower(), record)
    candidates = list(unique.values())
    if len(candidates) < N_PER_GROUP:
        raise RuntimeError(f"Only {len(candidates)} machine candidates available")

    # Keep the strongest candidates. MGT-B has only a small margin over 200.
    candidates.sort(key=lambda x: (-relevance(x["text"]), len(x["text"])))
    pool = candidates[:min(len(candidates), max(N_PER_GROUP, 600))]
    texts = [x["text"] for x in pool]
    vectorizer = TfidfVectorizer(
        stop_words="english", ngram_range=(1, 2), max_features=20_000,
        sublinear_tf=True,
    )
    matrix = vectorizer.fit_transform(texts)

    rng = random.Random(seed)
    selected_indices = [rng.randrange(len(pool))]
    selected_matrix = matrix[selected_indices[0]]
    # Select wording that is far from the closest already-selected email.
    max_similarity = (matrix @ selected_matrix.T).toarray().ravel()
    for _ in range(1, N_PER_GROUP):
        max_similarity[selected_indices] = 1.0
        # Small relevance tie-break prevents selecting weakly topical outliers.
        best = min(
            (i for i in range(len(pool)) if i not in selected_indices),
            key=lambda i: (max_similarity[i] - 0.002 * relevance(pool[i]["text"])),
        )
        selected_indices.append(best)
        selected_matrix = matrix[best]
        similarity = (matrix @ selected_matrix.T).toarray().ravel()
        max_similarity = __import__("numpy").maximum(max_similarity, similarity)
    return [pool[i] for i in selected_indices]


def choose_human(records, seed):
    unique = {}
    for record in records:
        unique.setdefault(record["text"].lower(), record)
    candidates = list(unique.values())
    if len(candidates) < N_PER_GROUP:
        raise RuntimeError(f"Only {len(candidates)} human candidates available")
    rng = random.Random(seed)
    rng.shuffle(candidates)
    return candidates[:N_PER_GROUP]


def add_group(records, group, origin, label):
    for record in records:
        record["origin"] = origin
        record["phishing_label"] = label
        record["group"] = group


mgt = json.loads(MGT_PATH.read_text(encoding="utf-8-sig"))
groups = {"MG-B": [], "MG-P": [], "HW-B": [], "HW-P": []}

for index, item in enumerate(mgt):
    if item.get("Language", "").lower() != "en":
        continue
    subject = clean(item.get("Subject", ""))
    body = clean(item.get("Body", ""))
    text = clean(f"{subject}\n\n{body}")
    if not text or not is_it_related(text):
        continue
    label = int(item["type"])
    groups["MG-P" if label else "MG-B"].append({
        "text": text,
        "subject": subject,
        "body": body,
        "language": "en",
        "source": "ephishLLM.json",
        "source_index": index,
    })

hwt = pd.read_parquet(HWT_PATH)
hwt = hwt[hwt["label"].notna()]
for index, row in hwt.iterrows():
    if str(row.get("language", "")).lower() != "en":
        continue
    subject = clean(row.get("subject", ""))
    body = clean(row.get("body", ""))
    text = clean(f"{subject}\n\n{body}")
    if not text or not is_it_related(text):
        continue
    label = int(row["label"])
    groups["HW-P" if label else "HW-B"].append({
        "text": text,
        "subject": subject,
        "body": body,
        "language": "en",
        "source": "meajor_cleaned_preprocessed.parquet.gzip",
        "source_index": int(index),
        "source_dataset": row.get("source"),
    })

selected = []
for group_index, group in enumerate(("MG-B", "MG-P", "HW-B", "HW-P")):
    records = choose_machine(groups[group], SEED + group_index) if group.startswith("MG") else choose_human(groups[group], SEED + group_index)
    for number, record in enumerate(records, 1):
        record["sample_id"] = f"{group}_{number:03d}"
        record["topic_keyword_count"] = relevance(record["text"])
        record.pop("source_index", None)
        add_group([record], group, "machine" if group.startswith("MG") else "human", 1 if group.endswith("P") else 0)
        selected.append(record)

payload = {
    "theme": "IT account, access, security, and software/system communication",
    "n_samples": len(selected),
    "samples_per_group": N_PER_GROUP,
    "selection_seed": SEED,
    "selection_rule": "English emails matching at least two of security/access, technology/system, and IT-action terms",
    "groups": {group: N_PER_GROUP for group in ("MG-B", "MG-P", "HW-B", "HW-P")},
    "samples": selected,
}
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {len(selected)} samples to {OUTPUT_PATH.resolve()}")
