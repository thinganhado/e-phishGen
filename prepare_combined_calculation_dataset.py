import json
import re
from pathlib import Path


ROOT = Path(r"D:\AI\projects\e-phishGen")
SOURCE = ROOT / "combined.json"
OUTPUT = ROOT / "combined_calculation.json"


def normalize_urls(text):
    text = str(text or "")
    text = re.sub(r"https?://[^\s<>\]\[]+|www\.[^\s<>\]\[]+", "[URL]", text, flags=re.I)
    text = re.sub(r"<\|URL\|>|\[URL\]", "[URL]", text, flags=re.I)
    return text


source = json.loads(SOURCE.read_text(encoding="utf-8"))
samples = []
for index, item in enumerate(source, 1):
    subject = normalize_urls(item.get("Subject", ""))
    body = normalize_urls(item.get("Body", ""))
    category = item.get("PEST_Category") or "unknown_category"
    technique = item.get("PEST_Technique") or "unknown_technique"
    motivation = item.get("Motivation") or "unknown_motivation"
    samples.append({
        "sample_id": f"COMBINED_{index:04d}",
        "group": item["Group"],
        "text": f"{subject}\n{body}".strip(),
        "subject": subject,
        "body": body,
        "match_stratum": f"{category}__{technique}__{motivation}",
        "scenario": category,
        "scenario_detail": technique,
        "goal_frame": motivation,
        "source_index": index,
        "original_id": item.get("Original_ID"),
        "type": item.get("Type"),
        "created_by": item.get("Created by"),
        "source": item.get("Source"),
        "url_normalized": True,
    })

result = {
    "source": SOURCE.name,
    "n_samples": len(samples),
    "groups": {group: sum(x["group"] == group for x in samples) for group in ("HW-P", "HW-B", "MG-P", "MG-B")},
    "url_normalization": "URL-bearing content normalized to [URL]",
    "stratification": "PEST_Category + PEST_Technique + Motivation",
    "samples": samples,
}
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"output": str(OUTPUT), "n_samples": len(samples), "groups": result["groups"]}, indent=2))
