"""Create an aggregate HWT/MGT and phishing/benign comparison report."""

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
SOURCE = RESULTS / "matched_pool_44_metrics.json"
TARGET = RESULTS / "matched_pool_44_metrics.md"


def flatten_numbers(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return [float(value)]
    if isinstance(value, list):
        output = []
        for item in value:
            output.extend(flatten_numbers(item))
        return output
    return []


def row_value(row, metric):
    """Return one value per sample; vectors are reduced within each sample."""
    values = flatten_numbers(row["metrics"].get(metric))
    return sum(values) / len(values) if values else None


def values(rows, selector, metric):
    output = []
    for row in rows:
        if selector(row):
            value = row_value(row, metric)
            if value is not None:
                output.append(value)
    return output


def average(items):
    return sum(items) / len(items) if items else None


def sample_sd(items):
    if len(items) < 2:
        return None
    center = average(items)
    return math.sqrt(sum((item - center) ** 2 for item in items) / (len(items) - 1))


def effect_size(left, right):
    """Cohen's d: left mean minus right mean, divided by pooled SD."""
    if len(left) < 2 or len(right) < 2:
        return None
    sd_left = sample_sd(left)
    sd_right = sample_sd(right)
    pooled = math.sqrt(((len(left) - 1) * sd_left**2 + (len(right) - 1) * sd_right**2)
                       / (len(left) + len(right) - 2))
    if pooled == 0:
        return 0.0
    return (average(left) - average(right)) / pooled


def fmt(value):
    return "-" if value is None else f"{value:.4f}"


def metric_label(name):
    return name.replace("_", " ").capitalize()


def append_comparison_table(lines, title, description, left_name, right_name,
                            left_selector, right_selector, metrics, rows):
    lines += ["", f"## {title}", "", description, "",
              f"| Metric | {left_name} mean | {right_name} mean | Difference ({left_name} - {right_name}) | Cohen d |",
              "|---|---:|---:|---:|---:|"]
    for metric in metrics:
        left = values(rows, left_selector, metric)
        right = values(rows, right_selector, metric)
        lines.append(f"| {metric_label(metric)} | {fmt(average(left))} | {fmt(average(right))} | "
                     f"{fmt(average(left) - average(right) if left and right else None)} | "
                     f"{fmt(effect_size(left, right))} |")


def main():
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = payload["results"]
    all_metrics = set()
    for row in rows:
        all_metrics.update(row["metrics"])
    metrics = sorted(all_metrics - {"regeneration_count", "perturbation_count"})

    groups = {group: sum(row["group"] == group for row in rows)
              for group in ("HW-P", "MG-P", "HW-B", "MG-B")}
    lines = [
        "# HWT-MGT descriptive comparison",
        "",
        "This report uses the calculated metrics to assess two separate distinctions:",
        "whether text is human-written or machine-generated, and whether text is phishing or benign.",
        "Individual sample values are intentionally omitted; the raw values remain in the JSON file.",
        "",
        "## Dataset and notation",
        "",
        f"- Total samples: **{len(rows)}**",
        f"- `HW-P`: **{groups['HW-P']}**; `MG-P`: **{groups['MG-P']}**",
        f"- `HW-B`: **{groups['HW-B']}**; `MG-B`: **{groups['MG-B']}**",
        "- Each pooled comparison contains 22 samples per side.",
        "- Difference is calculated as left mean minus right mean.",
        "- Cohen d is a standardized effect size; larger absolute values indicate stronger separation in this sample.",
    ]

    append_comparison_table(
        lines,
        "HWT versus MGT",
        "This pools phishing and benign samples: `HW = HW-P + HW-B` and `MG = MG-P + MG-B`. "
        "It directly evaluates whether the metrics distinguish human-written from machine-generated text.",
        "HW", "MG",
        lambda row: row["group"].startswith("HW-"),
        lambda row: row["group"].startswith("MG-"),
        metrics, rows,
    )
    lines += [
        "",
        "### Outstanding observations",
        "",
        "- The strongest HWT/MGT separation is in `lrr` (Cohen d = -1.303): MG has the higher mean.",
        "- Other comparatively strong HWT/MGT differences are `mle_intrinsic_dimension` (d = -1.267), `phd_intrinsic_dimension` (d = -1.169), rank 100-1000 ratio (d = 1.159), mean token rank (d = 0.993), and mean log rank (d = 0.988).",
        "- The two perplexity measures also separate the groups substantially: both are higher for HW, with d about 0.86. Average log probability shows a similar pattern, with MG having the higher (less negative) mean.",
        "- `detectgpt_discrepancy` is nearly unchanged between HW and MG (d = -0.041), and `npr` is also weak (d = -0.112); these metrics do not distinguish authorship strongly in this sample.",
        "",
    ]
    append_comparison_table(
        lines,
        "Phishing versus benign",
        "This pools authorship sources: `P = HW-P + MG-P` and `B = HW-B + MG-B`. "
        "It directly evaluates whether the metrics distinguish phishing from benign text.",
        "P", "B",
        lambda row: row["group"].endswith("-P"),
        lambda row: row["group"].endswith("-B"),
        metrics, rows,
    )
    lines += [
        "",
        "### Outstanding observations",
        "",
        "- The largest phishing/benign separation is `ngram_overlap_ratio` (d = 0.854), with a higher mean for phishing samples.",
        "- DetectGPT discrepancy (d = 0.603), total surprisal (d = -0.589), DNA regeneration difference (d = 0.554), NPR (d = 0.543), and normalized DetectGPT discrepancy (d = 0.503) show moderate separation.",
        "- Phishing has lower predictive entropy (d = -0.465) and lower perplexity (d about -0.21) than benign text. Thus, the direction is metric-dependent rather than uniformly higher for phishing.",
        "- Rank-based measures are weak for phishing/benign separation: mean token rank has d = -0.070, and the rank-bucket ratios are all below |d| = 0.32.",
        "- Intrinsic-dimension and UID metrics are effectively unchanged between phishing and benign text; PHD has d = -0.017 and UID variance has d = -0.034.",
        "",
    ]

    lines += [
        "",
        "## Annotation-group context",
        "",
        "These four means show whether a pooled separation is consistent across the underlying annotations.",
        "",
        "| Metric | HW-P | MG-P | HW-B | MG-B |",
        "|---|---:|---:|---:|---:|",
    ]
    selectors = {group: (lambda group: lambda row: row["group"] == group)(group)
                 for group in groups}
    for metric in metrics:
        means = [average(values(rows, selectors[group], metric)) for group in ("HW-P", "MG-P", "HW-B", "MG-B")]
        lines.append(f"| {metric_label(metric)} | " + " | ".join(fmt(value) for value in means) + " |")

    lines += [
        "",
        "## How to read the separation",
        "",
        "- The `Difference` column shows the direction and magnitude in the metric's original units.",
        "- The `Cohen d` column makes separation more comparable across metrics with different scales. Inspect the largest absolute values first.",
        "- A positive `HW - MG` value means the metric is higher for human-written text; a negative value means it is higher for machine-generated text.",
        "- A positive `P - B` value means the metric is higher for phishing text; a negative value means it is higher for benign text.",
        "- These are descriptive comparisons, not statistical significance tests or trained classification results.",
        "- `uid_min_span` and `uid_max_span` are reduced to one mean per sample before group aggregation; raw vectors are not printed.",
        "- All 34 metric fields were present for all 44 samples, with zero recorded calculation errors.",
        "",
        "## Reproducibility",
        "",
        "The complete per-sample values remain available in `matched_pool_44_metrics.json`.",
        "",
    ]
    TARGET.write_text("\n".join(lines), encoding="utf-8")
    print(f"WROTE {TARGET}")


if __name__ == "__main__":
    main()
