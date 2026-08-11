"""Descriptive distribution analysis for the calculation result JSON files.

Usage:
    python descriptive_analysis.py

The generated report is descriptive only. It does not perform hypothesis
testing or claim that a feature will generalize beyond this matched sample.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, median, stdev


ROOT = Path(__file__).resolve().parent
PAIRS = (("HW-P", "MG-P"), ("HW-B", "MG-B"))


def quantile(values, q):
    values = sorted(values)
    if not values:
        return float("nan")
    pos = (len(values) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return values[lo]
    return values[lo] + (values[hi] - values[lo]) * (pos - lo)


def skewness(values):
    if len(values) < 3:
        return 0.0
    m = mean(values)
    m2 = mean((x - m) ** 2 for x in values)
    if m2 == 0:
        return 0.0
    return mean((x - m) ** 3 for x in values) / (m2 ** 1.5)


def fmt(value):
    if not math.isfinite(value):
        return "NA"
    if abs(value) >= 1000 or (0 < abs(value) < 0.001):
        return f"{value:.3g}"
    return f"{value:.4f}".rstrip("0").rstrip(".")


def values_for(rows, group, key):
    values = []
    for row in rows:
        if row.get("group") != group:
            continue
        value = row.get("metrics", {}).get(key)
        if isinstance(value, list):
            values.extend(x for x in value if isinstance(x, (int, float)))
        elif isinstance(value, (int, float)) and math.isfinite(value):
            values.append(float(value))
    return values


def overlap_coefficient(a, b):
    """Histogram OVL, suitable as a compact descriptive overlap indicator."""
    combined = a + b
    if not combined or max(combined) == min(combined):
        return 1.0
    lo, hi = min(combined), max(combined)
    bins = min(20, max(5, int(math.sqrt(len(combined)))))
    width = (hi - lo) / bins
    ca = [0] * bins
    cb = [0] * bins
    for value in a:
        ca[min(bins - 1, int((value - lo) / width))] += 1
    for value in b:
        cb[min(bins - 1, int((value - lo) / width))] += 1
    return sum(min(x / len(a), y / len(b)) for x, y in zip(ca, cb))


def peak_count(values):
    """Return a conservative histogram peak count; small-n results are tentative."""
    if len(values) < 8 or max(values) == min(values):
        return 1
    lo, hi = min(values), max(values)
    bins = min(12, max(5, int(math.sqrt(len(values)))))
    width = (hi - lo) / bins
    counts = [0] * bins
    for value in values:
        counts[min(bins - 1, int((value - lo) / width))] += 1
    peaks = 0
    for i, count in enumerate(counts):
        left = counts[i - 1] if i else -1
        right = counts[i + 1] if i + 1 < bins else -1
        if count >= left and count >= right and count >= max(2, len(values) * 0.12):
            peaks += 1
    return max(1, peaks)


def outlier_count(values):
    q1, q3 = quantile(values, 0.25), quantile(values, 0.75)
    iqr = q3 - q1
    if iqr == 0:
        return sum(x != q1 for x in values)
    return sum(x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr for x in values)


def shape_note(a, b):
    sd_a = stdev(a) if len(a) > 1 else 0.0
    sd_b = stdev(b) if len(b) > 1 else 0.0
    ratio = sd_b / sd_a if sd_a else float("inf") if sd_b else 1.0
    skew_delta = skewness(b) - skewness(a)
    notes = []
    if ratio > 1.5 or ratio < 2 / 3:
        notes.append(f"variance {'higher' if ratio > 1 else 'lower'} in MG (SD ratio {fmt(ratio)})")
    if abs(skew_delta) >= 1:
        notes.append(f"skew changes ({'more' if skew_delta > 0 else 'less'} right-skewed in MG)")
    peaks_a, peaks_b = peak_count(a), peak_count(b)
    if peaks_a > 1 or peaks_b > 1:
        notes.append(f"possible multimodality (peaks HW/MG {peaks_a}/{peaks_b}; tentative at n={len(a)})")
    out_a, out_b = outlier_count(a), outlier_count(b)
    if out_a or out_b:
        notes.append(f"Tukey outliers HW/MG {out_a}/{out_b}")
    return "; ".join(notes) if notes else "no prominent variance/skew/shape change"


def analyze(rows, group_a, group_b, key):
    a, b = values_for(rows, group_a, key), values_for(rows, group_b, key)
    if not a or not b:
        return None
    ma, mb = mean(a), mean(b)
    med_a, med_b = median(a), median(b)
    pooled_sd = stdev(a + b) if len(a + b) > 1 else 0.0
    effect = (mb - ma) / pooled_sd if pooled_sd else 0.0
    if abs(effect) >= 0.8:
        location = "clear MG shift"
    elif abs(effect) >= 0.4:
        location = "moderate MG shift"
    elif abs(effect) >= 0.2:
        location = "small MG shift"
    else:
        location = "essentially overlapping location"
    direction = "higher" if effect > 0 else "lower" if effect < 0 else "same"
    return {
        "n_a": len(a), "n_b": len(b), "mean_a": ma, "mean_b": mb,
        "median_a": med_a, "median_b": med_b,
        "q1_a": quantile(a, .25), "q3_a": quantile(a, .75),
        "q1_b": quantile(b, .25), "q3_b": quantile(b, .75),
        "sd_a": stdev(a) if len(a) > 1 else 0.0,
        "sd_b": stdev(b) if len(b) > 1 else 0.0,
        "skew_a": skewness(a), "skew_b": skewness(b),
        "effect": effect, "location": f"{location}; MG {direction}",
        "overlap": overlap_coefficient(a, b), "shape": shape_note(a, b),
    }


def main():
    reports = []
    for result_path in sorted(ROOT.glob("*/results/*.json")):
        if result_path.name.endswith(".partial.json"):
            continue
        payload = json.loads(result_path.read_text(encoding="utf-8"))
        rows = payload.get("results", [])
        reports.append((result_path.parent.parent.name, result_path, rows))

    lines = [
        "# Descriptive distribution analysis",
        "",
        "This report compares HW-P with MG-P and HW-B with MG-B independently.",
        "It describes the observed matched sample only (`n=11` per class per pair);",
        "it is not a significance test or a generalization claim.",
        "",
        "Interpretation: `effect` is the signed MG-minus-HW difference divided by",
        "the pooled sample SD. The histogram overlap coefficient (OVL) ranges from",
        "0 (little overlap) to 1 (complete overlap). Shape flags use Tukey outliers",
        "and conservative histogram diagnostics; multimodality flags are tentative",
        "at this small sample size.",
        "UID span metrics are vector-valued in the source JSON; their rows pool all",
        "available span elements and should not be interpreted as 11 independent",
        "document-level observations.",
        "",
    ]
    for name, path, rows in reports:
        keys = sorted(set().union(*(row.get("metrics", {}) for row in rows)))
        lines += [f"## {name}", "", f"Source: `{path.relative_to(ROOT)}`", ""]
        for group_a, group_b in PAIRS:
            lines += [f"### {group_a} vs {group_b}", "", "| Feature | HW median [Q1, Q3] | MG median [Q1, Q3] | Mean HW → MG | Effect | OVL | Shape notes |", "|---|---:|---:|---:|---:|---:|---|"]
            for key in keys:
                result = analyze(rows, group_a, group_b, key)
                if not result:
                    continue
                lines.append(
                    f"| `{key}` | {fmt(result['median_a'])} [{fmt(result['q1_a'])}, {fmt(result['q3_a'])}] | "
                    f"{fmt(result['median_b'])} [{fmt(result['q1_b'])}, {fmt(result['q3_b'])}] | "
                    f"{fmt(result['mean_a'])} -> {fmt(result['mean_b'])} ({result['location']}) | "
                    f"{result['effect']:.2f} | {result['overlap']:.2f} | {result['shape']} |"
                )
            lines += ["", "Constant-valued metrics and metrics missing from either class are omitted.", ""]
    output = ROOT / "DESCRIPTIVE_ANALYSIS.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
