import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd


ROOT = Path(r"D:\AI\projects\e-phishGen")
MGT_PATH = ROOT / "ephishLLM.json"
HWT_PATH = ROOT / "meajor_cleaned_preprocessed.parquet.gzip"
OUTPUT = ROOT / "scaled_stratified_pool_8980.json"
SEED = 42

SCENARIO_PATTERNS = {
    "account_access": r"account|password|login|credential|sign[ -]?in|authentication|verify|verification|access|mailbox|user",
    "software_system": r"software|system|update|upgrade|install|patch|maintenance|server|database|computer|application|platform|technical|\bit\b",
    "finance_payment": r"bank|payment|invoice|billing|credit|loan|financial|transaction|trading|mortgage|fund",
    "email_delivery": r"email|e-mail|mail|message|delivery|inbox|outlook|sendmail",
    "security_compliance": r"security|cyber|compliance|audit|policy|risk|threat|breach|antivirus|spyware|fraud",
    "business_project": r"project|meeting|proposal|contract|client|customer|vendor|team|department|work|partnership|organization|company",
    "marketing_commerce": r"sale|offer|discount|promotion|webinar|conference|newsletter|shopping|order|product",
}
GOAL_PATTERNS = {
    "credential_access": r"account|password|login|credential|sign[ -]?in|authentication|verify|verification|access|mailbox|user",
    "software_install_update": r"software|system|update|upgrade|install|patch|maintenance|server|database|computer|application|platform|download",
    "financial_payment": r"bank|payment|invoice|billing|credit|loan|financial|transaction|trading|mortgage|fund|prize|money",
    "malware_attachment": r"malware|virus|antivirus|spyware|attachment|document|macro|file",
    "communication_business": r"project|meeting|proposal|contract|client|customer|vendor|team|department|work|partnership|company|organization",
    "marketing_registration": r"sale|offer|discount|promotion|webinar|conference|newsletter|shopping|order|register|subscription",
    "security_compliance": r"security|cyber|compliance|audit|policy|risk|threat|breach|fraud",
}
SCENARIO_PRIORITY = list(SCENARIO_PATTERNS)
GOAL_PRIORITY = list(GOAL_PATTERNS)


def classify(text, patterns, priority):
    return [name for name in priority if re.search(patterns[name], text, re.I)]


def primary(tags):
    return tags[0] if tags else "other"


def normalize_urls(text):
    text = str(text or "")
    text = re.sub(r"<\|URL\|>|\[URL\]", "[URL]", text, flags=re.I)
    text = re.sub(r"<<\s*(?:url|link|href)[^>]*>>", "[URL]", text, flags=re.I)
    text = re.sub(r"https?://[^\s<>\]\[]+|www\.[^\s<>\]\[]+", "[URL]", text, flags=re.I)
    return re.sub(
        r"(?<![@\w])(?:[a-z0-9-]+\.)+(?:com|net|org|io|co|biz|info)(?:/[^\s<>\]\[]*)?",
        "[URL]",
        text,
        flags=re.I,
    )


def word_count(text):
    return len(re.findall(r"\b[\w’'-]+\b", text))


def goal_description(group, goal):
    malicious = {
        "credential_access": "credential/account capture",
        "software_install_update": "malicious software/update lure",
        "financial_payment": "financial/payment fraud",
        "malware_attachment": "malware/attachment delivery",
        "communication_business": "business/social-engineering action",
        "marketing_registration": "promotional/registration lure",
        "security_compliance": "security/compliance-themed action",
    }
    legitimate = {
        "credential_access": "account/access administration",
        "software_install_update": "software/system maintenance",
        "financial_payment": "legitimate finance/payment operation",
        "malware_attachment": "legitimate file/attachment operation",
        "communication_business": "business/project communication",
        "marketing_registration": "legitimate marketing/registration",
        "security_compliance": "security/compliance administration",
    }
    return (malicious if group.endswith("-P") else legitimate).get(goal, goal)


def make_record(group, source_name, source_index, subject, body, label):
    subject = normalize_urls(subject)
    body = normalize_urls(body)
    text = f"{subject}\n{body}".strip()
    scenario_tags = classify(text, SCENARIO_PATTERNS, SCENARIO_PRIORITY)
    goal_tags = classify(text, GOAL_PATTERNS, GOAL_PRIORITY)
    scenario = primary(scenario_tags)
    goal = primary(goal_tags)
    return {
        "sample_id": f"{source_name}_{source_index:06d}",
        "source": source_name,
        "source_index": source_index,
        "group": group,
        "label": label,
        "subject": subject,
        "body": body,
        "text": text,
        "word_count": word_count(text),
        "scenario": scenario,
        "scenario_tags": scenario_tags,
        "goal_frame": goal,
        "goal_tags": goal_tags,
        "match_stratum": f"{scenario}__{goal}",
        "goal_description": goal_description(group, goal),
        "urls_normalized": True,
    }


records = []
with MGT_PATH.open(encoding="utf-8") as handle:
    mgt = json.load(handle)
for index, item in enumerate(mgt):
    if str(item.get("Language", "")).lower() != "en":
        continue
    kind = int(item["type"])
    group = "MG-P" if kind == 1 else "MG-B"
    records.append(make_record(group, "MGT", index, item.get("Subject", ""), item.get("Body", ""), kind))

hwt = pd.read_parquet(HWT_PATH)
hwt = hwt[hwt["language"].astype(str).str.lower().eq("en") & hwt["label"].notna()]
for index, row in hwt.iterrows():
    kind = int(row["label"])
    group = "HW-P" if kind == 1 else "HW-B"
    records.append(make_record(group, "HWT", int(index), row.get("subject", ""), row.get("body", ""), kind))

groups = ["HW-P", "HW-B", "MG-P", "MG-B"]
by_cell = defaultdict(list)
for record in records:
    by_cell[(record["group"], (record["scenario"], record["goal_frame"]))].append(record)

cell_counts = {}
all_cells = {cell for _, cell in by_cell}
for cell in sorted(all_cells):
    if "other" in cell:
        continue
    count = min(len(by_cell[(group, cell)]) for group in groups)
    if count:
        cell_counts[cell] = count

rng = random.Random(SEED)
selected = []
for cell, count in sorted(cell_counts.items()):
    for group in groups:
        candidates = list(by_cell[(group, cell)])
        rng.shuffle(candidates)
        selected.extend(candidates[:count])
selected.sort(key=lambda row: (row["group"], row["scenario"], row["goal_frame"], row["sample_id"]))

result = {
    "source_datasets": {"MGT": MGT_PATH.name, "HWT": HWT_PATH.name},
    "selection_seed": SEED,
    "selection_rule": "English only; no length limit; every scenario-goal cell present in all four groups retained at the largest common count",
    "url_normalization": "All explicit URLs, bare link-like domains, and URL/link markers replaced with [URL]; email addresses retained",
    "n_samples": len(selected),
    "groups": dict(Counter(row["group"] for row in selected)),
    "cell_counts_per_group": {f"{scenario}__{goal}": count for (scenario, goal), count in cell_counts.items()},
    "scenario_counts_per_group": {group: dict(Counter(row["scenario"] for row in selected if row["group"] == group)) for group in groups},
    "goal_counts_per_group": {group: dict(Counter(row["goal_frame"] for row in selected if row["group"] == group)) for group in groups},
    "samples": selected,
}
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"output": str(OUTPUT), "n_samples": len(selected), "groups": result["groups"], "cells": len(cell_counts), "cells_per_group": sum(cell_counts.values())}, indent=2))
