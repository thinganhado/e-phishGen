import json
import random
import re
from pathlib import Path


ROOT = Path(r"D:\AI\projects\e-phishGen")
SOURCE = ROOT / "800_dataset.json"
OUTPUT = ROOT / "matched_pool_scaled_284.json"
SEED = 42
GROUPS = ("HW-P", "MG-P", "HW-B", "MG-B")


def classify(sample):
    text = (sample["subject"] + " " + sample["text"]).lower()

    banking = re.search(
        r"\b(?:bank|banking|online banking|loan|mortgage|payment|invoice|financial|investment|refinanc|credit card)\b",
        text,
    )
    account = re.search(
        r"\b(?:account|password|login|sign.?in|credential|verify|verification|authentication|mfa|access|mailbox|security alert|security update)\b",
        text,
    )
    software = re.search(
        r"\b(?:software|system|update|upgrade|install|patch|maintenance|malware|virus|spyware|server|database|application|technical support)\b",
        text,
    )

    # Primary scenario avoids double-counting and makes the balancing rule
    # deterministic.  These are intentionally broad strata for scaling.
    if banking:
        scenario = "banking_security"
        goal = "financial_access_or_security_action"
    elif account:
        scenario = "account_security"
        goal = "account_access_or_security_action"
    elif software:
        scenario = "software_system"
        goal = "software_or_system_action"
    else:
        return None

    return scenario, goal


def normalize_urls(text):
    text = re.sub(r"<\|URL\|>|\[URL\]", "[URL]", text, flags=re.I)
    text = re.sub(r"https?://[^\s<>\]\[]+|www\.[^\s<>\]\[]+", "[URL]", text, flags=re.I)
    # Replace bare link-like domains while retaining email addresses.
    return re.sub(
        r"(?<![@\w])(?:[a-z0-9-]+\.)+(?:com|net|org|io|co)(?:/[^\s<>\]\[]*)?",
        "[URL]",
        text,
        flags=re.I,
    )


def word_count(text):
    return len(re.findall(r"\b[\w’'-]+\b", text))


data = json.loads(SOURCE.read_text(encoding="utf-8"))
rng = random.Random(SEED)
eligible = {group: {} for group in GROUPS}

for sample in data["samples"]:
    if sample["group"] not in GROUPS:
        continue
    labels = classify(sample)
    if labels is None:
        continue
    scenario, goal = labels
    eligible[sample["group"]].setdefault(scenario, []).append(sample)

# Equalize every stratum to the smallest available group count.  This gives
# the maximum balanced pool under the declared primary-stratum taxonomy.
strata = ("banking_security", "account_security", "software_system")
stratum_sizes = {
    scenario: min(len(eligible[group].get(scenario, [])) for group in GROUPS)
    for scenario in strata
}

rows = []
for scenario in strata:
    for group in GROUPS:
        candidates = list(eligible[group].get(scenario, []))
        rng.shuffle(candidates)
        for original in candidates[: stratum_sizes[scenario]]:
            sample = dict(original)
            sample["text"] = normalize_urls(sample["text"])
            sample["subject"] = normalize_urls(sample["subject"])
            sample["body"] = normalize_urls(sample["body"])
            sample["word_count"] = word_count(sample["text"])
            sample["match_stratum"] = scenario
            sample["matched_goal"] = classify(original)[1]
            sample["urls_normalized"] = True
            rows.append(sample)

result = {
    "source": SOURCE.name,
    "selection_seed": SEED,
    "selection_rule": (
        "Primary-stratum balancing across banking/security, account/security, "
        "and software/system; no length limit; equal count in every stratum "
        "for HW-P, MG-P, HW-B, and MG-B"
    ),
    "goal_rule": (
        "Goals are aligned at the action level: financial access/security, "
        "account access/security, and software/system action. For benign "
        "messages these denote the legitimate operational purpose."
    ),
    "url_normalization": (
        "Explicit URLs, bare link-like domains, and existing URL markers "
        "replaced with [URL]; email addresses retained"
    ),
    "n_samples": len(rows),
    "groups": {group: sum(row["group"] == group for row in rows) for group in GROUPS},
    "strata": {
        scenario: {
            group: sum(row["group"] == group and row["match_stratum"] == scenario for row in rows)
            for group in GROUPS
        }
        for scenario in strata
    },
    "samples": rows,
}
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"output": str(OUTPUT), "n_samples": len(rows), "groups": result["groups"], "strata": result["strata"]}, indent=2))
