import csv
import json
import re
from pathlib import Path

csv.field_size_limit(100_000_000)

MACHINE_PATH = Path(r"C:\Users\donga\Documents\GitHub\e-phishGen\ephishLLM.json")
HUMAN_PATH = Path(r"C:\Users\donga\Downloads\phishing-email-dataset\Phishing_Email.csv")
OUTPUT_PATH = Path(r"C:\tmp\account_security_password_samples_80.json")

THEME = re.compile(
    r"account|password|passcode|credential|login|log[- ]?in|sign[- ]?in|verify|verification|"
    r"security|suspicious activity|unusual activity|access|identity|authentication|reset|"
    r"unlock|suspend|suspension|two[- ]factor|2fa|mfa",
    re.I,
)


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def rank(record):
    text = record["text"]
    hits = len(THEME.findall(text))
    # Prefer clearly themed, readable emails, but retain deterministic variety.
    length_bonus = min(len(text.split()), 250) / 250
    return (hits, length_bonus, -len(text), record["source_index"])


machine = json.loads(MACHINE_PATH.read_text(encoding="utf-8-sig"))
records = []
for index, item in enumerate(machine):
    subject = clean(item.get("Subject", ""))
    body = clean(item.get("Body", ""))
    text = clean(f"{subject}\n\n{body}")
    if text and item.get("Language", "").lower() == "en":
        records.append({
            "text": text,
            "phishing_label": int(item["type"]),
            "origin": "machine",
            "language": item.get("Language"),
            "source": "ephishLLM.json",
            "source_index": index,
        })

human_records = csv.DictReader(
    HUMAN_PATH.open(encoding="utf-8-sig", newline="")
)
for index, item in enumerate(human_records):
    text = clean(item.get("Email Text", ""))
    if text:
        records.append({
            "text": text,
            "phishing_label": 1 if item.get("Email Type") == "Phishing Email" else 0,
            "origin": "human",
            "language": "en_or_unknown",
            "source": "Phishing_Email.csv",
            "source_index": index,
        })

selected = []
for origin in ("machine", "human"):
    for label in (0, 1):
        group = [r for r in records if r["origin"] == origin and r["phishing_label"] == label]
        group.sort(key=rank, reverse=True)
        chosen = group[:20]
        if len(chosen) != 20:
            raise RuntimeError(f"Only found {len(chosen)} records for {origin}, label {label}")
        for sample_number, record in enumerate(chosen, 1):
            record["sample_id"] = f"{origin}_{'benign' if label == 0 else 'phishing'}_{sample_number:02d}"
            record.pop("source_index")
            selected.append(record)

OUTPUT_PATH.write_text(
    json.dumps(
        {
            "theme": "account security and password verification",
            "n_samples": len(selected),
            "groups": {
                "machine_benign": 20,
                "machine_phishing": 20,
                "human_benign": 20,
                "human_phishing": 20,
            },
            "samples": selected,
        },
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)
print(OUTPUT_PATH.resolve())
