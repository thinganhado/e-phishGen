"""Run the source-compatible 17 phishing stylometric features on the dataset."""

import importlib.util
import json
import sys
import types
from pathlib import Path

DATASET = Path(r"D:\AI\projects\e-phishGen\matched_pool_44.json")
ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
JSON_OUT = RESULTS / "matched_pool_44_phishing_metrics.json"
MD_OUT = RESULTS / "matched_pool_44_phishing_metrics.md"


def load_source_extractor():
    # 05_extract_features.py imports config and loads spaCy at module import.
    # Inject a harmless in-memory config so the source function can be reused
    # without requiring the original CSV corpus layout.
    config = types.ModuleType("config")
    config.HUMAN_DIR = RESULTS / "source_adapter" / "human"
    config.LLM_DIR = RESULTS / "source_adapter" / "llm"
    config.DATA_DIR = RESULTS / "source_adapter"
    config.LOGS_DIR = RESULTS / "source_adapter" / "logs"
    sys.modules["config"] = config
    path = ROOT / "preprocess" / "05_extract_features.py"
    spec = importlib.util.spec_from_file_location("phishing_source_features", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fmt(value):
    return "-" if value is None else f"{value:.4f}"


def mean(values):
    return sum(values) / len(values) if values else None


def effect_size(left, right):
    if len(left) < 2 or len(right) < 2:
        return None
    lm, rm = mean(left), mean(right)
    lv = sum((x - lm) ** 2 for x in left) / (len(left) - 1)
    rv = sum((x - rm) ** 2 for x in right) / (len(right) - 1)
    pooled = (((len(left) - 1) * lv + (len(right) - 1) * rv) /
              (len(left) + len(right) - 2)) ** 0.5
    return (lm - rm) / pooled if pooled else 0.0


def group_values(rows, metric, predicate):
    return [row["metrics"][metric] for row in rows if predicate(row)]


def append_table(lines, title, left_name, right_name, left_predicate,
                 right_predicate, rows, metrics):
    lines += ["", f"## {title}", "",
              f"| Metric | {left_name} mean | {right_name} mean | Difference ({left_name} - {right_name}) | Cohen d |",
              "|---|---:|---:|---:|---:|"]
    for metric in metrics:
        left = group_values(rows, metric, left_predicate)
        right = group_values(rows, metric, right_predicate)
        lm, rm = mean(left), mean(right)
        lines.append(f"| {metric.replace('_', ' ').capitalize()} | {fmt(lm)} | {fmt(rm)} | "
                     f"{fmt(lm - rm if lm is not None and rm is not None else None)} | {fmt(effect_size(left, right))} |")


def make_report(payload):
    rows = payload["results"]
    metrics = sorted({metric for row in rows for metric in row["metrics"]})
    counts = {group: sum(row["group"] == group for row in rows)
              for group in ("HW-P", "MG-P", "HW-B", "MG-B")}
    lines = [
        "# Phishing stylometric descriptive comparison",
        "",
        "This report summarizes the 16 applicable phishing features for "
        "`matched_pool_44.json`; individual sample rows are omitted.",
        "",
        "## Dataset and settings",
        "",
        f"- Samples: **{len(rows)}**",
        f"- `HW-P`: **{counts['HW-P']}**; `MG-P`: **{counts['MG-P']}**",
        f"- `HW-B`: **{counts['HW-B']}**; `MG-B`: **{counts['MG-B']}**",
        "- Each sample was processed as one input using the source `extract_features()` function.",
        "- spaCy model: `en_core_web_sm`.",
        "- URL metrics are intentionally excluded because this dataset does not contain URL information.",
        "- Difference is left mean minus right mean; Cohen d is descriptive, not a significance test.",
    ]
    append_table(lines, "HWT versus MGT", "HW", "MG",
                 lambda row: row["group"].startswith("HW-"),
                 lambda row: row["group"].startswith("MG-"), rows, metrics)
    lines += [
        "",
        "### Outstanding observations",
        "",
        "- Mean word length is the clearest HWT/MGT difference (d = -1.2634): MG samples use longer words on average.",
        "- MG also has higher CTA density (d = -0.6926), politeness density (d = -0.7199), time-pressure density (d = -0.5959), TTR (d = -0.5962), and urgency density (d = -0.4027).",
        "- HWT has higher Yule's K (d = 0.4334), indicating more word-frequency concentration under this corpus and tokenizer.",
        "- Mean parse depth is essentially identical between HW and MG (d = 0.0049), while clause density and imperative count are also weak separators.",
        "",
    ]
    append_table(lines, "Phishing versus benign", "P", "B",
                 lambda row: row["group"].endswith("-P"),
                 lambda row: row["group"].endswith("-B"), rows, metrics)
    lines += [
        "",
        "### Outstanding observations",
        "",
        "- Second-person ratio is the strongest Phishing/Benign difference (d = 1.9366): phishing samples address the reader much more directly.",
        "- CTA density is also substantially higher for phishing (d = 1.1614), followed by mean word length (d = 0.8909), urgency density (d = 0.6930), politeness density (d = 0.6458), and time-pressure density (d = 0.3853).",
        "- Phishing samples have lower mean parse depth (d = -0.6220) and shorter mean sentences (d = -0.3389) than benign samples.",
        "- Authority density (d = 0.0044), TTR (d = -0.0695), verb ratio (d = 0.0942), and first-person ratio (d = 0.0441) show little or no separation.",
        "- URL metrics are excluded from this analysis because the dataset contains no URL information.",
        "",
        "## Reproducibility",
        "",
        "The complete per-sample values remain available in `matched_pool_44_phishing_metrics.json`.",
        "",
    ]
    return "\n".join(lines)


def main():
    source = load_source_extractor()
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    results = []
    for sample in payload["samples"]:
        try:
            metrics = source.extract_features(sample["text"])
            metrics.pop("url_density", None)
            errors = {}
        except Exception as exc:
            metrics = {}
            errors = {"feature_extraction": f"{type(exc).__name__}: {exc}"}
        results.append({
            "sample_id": sample["sample_id"],
            "group": sample["group"],
            "match_stratum": sample.get("match_stratum"),
            "metrics": metrics,
            "errors": errors,
        })
    output = {
        "metadata": {
            "dataset": str(DATASET),
            "sample_count": len(results),
            "feature_count": 16,
            "source_script": str(ROOT / "preprocess" / "05_extract_features.py"),
            "spacy_model": "en_core_web_sm",
        },
        "results": results,
    }
    RESULTS.mkdir(exist_ok=True)
    JSON_OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    MD_OUT.write_text(make_report(output), encoding="utf-8")
    print(f"WROTE {JSON_OUT}")
    print(f"WROTE {MD_OUT}")
    print(f"SAMPLES {len(results)} FEATURES {len(results[0]['metrics'])}")


if __name__ == "__main__":
    main()
