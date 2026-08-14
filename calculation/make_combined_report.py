"""Build one descriptive report from the three combined-dataset analyses."""

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HWT = ROOT / "HWT-MGT" / "results"
STYLO = ROOT / "Stylometric" / "results"
PHISH = ROOT / "Phishing" / "results"
TARGET = HWT / "combined_calculation_all_metrics.md"


def flatten(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return [float(value)]
    if isinstance(value, list):
        output = []
        for item in value:
            output.extend(flatten(item))
        return output
    return []


def sample_value(row, metric):
    values = flatten(row.get("metrics", {}).get(metric))
    return sum(values) / len(values) if values else None


def selected(rows, predicate, metric):
    return [value for row in rows if predicate(row)
            for value in [sample_value(row, metric)] if value is not None]


def mean(values):
    return sum(values) / len(values) if values else None


def sd(values):
    if len(values) < 2:
        return None
    center = mean(values)
    return math.sqrt(sum((x - center) ** 2 for x in values) / (len(values) - 1))


def cohens_d(left, right):
    if len(left) < 2 or len(right) < 2:
        return None
    pooled = math.sqrt(((len(left) - 1) * sd(left) ** 2 +
                        (len(right) - 1) * sd(right) ** 2) /
                       (len(left) + len(right) - 2))
    return 0.0 if pooled == 0 else (mean(left) - mean(right)) / pooled


def fmt(value):
    return "-" if value is None else f"{value:.4f}"


def label(metric):
    return metric.replace("_", " ").capitalize()


def metrics_for(rows):
    names = set()
    for row in rows:
        names.update(row.get("metrics", {}))
    return sorted(names - {"regeneration_count", "perturbation_count"})


def comparison(lines, heading, description, left_name, right_name,
               left_predicate, right_predicate, metrics, rows):
    lines += ["", f"## {heading}", "", description, "",
              f"| Metric | {left_name} mean | {right_name} mean | Difference ({left_name} - {right_name}) | Cohen d |",
              "|---|---:|---:|---:|---:|"]
    effects = []
    for metric in metrics:
        left = selected(rows, left_predicate, metric)
        right = selected(rows, right_predicate, metric)
        d = cohens_d(left, right)
        effects.append((abs(d) if d is not None else -1, metric, d,
                        mean(left), mean(right)))
        difference = mean(left) - mean(right) if left and right else None
        lines.append(f"| {label(metric)} | {fmt(mean(left))} | {fmt(mean(right))} | "
                     f"{fmt(difference)} | {fmt(d)} |")
    effects.sort(reverse=True)
    strongest = [f"`{metric}` (d = {fmt(d)})" for _, metric, d, _, _ in effects[:5]
                 if d is not None]
    lines += ["", "### Strongest descriptive separations", "",
              "The five largest absolute Cohen d values are: " +
              ", ".join(strongest) + "."]


def read_results(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload, payload["results"]


def append_existing(lines, path, title):
    text = path.read_text(encoding="utf-8").strip()
    body = text.split("\n", 1)[1] if "\n" in text else ""
    lines += ["", f"## {title}", "", body]


def main():
    hwt_payload, hwt_rows = read_results(HWT / "combined_calculation_metrics.json")
    groups = {group: sum(row.get("group") == group for row in hwt_rows)
              for group in ("HW-P", "MG-P", "HW-B", "MG-B")}
    metrics = metrics_for(hwt_rows)
    lines = [
        "# Combined calculation descriptive comparison", "",
        "This report consolidates the three completed analyses for the combined dataset.",
        "Individual sample values are omitted here; complete values remain in each group's JSON output.",
        "", "## Dataset and notation", "",
        f"- Total samples: **{len(hwt_rows)}**",
        f"- `HW-P`: **{groups['HW-P']}**; `MG-P`: **{groups['MG-P']}**",
        f"- `HW-B`: **{groups['HW-B']}**; `MG-B`: **{groups['MG-B']}**",
        "- Difference is calculated as left mean minus right mean.",
        "- Cohen d is a descriptive standardized effect size, not a significance test.",
        "", "# 1. HWT/MGT calculation", "",
        "This section uses the completed HWT/MGT model-based metrics.",
    ]
    comparison(lines, "HWT versus MGT",
               "This pools phishing and benign samples: `HW = HW-P + HW-B` and `MG = MG-P + MG-B`.",
               "HW", "MG", lambda r: r.get("group", "").startswith("HW-"),
               lambda r: r.get("group", "").startswith("MG-"), metrics, hwt_rows)
    comparison(lines, "Phishing versus benign",
               "This pools authorship sources: `P = HW-P + MG-P` and `B = HW-B + MG-B`.",
               "P", "B", lambda r: r.get("group", "").endswith("-P"),
               lambda r: r.get("group", "").endswith("-B"), metrics, hwt_rows)
    lines += ["", "## Annotation-group context", "",
              "Pooled comparisons can be inspected against the four underlying groups here.",
              "", "| Metric | HW-P | MG-P | HW-B | MG-B |", "|---|---:|---:|---:|---:|"]
    for metric in metrics:
        values = [mean(selected(hwt_rows, lambda r, g=g: r.get("group") == g, metric))
                  for g in ("HW-P", "MG-P", "HW-B", "MG-B")]
        lines.append(f"| {label(metric)} | " + " | ".join(fmt(x) for x in values) + " |")
    lines += ["", "# 2. Stylometric calculation", "",
              "The complete descriptive Stylometric report follows."]
    append_existing(lines, STYLO / "combined_calculation_stylometric_metrics.md", "Stylometric results")
    lines += ["", "# 3. Phishing calculation", "",
              "The complete descriptive Phishing-feature report follows."]
    append_existing(lines, PHISH / "combined_calculation_phishing_metrics.md", "Phishing results")
    lines += ["", "## Source files", "",
              "- HWT/MGT: `HWT-MGT/results/combined_calculation_metrics.json`",
              "- Stylometric: `Stylometric/results/combined_calculation_stylometric_metrics.json`",
              "- Phishing: `Phishing/results/combined_calculation_phishing_metrics.json`", ""]
    TARGET.write_text("\n".join(lines), encoding="utf-8")
    print(f"WROTE {TARGET}")


if __name__ == "__main__":
    main()
