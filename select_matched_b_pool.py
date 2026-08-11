import json
import re
from pathlib import Path


ROOT = Path(r"D:\AI\projects\e-phishGen")
SOURCE = ROOT / "800_dataset.json"
OUTPUT = ROOT / "matched_b_pool_20.json"

# For benign samples there is no phishing attack goal.  These strata match
# the legitimate communication intent and operational scenario instead.
selected = {
    "software_troubleshooting_support": {
        "HW-B": ["HW-B_005", "HW-B_053", "HW-B_172"],
        "MG-B": ["MG-B_009", "MG-B_098", "MG-B_130"],
    },
    "account_access_it_support": {
        "HW-B": ["HW-B_006", "HW-B_078", "HW-B_088"],
        "MG-B": ["MG-B_002", "MG-B_116", "MG-B_165"],
    },
    "system_operations_maintenance": {
        "HW-B": ["HW-B_077", "HW-B_157", "HW-B_185"],
        "MG-B": ["MG-B_004", "MG-B_069", "MG-B_082"],
    },
    "operational_market_update": {
        "HW-B": ["HW-B_009"],
        "MG-B": ["MG-B_172"],
    },
}


def word_count(text):
    return len(re.findall(r"\b[\w’'-]+\b", text))


def normalize_urls(text):
    text = re.sub(r"<\|URL\|>|\[URL\]", "[URL]", text, flags=re.I)
    text = re.sub(r"https?://[^\s<>\]\[]+|www\.[^\s<>\]\[]+", "[URL]", text, flags=re.I)
    text = re.sub(
        r"(?<![@\w])(?:[a-z0-9-]+\.)+(?:com|net|org|io|co)(?:/[^\s<>\]\[]*)?",
        "[URL]",
        text,
        flags=re.I,
    )
    return text


data = json.loads(SOURCE.read_text(encoding="utf-8"))
by_id = {sample["sample_id"]: sample for sample in data["samples"]}
rows = []
for stratum, groups in selected.items():
    for group, ids in groups.items():
        for sample_id in ids:
            sample = dict(by_id[sample_id])
            sample["text"] = normalize_urls(sample["text"])
            sample["subject"] = normalize_urls(sample["subject"])
            sample["body"] = normalize_urls(sample["body"])
            sample["word_count"] = word_count(sample["text"])
            sample["match_stratum"] = stratum
            sample["attack_goal"] = "none (benign operational communication)"
            sample["urls_normalized"] = True
            rows.append(sample)

result = {
    "source": SOURCE.name,
    "selection_rule": "Manually audited matched benign-intent strata; 50-150 word eligibility, centered near 100 words, equal HW-B/MG-B counts per stratum",
    "url_normalization": "Explicit URLs, bare link-like domains, and existing URL markers replaced with [URL]; email addresses retained",
    "n_samples": len(rows),
    "groups": {group: sum(1 for row in rows if row["group"] == group) for group in ("HW-B", "MG-B")},
    "strata": {stratum: {group: len(ids) for group, ids in groups.items()} for stratum, groups in selected.items()},
    "samples": rows,
}
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"output": str(OUTPUT), "n_samples": len(rows), "groups": result["groups"], "strata": result["strata"]}, indent=2))
