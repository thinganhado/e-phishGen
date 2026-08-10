import json
import sys
from pathlib import Path


def read_concatenated_json(path):
    raw = Path(path).read_text(encoding="utf-8-sig").strip()
    decoder = json.JSONDecoder()
    values = []
    position = 0
    while position < len(raw):
        while position < len(raw) and raw[position].isspace():
            position += 1
        if position >= len(raw):
            break
        value, position = decoder.raw_decode(raw, position)
        values.append(value)
    return values


source = Path(sys.argv[1])
destination = Path(sys.argv[2])
documents = read_concatenated_json(source)
all_samples = []
seen_ids = set()

for document in documents:
    samples = document.get("samples", []) if isinstance(document, dict) else document
    for sample in samples:
        sample_id = sample.get("sample_id") if isinstance(sample, dict) else None
        if sample_id and sample_id in seen_ids:
            continue
        if sample_id:
            seen_ids.add(sample_id)
        all_samples.append(sample)

fixed = {
    "theme": "account security and password verification",
    "n_samples": len(all_samples),
    "groups": {
        "machine_benign": sum(x.get("origin") == "machine" and x.get("phishing_label") == 0 for x in all_samples),
        "machine_phishing": sum(x.get("origin") == "machine" and x.get("phishing_label") == 1 for x in all_samples),
        "human_benign": sum(x.get("origin") == "human" and x.get("phishing_label") == 0 for x in all_samples),
        "human_phishing": sum(x.get("origin") == "human" and x.get("phishing_label") == 1 for x in all_samples),
    },
    "samples": all_samples,
}
destination.write_text(json.dumps(fixed, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Read {len(documents)} JSON documents; wrote {len(all_samples)} unique samples to {destination}")
