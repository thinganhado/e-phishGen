import json
import re
from pathlib import Path


ROOT = Path(r"D:\AI\projects\e-phishGen")
SOURCE = ROOT / "800_dataset.json"
OUTPUT = ROOT / "matched_pool_22.json"

# Conservative semantic strata.  The HW-P side is the limiting side because
# it contains far fewer messages in the target length band.
selected = {
    "banking_security": {
        "HW-P": ["HW-P_001", "HW-P_004"],
        "MG-P": ["MG-P_011", "MG-P_067"],
    },
    "email_account_verification": {
        "HW-P": ["HW-P_002", "HW-P_022", "HW-P_038", "HW-P_048", "HW-P_079", "HW-P_081"],
        "MG-P": ["MG-P_015", "MG-P_022", "MG-P_048", "MG-P_071", "MG-P_089", "MG-P_133"],
    },
    "software_system_security": {
        "HW-P": ["HW-P_127", "HW-P_135", "HW-P_170"],
        "MG-P": ["MG-P_019", "MG-P_023", "MG-P_064"],
    },
}


def word_count(text):
    return len(re.findall(r"\b[\w’'-]+\b", text))


def normalize_urls(text):
    # Normalize explicit links and anonymized URL markers to one token.
    text = re.sub(r"<\|URL\|>|\[URL\]", "[URL]", text, flags=re.I)
    text = re.sub(r"https?://[^\s<>\]\[]+|www\.[^\s<>\]\[]+", "[URL]", text, flags=re.I)
    # Replace bare link-like domains, but do not alter email addresses.
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
            sample["urls_normalized"] = True
            rows.append(sample)

result = {
    "source": SOURCE.name,
    "selection_rule": "Manually audited matched strata; 50-150 word eligibility, centered near 100 words, equal HW-P/MG-P counts per stratum",
    "url_normalization": "Explicit URLs, bare link-like domains, and existing URL markers replaced with [URL]; email addresses retained",
    "n_samples": len(rows),
    "groups": {group: sum(1 for row in rows if row["group"] == group) for group in ("HW-P", "MG-P")},
    "strata": {stratum: {group: len(ids) for group, ids in groups.items()} for stratum, groups in selected.items()},
    "samples": rows,
}
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"output": str(OUTPUT), "n_samples": len(rows), "groups": result["groups"], "strata": result["strata"]}, indent=2))
