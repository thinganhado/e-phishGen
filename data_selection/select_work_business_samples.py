import csv
import json
import random
import re
import sys
from pathlib import Path

csv.field_size_limit(100_000_000)

MACHINE_PATH = Path(r"C:\Users\donga\Documents\GitHub\e-phishGen\ephishLLM.json")
HUMAN_PATH = Path(r"C:\Users\donga\Downloads\phishing-email-dataset\Phishing_Email.csv")
OUTPUT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("work_business_samples_4000.json")
SEED = 42
N_PER_GROUP = 1000

TERMS = [
    "project", "meeting", "team", "company", "business", "client", "customer",
    "manager", "management", "report", "schedule", "contract", "proposal",
    "partnership", "department", "office", "work", "employee", "colleague",
    "deadline", "presentation", "conference", "invoice", "purchase order",
    "sales", "vendor", "supplier", "career", "job", "interview", "recruitment",
]
PATTERNS = [re.compile(r"\b" + re.escape(term) + r"\b", re.I) for term in TERMS]


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def relevance(text):
    return sum(bool(pattern.search(text)) for pattern in PATTERNS)


def choose(records, seed):
    candidates = [r for r in records if r["text"] and relevance(r["text"]) > 0]
    if len(candidates) < N_PER_GROUP:
        raise RuntimeError(f"Only {len(candidates)} matching records available")
    # Keep the sample representative by sampling from all relevant records,
    # with a fixed seed for reproducibility.
    rng = random.Random(seed)
    rng.shuffle(candidates)
    return candidates[:N_PER_GROUP]


machine = json.loads(MACHINE_PATH.read_text(encoding="utf-8-sig"))
records = {"machine_benign": [], "machine_phishing": [], "human_benign": [], "human_phishing": []}

for index, item in enumerate(machine):
    if item.get("Language", "").lower() != "en":
        continue
    text = clean(f"{item.get('Subject', '')}\n\n{item.get('Body', '')}")
    group = "machine_phishing" if int(item["type"]) == 1 else "machine_benign"
    records[group].append({
        "text": text,
        "origin": "machine",
        "phishing_label": int(item["type"]),
        "language": item.get("Language"),
        "source": "ephishLLM.json",
        "source_index": index,
    })

with HUMAN_PATH.open(encoding="utf-8-sig", newline="") as handle:
    for index, item in enumerate(csv.DictReader(handle)):
        text = clean(item.get("Email Text", ""))
        if not text:
            continue
        phishing = item.get("Email Type") == "Phishing Email"
        group = "human_phishing" if phishing else "human_benign"
        records[group].append({
            "text": text,
            "origin": "human",
            "phishing_label": int(phishing),
            "language": "en_or_unknown",
            "source": "Phishing_Email.csv",
            "source_index": index,
        })

selected = []
for group_index, group in enumerate(("machine_benign", "machine_phishing", "human_benign", "human_phishing")):
    chosen = choose(records[group], SEED + group_index)
    for number, record in enumerate(chosen, 1):
        record["sample_id"] = f"{group}_{number:04d}"
        record["work_business_keyword_count"] = relevance(record["text"])
        record.pop("source_index")
        selected.append(record)

payload = {
    "theme": "work/business communication",
    "n_samples": len(selected),
    "samples_per_group": N_PER_GROUP,
    "selection_seed": SEED,
    "selection_rule": "non-empty English machine records and non-empty human records matching at least one work/business keyword",
    "groups": {group: N_PER_GROUP for group in records},
    "samples": selected,
}
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {len(selected)} samples to {OUTPUT_PATH.resolve()}")
