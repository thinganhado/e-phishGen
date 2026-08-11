import json
import re
from pathlib import Path


ROOT = Path(r"D:\AI\projects\e-phishGen")
SOURCE = ROOT / "800_dataset.json"
OUTPUT = ROOT / "matched_pool_44.json"
PHISHING_POOL = ROOT / "matched_pool_22.json"

# The benign strata mirror the broad operational contexts used in the
# phishing pool.  For benign mail, the analogous field is the legitimate
# operational purpose rather than an attack goal.
selected = {
    "banking_security": {
        "HW-B": ["HW-B_006", "HW-B_078"],
        "MG-B": ["MG-B_002", "MG-B_014"],
    },
    "email_account_verification": {
        "HW-B": ["HW-B_005", "HW-B_077", "HW-B_157", "HW-B_159", "HW-B_172", "HW-B_185"],
        "MG-B": ["MG-B_004", "MG-B_006", "MG-B_013", "MG-B_068", "MG-B_069", "MG-B_072"],
    },
    "software_system_security": {
        "HW-B": ["HW-B_053", "HW-B_066", "HW-B_178"],
        "MG-B": ["MG-B_011", "MG-B_030", "MG-B_060"],
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
phishing = json.loads(PHISHING_POOL.read_text(encoding="utf-8"))
by_id = {sample["sample_id"]: sample for sample in data["samples"]}
rows = list(phishing["samples"])

for stratum, groups in selected.items():
    for group, ids in groups.items():
        for sample_id in ids:
            sample = dict(by_id[sample_id])
            sample["text"] = normalize_urls(sample["text"])
            sample["subject"] = normalize_urls(sample["subject"])
            sample["body"] = normalize_urls(sample["body"])
            sample["word_count"] = word_count(sample["text"])
            sample["match_stratum"] = stratum
            sample["legitimate_purpose"] = {
                "banking_security": "legitimate access/security administration",
                "email_account_verification": "legitimate account/email/system operations",
                "software_system_security": "legitimate software/system maintenance",
            }[stratum]
            sample["urls_normalized"] = True
            rows.append(sample)

result = dict(phishing)
result["source"] = SOURCE.name
result["selection_rule"] = (
    "Matched HW-P/MG-P and HW-B/MG-B strata; 50-150 word eligibility, "
    "centered near 100 words, equal counts per group and stratum"
)
result["url_normalization"] = (
    "Explicit URLs, bare link-like domains, and existing URL markers replaced "
    "with [URL]; email addresses retained"
)
result["n_samples"] = len(rows)
result["groups"] = {group: sum(1 for row in rows if row["group"] == group) for group in ("HW-P", "MG-P", "HW-B", "MG-B")}
result["strata"] = {
    stratum: {group: len(ids) for group, ids in groups.items()}
    for stratum, groups in selected.items()
}
result["samples"] = rows
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"output": str(OUTPUT), "n_samples": len(rows), "groups": result["groups"], "strata": result["strata"]}, indent=2))
