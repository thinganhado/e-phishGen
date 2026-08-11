"""Stratum-adjusted factorial tests for HW/MG x phishing/benign results."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import t as student_t


ROOT = Path(__file__).resolve().parent
BOOTSTRAPS = 1000
SEED = 20260811
GROUPS = ("HW-P", "MG-P", "HW-B", "MG-B")
CONTRASTS = {
    "G_P": np.array([0, 1, 0, 1.0]),      # MG-P - HW-P
    "G_B": np.array([0, 1, 0, 0.0]),      # MG-B - HW-B
    "P_HW": np.array([0, 0, 1, 0.0]),     # HW-P - HW-B
    "P_MG": np.array([0, 0, 1, 1.0]),     # MG-P - MG-B
    "interaction": np.array([0, 0, 0, 1.0]),
}


def full_contrast(contrast, width):
    return np.pad(contrast, (0, width - len(contrast)))


def fmt(value):
    if not math.isfinite(value):
        return "NA"
    if abs(value) >= 1000 or (0 < abs(value) < 0.001):
        return f"{value:.3g}"
    return f"{value:.4f}".rstrip("0").rstrip(".")


def load_result(path):
    return json.loads(path.read_text(encoding="utf-8"))["results"]


def scalar_features(rows):
    keys = set()
    for row in rows:
        keys.update(row.get("metrics", {}))
    result = []
    for key in sorted(keys):
        values = [row.get("metrics", {}).get(key) for row in rows]
        if all(isinstance(value, (int, float)) and math.isfinite(value) for value in values) and np.ptp(values) > 1e-12:
            result.append(key)
    return result


def make_design(rows):
    strata = sorted({row["match_stratum"] for row in rows})
    baseline = strata[0]
    matrix = []
    for row in rows:
        group = row["group"]
        generation = float(group.startswith("MG-"))
        phishing = float(group.endswith("-P"))
        matrix.append([
            1.0, generation, phishing, generation * phishing,
            *[float(row["match_stratum"] == s) for s in strata[1:]],
        ])
    return np.asarray(matrix), strata, baseline


def fit(rows, feature):
    x, _, _ = make_design(rows)
    y = np.asarray([row["metrics"][feature] for row in rows], dtype=float)
    beta = np.linalg.pinv(x) @ y
    residual = y - x @ beta
    rank = np.linalg.matrix_rank(x)
    df = max(1, len(y) - rank)
    bread = np.linalg.pinv(x.T @ x)
    leverage = np.sum((x @ bread) * x, axis=1)
    scale = residual / np.maximum(1.0 - leverage, 1e-8)
    meat = (x * scale[:, None]).T @ (x * scale[:, None])
    covariance = bread @ meat @ bread
    return beta, covariance, df


def bootstrap(rows, feature, rng):
    cells = {}
    for row in rows:
        cells.setdefault((row["group"], row["match_stratum"]), []).append(row)
    samples = []
    for _ in range(BOOTSTRAPS):
        resampled = []
        for cell_rows in cells.values():
            indices = rng.integers(0, len(cell_rows), len(cell_rows))
            resampled.extend(cell_rows[index] for index in indices)
        beta, _, _ = fit(resampled, feature)
        samples.append([float(full_contrast(c, len(beta)) @ beta) for c in CONTRASTS.values()])
    return np.asarray(samples)


def p_value(beta, covariance, df, contrast):
    contrast = full_contrast(contrast, len(beta))
    estimate = float(contrast @ beta)
    variance = float(contrast @ covariance @ contrast)
    if variance <= 0 or not math.isfinite(variance):
        return 1.0 if estimate == 0 else 0.0
    statistic = abs(estimate) / math.sqrt(variance)
    return float(2 * student_t.sf(statistic, df))


def benjamini_hochberg(p_values):
    q_values = [float("nan")] * len(p_values)
    valid = sorted((p, i) for i, p in enumerate(p_values) if math.isfinite(p))
    running = 1.0
    for rank, (p, index) in reversed(list(enumerate(valid, 1))):
        running = min(running, p * len(valid) / rank)
        q_values[index] = min(1.0, running)
    return q_values


def result_rows(rows, features):
    rng = np.random.default_rng(SEED)
    output = []
    for feature in features:
        beta, covariance, df = fit(rows, feature)
        boot = bootstrap(rows, feature, rng)
        item = {"feature": feature}
        for index, (name, contrast) in enumerate(CONTRASTS.items()):
            estimate = float(full_contrast(contrast, len(beta)) @ beta)
            p = p_value(beta, covariance, df, contrast)
            lo, hi = np.quantile(boot[:, index], [0.025, 0.975])
            item[name] = {"estimate": estimate, "lo": float(lo), "hi": float(hi), "p": p}
        output.append(item)
    for name in CONTRASTS:
        qs = benjamini_hochberg([item[name]["p"] for item in output])
        for item, q in zip(output, qs):
            item[name]["q"] = q
    return output


def compact(effect):
    return f"{fmt(effect['estimate'])} [{fmt(effect['lo'])}, {fmt(effect['hi'])}], q={fmt(effect['q'])}"


def interpretation(item):
    gp, gb = item["G_P"]["estimate"], item["G_B"]["estimate"]
    phw, pmg = item["P_HW"]["estimate"], item["P_MG"]["estimate"]
    gen = "consistent" if gp * gb > 0 else "opposing/unclear"
    phishing = "consistent" if phw * pmg > 0 else "opposing/unclear"
    interaction = "small/uncertain" if item["interaction"]["q"] >= 0.05 else "evidence of interaction"
    return f"generation {gen}; phishing {phishing}; {interaction}"


def main():
    sections = []
    for path in sorted(ROOT.glob("*/results/*.json")):
        if path.name.endswith(".partial.json"):
            continue
        rows = load_result(path)
        features = scalar_features(rows)
        skipped = sorted(set().union(*(row.get("metrics", {}) for row in rows)) - set(features))
        analyses = result_rows(rows, features)
        sections.append((path.parent.parent.name, path, analyses, skipped))

    lines = [
        "# Factorial feature tests",
        "",
        "This analysis uses the four result cells HW-P, MG-P, HW-B, and MG-B.",
        "The model is a stratum-adjusted 2x2 linear model with generation, phishing,",
        "and generation x phishing interaction terms. Rows share matching strata but",
        "are not one-to-one document pairs, so paired tests were not used.",
        "",
        "Each cell contains 11 observations. Values below are adjusted contrasts",
        "reported as estimate [bootstrap 95% interval], with Benjamini-Hochberg q",
        "values computed separately for each contrast across features. Standard errors",
        "use HC3 heteroskedasticity-robust covariance. Results are exploratory because",
        "the sample is small and the features are correlated.",
        "",
        "| Contrast | Meaning |",
        "|---|---|",
        "| G_P | MG-P - HW-P: generation effect in phishing |",
        "| G_B | MG-B - HW-B: generation effect in benign text |",
        "| P_HW | HW-P - HW-B: phishing effect in human text |",
        "| P_MG | MG-P - MG-B: phishing effect in machine text |",
        "| interaction | G_P - G_B = P_MG - P_HW |",
        "",
    ]
    for name, path, analyses, skipped in sections:
        lines += [f"## {name}", "", f"Source: `{path.relative_to(ROOT)}`", ""]
        lines += [
            "| Feature | G_P | G_B | P_HW | P_MG | Interaction | Transferability reading |",
            "|---|---:|---:|---:|---:|---:|---|",
        ]
        for item in analyses:
            lines.append(
                f"| `{item['feature']}` | {compact(item['G_P'])} | {compact(item['G_B'])} | "
                f"{compact(item['P_HW'])} | {compact(item['P_MG'])} | {compact(item['interaction'])} | {interpretation(item)} |"
            )
        if skipped:
            lines += ["", "Skipped non-scalar metrics: " + ", ".join(f"`{x}`" for x in skipped) + "."]
        lines += ["", "### Candidate transferable features", ""]
        candidates = []
        for item in analyses:
            gen_consistent = item["G_P"]["estimate"] * item["G_B"]["estimate"] > 0
            ph_consistent = item["P_HW"]["estimate"] * item["P_MG"]["estimate"] > 0
            gen_support = "both q<0.05" if item["G_P"]["q"] < 0.05 and item["G_B"]["q"] < 0.05 else "one q<0.05" if min(item["G_P"]["q"], item["G_B"]["q"]) < 0.05 else "direction only"
            ph_support = "both q<0.05" if item["P_HW"]["q"] < 0.05 and item["P_MG"]["q"] < 0.05 else "one q<0.05" if min(item["P_HW"]["q"], item["P_MG"]["q"]) < 0.05 else "direction only"
            if gen_consistent and item["interaction"]["q"] >= 0.05:
                candidates.append(("MGT", item["feature"], min(item["G_P"]["q"], item["G_B"]["q"]), gen_support))
            if ph_consistent and item["interaction"]["q"] >= 0.05:
                candidates.append(("phishing", item["feature"], min(item["P_HW"]["q"], item["P_MG"]["q"]), ph_support))
        if candidates:
            lines += ["| Type | Feature | Minimum q | Evidence across both cells |", "|---|---|---:|---|"]
            for kind, feature, q, support in sorted(candidates, key=lambda x: (x[0], x[2], x[1])):
                lines.append(f"| {kind} | `{feature}` | {fmt(q)} | {support} |")
        else:
            lines.append("No direction-consistent candidates met the exploratory interaction criterion.")
        lines.append("")
    output = ROOT / "FACTORIAL_TESTS.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
