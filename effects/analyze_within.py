#!/usr/bin/env python
"""Estimate within-dataset Generation, Phishing, and Interaction effects.

Example::

    python effects/analyze_within.py \
      --dataset-id scaled_8980 \
      --samples scaled_stratified_pool_8980.json \
      --metrics phishing=calculation/Phishing/results/scaled_stratified_pool_8980_phishing_metrics.json \
      --metrics stylometric=calculation/Stylometric/results/scaled_stratified_pool_8980_stylometric_metrics.json \
      --output effects/results/scaled_8980

Use ``--allow-partial`` explicitly for checkpoint files. Feature-level
completeness and four-cell support are then checked conservatively.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from effects.core import (  # noqa: E402
    ALL_CONTRASTS,
    GROUPS,
    MAIN_EFFECTS,
    analyze_outcome,
    benjamini_hochberg,
    classify_feature,
    effect_codes,
    hedges_correction,
    json_safe,
    supported_rows,
)
from effects.io_utils import (  # noqa: E402
    dataset_diagnostics,
    feature_candidates,
    load_metric_family,
    load_samples,
    read_json,
    sha256_file,
)
from effects.plotting import plot_top_interactions, plot_within_effect_heatmap  # noqa: E402


SCHEMA_VERSION = "ephishgen.effects.within.v2"
IMPLEMENTATION_VERSION = "1.1.0"


def _signature(label: str, specification: Mapping[str, Any]) -> str:
    encoded = json.dumps(specification, sort_keys=True, separators=(",", ":"))
    return label + ":" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:20]


def _run_config_signature(config: Mapping[str, Any]) -> str:
    specification = {
        "implementation_version": IMPLEMENTATION_VERSION,
        "schema_version": SCHEMA_VERSION,
        "factor_coding": {"HW": -0.5, "MG": 0.5, "B": -0.5, "P": 0.5},
        "formula": "metric ~ G + P + G:P + match_stratum fixed effects",
        "covariance": "CR1" if config["cluster_field"] else "HC3",
        "cluster_field": config["cluster_field"],
        "equal_stratum": config["equal_stratum"],
        "length_sensitivity": config.get("length_sensitivity", False),
        "standardization": "residual SD; exact Hedges J; approximate delta SE v1",
        "alpha": config["alpha"],
        "equivalence_bound": config["equivalence_bound"],
        "minimum_effect": config["minimum_effect"],
        "min_cell_n": config["min_cell_n"],
        "length_reference_words": config.get("length_reference_words", 100.0),
    }
    return _signature("ephishgen-effects-run", specification)


def _estimator_signatures(
    config: Mapping[str, Any],
    length_measurement: Mapping[str, Any] | None = None,
) -> dict[str, str]:
    """Per-variant compatibility signatures, excluding unrelated reporting options."""

    base = {
        "estimator_spec_version": "2",
        "factor_coding": {"HW": -0.5, "MG": 0.5, "B": -0.5, "P": 0.5},
        "formula": "G + P + G:P + match_stratum fixed effects",
        "covariance": (
            "CR1 cluster-robust with cluster degrees of freedom; independent-unit field="
            + str(config.get("cluster_field"))
            if config.get("cluster_field")
            else "HC3 heteroskedasticity-robust with residual degrees of freedom"
        ),
        "standardization": "full-model residual SD; exact Hedges J v1",
        "standardized_se": "delta method with residual-scale uncertainty v1",
    }
    specifications: dict[str, dict[str, Any]] = {
        "sample_weighted": {**base, "weighting": "one per document"},
    }
    if config["equal_stratum"]:
        specifications["equal_stratum"] = {
            **base,
            "weighting": "equal total weight per stratum-by-group cell",
        }
    if config.get("length_sensitivity", False):
        reference = float(config.get("length_reference_words", 100.0))
        measurement_definition = {
            key: value
            for key, value in dict(length_measurement or {}).items()
            if key in {"method", "field", "pattern", "engine"}
        }
        specifications["length_adjusted"] = {
            **base,
            "weighting": "one per document",
            "length": "log1p word count linear and quadratic common curve",
            "reference_words": reference,
            "length_measurement": measurement_definition,
        }
        specifications["length_adjusted_varying_slopes"] = {
            **base,
            "weighting": "one per document",
            "length": (
                "log1p word count linear/quadratic common curve plus "
                "G/P/G:P-specific linear slopes"
            ),
            "reference_words": reference,
            "length_measurement": measurement_definition,
        }
        specifications["length_common_support"] = {
            **base,
            "weighting": "one per document",
            "length": "dataset-specific observed min/max range overlap",
            "length_measurement": measurement_definition,
        }
    return {
        variant: _signature("ephishgen-estimator", specification)
        for variant, specification in specifications.items()
    }


def _metric_spec(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Expected FAMILY=PATH")
    family, path = value.split("=", 1)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", family):
        raise argparse.ArgumentTypeError(f"Invalid metric family {family!r}")
    if not path:
        raise argparse.ArgumentTypeError("Metric path cannot be empty")
    return family, path


def _signature_spec(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Expected FAMILY=SIGNATURE")
    family, signature = value.split("=", 1)
    if not family or not signature:
        raise argparse.ArgumentTypeError("Family and signature must be nonempty")
    return family, signature


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fit stratum-adjusted 2x2 Generation x Phishing models, standardized "
            "G/P/I effects, equivalence tests, diagnostics, and interaction plots."
        )
    )
    parser.add_argument("--manifest", type=Path, help="JSON manifest; CLI values override it")
    parser.add_argument("--dataset-id", help="Stable ID used in within/meta outputs")
    parser.add_argument("--samples", type=Path, help="Dataset JSON containing samples")
    parser.add_argument(
        "--metrics",
        action="append",
        type=_metric_spec,
        metavar="FAMILY=PATH",
        help="Calculation result JSON; repeat for each family",
    )
    parser.add_argument(
        "--signature",
        action="append",
        type=_signature_spec,
        metavar="FAMILY=SIGNATURE",
        help="Measurement signature override used to align metrics across datasets",
    )
    parser.add_argument("--output", type=Path, help="Output directory")
    parser.add_argument(
        "--independence-group",
        help="Pools from the same corpora/cohort must share this value for meta-analysis",
    )
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        default=None,
        help="Permit partial files/features; output is explicitly provisional",
    )
    parser.add_argument(
        "--cluster-field",
        help="Sample field identifying independent clusters (e.g. base_prompt_id)",
    )
    parser.add_argument("--alpha", type=float, help="Test/FDR alpha (default 0.05)")
    parser.add_argument(
        "--equivalence-bound",
        type=float,
        help="Standardized +/- SESOI for TOST (default 0.2)",
    )
    parser.add_argument(
        "--minimum-effect",
        type=float,
        help="Minimum absolute standardized effect for taxonomy (default 0.2)",
    )
    parser.add_argument(
        "--min-cell-n",
        type=int,
        help="Minimum observations in every group within an included stratum (default 1)",
    )
    parser.add_argument(
        "--no-equal-stratum",
        action="store_true",
        default=None,
        help="Disable the equal-stratum robustness variant",
    )
    parser.add_argument(
        "--length-sensitivity",
        action="store_true",
        default=None,
        help=(
            "Add declared log-length-adjusted, varying-slope, and four-group "
            "observed-range-overlap sensitivity variants"
        ),
    )
    parser.add_argument(
        "--length-reference-words",
        type=float,
        help=(
            "Predeclared physical reference for conditional length effects "
            "(default 100 words)"
        ),
    )
    parser.add_argument("--no-plots", action="store_true", default=None)
    parser.add_argument("--max-plot-features", type=int, help="Heatmap row limit (default 50)")
    parser.add_argument("--top-interactions", type=int, help="Interaction-plot limit (default 12)")
    return parser


def _resolve_path(value: str | Path | None, base: Path) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def _manifest_metrics(raw: Any, base: Path) -> list[tuple[str, Path, str | None]]:
    if raw is None:
        return []
    result = []
    if isinstance(raw, Mapping):
        raw = [
            {"family": family, **({"path": value} if isinstance(value, str) else dict(value))}
            for family, value in raw.items()
        ]
    if not isinstance(raw, list):
        raise ValueError("manifest metrics must be a list or object")
    for item in raw:
        if not isinstance(item, Mapping) or "family" not in item or "path" not in item:
            raise ValueError("Each manifest metric needs family and path")
        result.append(
            (
                str(item["family"]),
                _resolve_path(item["path"], base),
                str(item["signature"]) if item.get("signature") else None,
            )
        )
    return result


def resolve_config(args: argparse.Namespace) -> dict[str, Any]:
    manifest: dict[str, Any] = {}
    base = Path.cwd()
    if args.manifest:
        manifest_path = args.manifest.resolve()
        manifest = read_json(manifest_path)
        if not isinstance(manifest, Mapping):
            raise ValueError("Manifest must contain a JSON object")
        manifest = dict(manifest)
        allowed_manifest_fields = {
            "dataset_id",
            "samples",
            "output",
            "metrics",
            "signatures",
            "independence_group",
            "allow_partial",
            "cluster_field",
            "alpha",
            "equivalence_bound",
            "minimum_effect",
            "min_cell_n",
            "no_equal_stratum",
            "length_sensitivity",
            "length_reference_words",
            "no_plots",
            "max_plot_features",
            "top_interactions",
        }
        unknown_fields = sorted(set(manifest) - allowed_manifest_fields)
        if unknown_fields:
            raise ValueError(
                "Unknown within-manifest fields: " + ", ".join(unknown_fields)
            )
        base = manifest_path.parent

    dataset_id = args.dataset_id or manifest.get("dataset_id")
    samples = args.samples.resolve() if args.samples else _resolve_path(manifest.get("samples"), base)
    output = args.output.resolve() if args.output else _resolve_path(manifest.get("output"), base)
    if not dataset_id or samples is None or output is None:
        raise ValueError("dataset-id, samples, and output are required (CLI or manifest)")

    signatures = {
        str(key): str(value) for key, value in dict(manifest.get("signatures", {})).items()
    }
    cli_signatures = dict(args.signature or [])
    if args.signature:
        signatures.update(cli_signatures)
    metrics = _manifest_metrics(manifest.get("metrics"), base)
    inline_manifest_signatures = {
        family: signature
        for family, _, signature in metrics
        if signature is not None
    }
    if args.metrics:
        metrics = [
            (
                family,
                _resolve_path(path, Path.cwd()),
                cli_signatures.get(
                    family,
                    signatures.get(family, inline_manifest_signatures.get(family)),
                ),
            )
            for family, path in args.metrics
        ]
    else:
        metrics = [
            (
                family,
                path,
                cli_signatures.get(family, signature or signatures.get(family)),
            )
            for family, path, signature in metrics
        ]
    if not metrics:
        raise ValueError("At least one --metrics FAMILY=PATH input is required")
    families = [family for family, _, _ in metrics]
    if len(families) != len(set(families)):
        raise ValueError("Metric family names must be unique within one analysis")

    def setting(name: str, cli_value: Any, default: Any) -> Any:
        return cli_value if cli_value is not None else manifest.get(name, default)

    def boolean_setting(name: str, cli_value: Any, default: bool) -> bool:
        value = setting(name, cli_value, default)
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be a JSON boolean, not {value!r}")
        return value

    explicit_independence_group = (
        args.independence_group
        if args.independence_group is not None
        else manifest.get("independence_group")
    )
    if explicit_independence_group is not None and (
        not isinstance(explicit_independence_group, str)
        or not explicit_independence_group.strip()
    ):
        raise ValueError("independence_group must be a nonempty string when declared")
    if isinstance(explicit_independence_group, str):
        explicit_independence_group = explicit_independence_group.strip()
    config = {
        "dataset_id": str(dataset_id),
        "samples": samples,
        "metrics": metrics,
        "output": output,
        "independence_group": str(
            explicit_independence_group or dataset_id
        ),
        "independence_group_explicit": explicit_independence_group is not None,
        "allow_partial": boolean_setting("allow_partial", args.allow_partial, False),
        "cluster_field": args.cluster_field or manifest.get("cluster_field"),
        "alpha": float(setting("alpha", args.alpha, 0.05)),
        "equivalence_bound": float(
            setting("equivalence_bound", args.equivalence_bound, 0.2)
        ),
        "minimum_effect": float(setting("minimum_effect", args.minimum_effect, 0.2)),
        "min_cell_n": int(setting("min_cell_n", args.min_cell_n, 1)),
        "equal_stratum": not boolean_setting(
            "no_equal_stratum", args.no_equal_stratum, False
        ),
        "length_sensitivity": boolean_setting(
            "length_sensitivity", args.length_sensitivity, False
        ),
        "length_reference_words": float(
            setting("length_reference_words", args.length_reference_words, 100.0)
        ),
        "plots": not boolean_setting("no_plots", args.no_plots, False),
        "max_plot_features": int(
            setting("max_plot_features", args.max_plot_features, 50)
        ),
        "top_interactions": int(
            setting("top_interactions", args.top_interactions, 12)
        ),
        "manifest": str(args.manifest.resolve()) if args.manifest else None,
    }
    numeric_settings = {
        "alpha": config["alpha"],
        "equivalence_bound": config["equivalence_bound"],
        "minimum_effect": config["minimum_effect"],
        "length_reference_words": config["length_reference_words"],
    }
    if not all(math.isfinite(float(value)) for value in numeric_settings.values()):
        raise ValueError("All numeric effect-analysis settings must be finite")
    if not (0 < config["alpha"] < 0.5):
        raise ValueError("alpha must be between 0 and 0.5")
    if config["equivalence_bound"] <= 0 or config["minimum_effect"] < 0:
        raise ValueError("Effect and equivalence thresholds must be positive")
    if config["length_reference_words"] < 0:
        raise ValueError("length-reference-words must be nonnegative")
    if config["min_cell_n"] < 1:
        raise ValueError("min-cell-n must be at least 1")
    if config["max_plot_features"] < 1 or config["top_interactions"] < 1:
        raise ValueError("Plot feature/count limits must be at least 1")
    return config


def _clusters(rows: Sequence[Mapping[str, Any]], field: str | None) -> list[str] | None:
    if field is None:
        return None
    missing = [str(row["sample_id"]) for row in rows if row.get(field) in (None, "")]
    if missing:
        raise ValueError(
            f"Cluster field {field!r} is missing for {len(missing)} fitted rows; "
            f"first IDs: {missing[:5]}"
        )
    return [str(row[field]) for row in rows]


def _provided_word_count(row: Mapping[str, Any]) -> float | None:
    value = row.get("word_count")
    if (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and math.isfinite(float(value))
        and float(value) >= 0
    ):
        return float(value)
    return None


def _regex_word_count(row: Mapping[str, Any]) -> float | None:
    text = row.get("text")
    if isinstance(text, str):
        return float(len(re.findall(r"\b\w+\b", text, flags=re.UNICODE)))
    return None


def _length_summary(values: Sequence[float]) -> dict[str, Any]:
    array = np.asarray(values, dtype=float)
    return {
        "n": int(len(array)),
        "mean": float(np.mean(array)),
        "median": float(np.median(array)),
        "sd": float(np.std(array, ddof=1)) if len(array) > 1 else None,
        "minimum": float(np.min(array)),
        "maximum": float(np.max(array)),
    }


def _stratum_effects(
    rows: Sequence[Mapping[str, Any]],
    values: Sequence[float],
    primary_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Descriptive G/P/I contrasts by stratum, standardized on one common scale."""

    by_stratum: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row, value in zip(rows, values):
        by_stratum[str(row.get("match_stratum", "__all__"))][
            str(row["group"])
        ].append(float(value))

    residual_sd = float(primary_result["residual_sd"])
    correction = hedges_correction(int(primary_result["df_residual"]))
    scale = (
        correction / residual_sd
        if residual_sd > 0 and math.isfinite(residual_sd) and math.isfinite(correction)
        else None
    )
    summaries = []
    for stratum, cells in sorted(by_stratum.items()):
        if any(not cells.get(group) for group in GROUPS):
            continue
        means = {group: float(np.mean(cells[group])) for group in GROUPS}
        raw_effects = {
            "G": 0.5
            * ((means["MG-P"] - means["HW-P"]) + (means["MG-B"] - means["HW-B"])),
            "P": 0.5
            * ((means["HW-P"] - means["HW-B"]) + (means["MG-P"] - means["MG-B"])),
            "I": (means["MG-P"] - means["HW-P"])
            - (means["MG-B"] - means["HW-B"]),
        }
        summaries.append(
            {
                "stratum": stratum,
                "n_by_group": {group: len(cells[group]) for group in GROUPS},
                "cell_means": means,
                "effects_raw": raw_effects,
                "effects_standardized_common_residual_sd": {
                    effect: value * scale if scale is not None else None
                    for effect, value in raw_effects.items()
                },
                "inferential_status": "descriptive_only",
            }
        )
    return summaries


def _affine_duplicate_pairs(candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    pairs = []
    for left_index, left in enumerate(candidates):
        left_ids = tuple(str(row["sample_id"]) for row in left["rows"])
        left_values = np.asarray(left["values"], dtype=float)
        left_sd = float(np.std(left_values))
        if left_sd <= 0:
            continue
        for right in candidates[left_index + 1 :]:
            if left_ids != tuple(str(row["sample_id"]) for row in right["rows"]):
                continue
            right_values = np.asarray(right["values"], dtype=float)
            right_sd = float(np.std(right_values))
            if right_sd <= 0:
                continue
            correlation = float(np.corrcoef(left_values, right_values)[0, 1])
            if math.isfinite(correlation) and abs(correlation) >= 1.0 - 1e-12:
                slope = correlation * right_sd / left_sd
                intercept = float(np.mean(right_values) - slope * np.mean(left_values))
                pairs.append(
                    {
                        "left": left["feature"],
                        "right": right["feature"],
                        "correlation": correlation,
                        "right_equals_intercept_plus_slope_left": {
                            "intercept": intercept,
                            "slope": slope,
                        },
                    }
                )
    return pairs


def _apply_fdr(
    features: list[dict[str, Any]],
    variants: Sequence[str],
    alpha: float,
    minimum_effect: float,
) -> None:
    families = sorted({feature["family"] for feature in features})
    for family in families:
        family_features = [feature for feature in features if feature["family"] == family]
        for variant in variants:
            available = [feature for feature in family_features if variant in feature["variants"]]
            for contrast in ALL_CONTRASTS:
                p_values = [
                    feature["variants"][variant]["contrasts"][contrast]["raw"]["p"]
                    for feature in available
                ]
                for feature, q_value in zip(available, benjamini_hochberg(p_values)):
                    feature["variants"][variant]["contrasts"][contrast]["raw"]["q"] = q_value
            for contrast in MAIN_EFFECTS:
                p_values = [
                    feature["variants"][variant]["contrasts"][contrast]["equivalence"]["p_tost"]
                    for feature in available
                ]
                for feature, q_value in zip(available, benjamini_hochberg(p_values)):
                    equivalence = feature["variants"][variant]["contrasts"][contrast]["equivalence"]
                    equivalence["q_tost"] = q_value
                    equivalence["equivalent_unadjusted"] = equivalence["equivalent"]
                    equivalence["equivalent"] = bool(q_value is not None and q_value < alpha)
    for feature in features:
        feature["variant_classifications"] = {
            variant: classify_feature(
                result["contrasts"],
                alpha=alpha,
                minimum_effect=minimum_effect,
            )
            for variant, result in feature["variants"].items()
        }
        feature["classification"] = feature["variant_classifications"][
            "sample_weighted"
        ]


def run_analysis(config: Mapping[str, Any]) -> dict[str, Any]:
    samples, sample_metadata = load_samples(
        config["samples"], min_cell_n=config["min_cell_n"]
    )
    diagnostics = dataset_diagnostics(samples)
    if config["cluster_field"]:
        _clusters(samples, config["cluster_field"])
    variants = ["sample_weighted"]
    if config["equal_stratum"]:
        variants.append("equal_stratum")

    provided_counts = [_provided_word_count(sample) for sample in samples]
    regex_counts = [_regex_word_count(sample) for sample in samples]
    if all(value is not None for value in regex_counts):
        length_measurement = {
            "method": "unicode_regex_token_count",
            "pattern": r"\b\w+\b",
            "engine": "Python re UNICODE",
            "uniform_across_rows": True,
            "reason": "Text was available for every row, so one explicit rule was applied uniformly",
        }
        word_count_by_id = {
            str(sample["sample_id"]): float(value)
            for sample, value in zip(samples, regex_counts)
        }
    elif all(value is not None for value in provided_counts):
        length_measurement = {
            "method": "provided_word_count_field",
            "field": "word_count",
            "uniform_across_rows": True,
            "reason": "Text was unavailable for at least one row; the complete provided field was used",
        }
        word_count_by_id = {
            str(sample["sample_id"]): float(value)
            for sample, value in zip(samples, provided_counts)
        }
    else:
        length_measurement = {
            "method": "unavailable",
            "uniform_across_rows": True,
            "invalid_or_missing_provided_rows": sum(
                value is None for value in provided_counts
            ),
            "missing_text_rows": sum(value is None for value in regex_counts),
        }
        word_count_by_id = {
            str(sample["sample_id"]): None for sample in samples
        }
    complete_word_counts = all(
        value is not None for value in word_count_by_id.values()
    )
    word_counts = (
        [float(word_count_by_id[str(sample["sample_id"])]) for sample in samples]
        if complete_word_counts
        else []
    )
    common_length_support: tuple[float, float] | None = None
    length_requested = bool(config.get("length_sensitivity", False))
    length_available = bool(word_counts and np.ptp(word_counts) > 1e-12)
    length_diagnostics: dict[str, Any] = {
        "requested": length_requested,
        "available": length_available,
        "missing_word_counts": sum(
            value is None for value in word_count_by_id.values()
        ),
        "measurement": length_measurement,
        "interpretation": (
            "Sensitivity estimands only: length may mediate generation or phishing effects, "
            "so the unadjusted sample-weighted model remains primary."
        ),
    }
    diagnostics["word_count_measurement"] = length_measurement
    if complete_word_counts:
        diagnostics["word_count_by_group"] = {
            group: _length_summary(
                [
                    float(word_count_by_id[str(sample["sample_id"])])
                    for sample in samples
                    if sample["group"] == group
                ]
            )
            for group in GROUPS
        }
    if length_available:
        lengths_by_group = {
            group: [
                float(word_count_by_id[str(sample["sample_id"])])
                for sample in samples
                if sample["group"] == group
            ]
            for group in GROUPS
        }
        lower = max(min(values) for values in lengths_by_group.values())
        upper = min(max(values) for values in lengths_by_group.values())
        if lower <= upper:
            common_length_support = (lower, upper)
            retained_lengths = {
                group: [value for value in values if lower <= value <= upper]
                for group, values in lengths_by_group.items()
            }
            length_diagnostics["common_support"] = {
                "method": (
                    "intersection of observed group min/max ranges; range restriction only, "
                    "not distribution balancing"
                ),
                "lower_words": lower,
                "upper_words": upper,
                "retained_by_group": {
                    group: sum(lower <= value <= upper for value in values)
                    for group, values in lengths_by_group.items()
                },
                "original_by_group": {
                    group: len(values) for group, values in lengths_by_group.items()
                },
                "retained_word_count_by_group": {
                    group: _length_summary(values)
                    for group, values in retained_lengths.items()
                },
                "limitations": (
                    "Observed extrema are outlier-sensitive and retained group length "
                    "distributions can still differ."
                ),
            }
            reference_words = float(config.get("length_reference_words", 100.0))
            reference_supported = lower <= reference_words <= upper
            length_diagnostics["conditional_reference_support"] = {
                "reference_words": reference_words,
                "inside_all_group_observed_ranges": reference_supported,
                "four_group_overlap_lower_words": lower,
                "four_group_overlap_upper_words": upper,
                "distance_below_overlap": max(0.0, lower - reference_words),
                "distance_above_overlap": max(0.0, reference_words - upper),
            }
            if length_requested and not reference_supported:
                raise ValueError(
                    f"length-reference-words={reference_words:g} lies outside the "
                    f"four-group observed overlap [{lower:g}, {upper:g}]; choose a "
                    "predeclared supported reference or omit length sensitivity"
                )
        else:
            length_diagnostics["common_support"] = None
            length_diagnostics["common_support_warning"] = (
                "The four groups have no overlapping observed word-count range."
            )
    if length_requested and length_available:
        variants.append("length_adjusted")
        variants.append("length_adjusted_varying_slopes")
        if common_length_support is not None:
            variants.append("length_common_support")
    elif length_requested:
        diagnostics.setdefault("warnings", []).append(
            "Length sensitivity was requested but complete, varying word counts could not be derived."
        )
    diagnostics["length_sensitivity"] = length_diagnostics

    if word_counts and np.ptp(word_counts) > 1e-12:
        word_count_effects: dict[str, Any] = {}
        word_count_errors: dict[str, str] = {}
        for variant in variants:
            if variant not in ("sample_weighted", "equal_stratum"):
                continue
            try:
                word_count_effects[variant] = analyze_outcome(
                    samples,
                    word_counts,
                    weighting=(
                        "sample" if variant == "sample_weighted" else "equal_stratum"
                    ),
                    alpha=config["alpha"],
                    equivalence_bound=config["equivalence_bound"],
                    clusters=_clusters(samples, config["cluster_field"]),
                )
            except (ValueError, np.linalg.LinAlgError) as exc:
                word_count_errors[variant] = str(exc)
        diagnostics["word_count_factorial_effects"] = word_count_effects
        diagnostics["word_count_factorial_effect_errors"] = word_count_errors
        if word_count_errors:
            diagnostics.setdefault("warnings", []).append(
                "Some word-count diagnostic models were not estimable: "
                + "; ".join(
                    f"{variant}: {error}"
                    for variant, error in sorted(word_count_errors.items())
                )
            )

    features: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    family_diagnostics: dict[str, Any] = {}
    input_metrics = []
    provisional = bool(config["allow_partial"])

    for family, path, signature in config["metrics"]:
        loaded = load_metric_family(
            path,
            family,
            samples,
            allow_partial=config["allow_partial"],
            signature_override=signature,
        )
        candidates, family_skipped = feature_candidates(
            loaded["rows"],
            allow_partial=config["allow_partial"],
            min_cell_n=config["min_cell_n"],
        )
        affine_pairs = _affine_duplicate_pairs(candidates)
        family_diagnostics[family] = {
            "input_path": loaded["path"],
            "partial_file": loaded["partial_file"],
            "partial_reasons": loaded["partial_reasons"],
            "missing_sample_rows": loaded["missing_sample_rows"],
            "observed_feature_count": loaded["observed_feature_count"],
            "expected_feature_count": loaded["expected_feature_count"],
            "missing_expected_features": loaded["missing_expected_features"],
            "incomplete_expected_features": loaded["incomplete_expected_features"],
            "incomplete_observed_features": loaded["incomplete_observed_features"],
            "rows_with_errors": loaded["rows_with_errors"],
            "candidate_features": len(candidates),
            "skipped_features": len(family_skipped),
            "affine_duplicate_pairs": affine_pairs,
        }
        input_metrics.append(
            {
                key: loaded[key]
                for key in (
                    "family",
                    "path",
                    "sha256",
                    "partial_file",
                    "partial_filename",
                    "partial_reasons",
                    "explicit_status",
                    "missing_sample_rows",
                    "observed_feature_count",
                    "expected_feature_count",
                    "missing_expected_features",
                    "incomplete_expected_features",
                    "incomplete_observed_features",
                    "rows_with_errors",
                    "metadata",
                    "metric_signature",
                )
            }
        )
        provisional = provisional or loaded["partial_file"]
        skipped.extend({"family": family, **item} for item in family_skipped)

        for position, candidate in enumerate(candidates, 1):
            print(
                f"[{family}] {position}/{len(candidates)} {candidate['feature']}",
                flush=True,
            )
            variant_results: dict[str, Any] = {}
            variant_errors: dict[str, str] = {}
            try:
                variant_results["sample_weighted"] = analyze_outcome(
                    candidate["rows"],
                    candidate["values"],
                    weighting="sample",
                    alpha=config["alpha"],
                    equivalence_bound=config["equivalence_bound"],
                    clusters=_clusters(candidate["rows"], config["cluster_field"]),
                )
            except (ValueError, np.linalg.LinAlgError) as exc:
                skipped.append(
                    {
                        "family": family,
                        "feature": candidate["feature"],
                        "reason": "model_not_estimable",
                        "details": str(exc),
                        **candidate["completeness"],
                    }
                )
                continue

            if "equal_stratum" in variants:
                try:
                    variant_results["equal_stratum"] = analyze_outcome(
                        candidate["rows"],
                        candidate["values"],
                        weighting="equal_stratum",
                        alpha=config["alpha"],
                        equivalence_bound=config["equivalence_bound"],
                        clusters=_clusters(candidate["rows"], config["cluster_field"]),
                    )
                except (ValueError, np.linalg.LinAlgError) as exc:
                    variant_errors["equal_stratum"] = str(exc)

            if "length_adjusted" in variants:
                z_length: np.ndarray | None = None
                try:
                    log_lengths = np.log1p(
                        np.asarray(
                            [
                                word_count_by_id[str(row["sample_id"])]
                                for row in candidate["rows"]
                            ],
                            dtype=float,
                        )
                    )
                    log_mean = float(np.mean(log_lengths))
                    log_sd = float(np.std(log_lengths))
                    if log_sd <= 1e-12:
                        raise ValueError("Log word count is constant for this feature")
                    reference_words = float(config.get("length_reference_words", 100.0))
                    reference_log = math.log1p(reference_words)
                    z_length = (log_lengths - reference_log) / log_sd
                    quadratic_center = 0.0
                    transform_metadata = {
                        "measurement": length_measurement,
                        "transform": "log1p(word_count)",
                        "mean_log1p_word_count": log_mean,
                        "sd_log1p_word_count_population": log_sd,
                        "reference_word_count": reference_words,
                        "reference_log1p_word_count": reference_log,
                        "quadratic_center_mean_z_squared": quadratic_center,
                        "reference_interpretation": (
                            "G/P/I are conditional contrasts at the preregistered physical "
                            "word-count reference where z(log length)=0"
                        ),
                    }
                    length_covariates = np.column_stack(
                        [z_length, z_length**2 - quadratic_center]
                    )
                    variant_results["length_adjusted"] = analyze_outcome(
                        candidate["rows"],
                        candidate["values"],
                        weighting="sample",
                        alpha=config["alpha"],
                        equivalence_bound=config["equivalence_bound"],
                        clusters=_clusters(candidate["rows"], config["cluster_field"]),
                        covariates=length_covariates,
                        covariate_names=(
                            "reference_centered_scaled_log_word_count",
                            "reference_centered_scaled_log_word_count_squared",
                        ),
                    )
                    variant_results["length_adjusted"]["length_transform"] = {
                        **transform_metadata,
                        "slope_assumption": "common linear/quadratic curve across groups",
                    }
                except (ValueError, np.linalg.LinAlgError) as exc:
                    variant_errors["length_adjusted"] = str(exc)

                try:
                    if z_length is None:
                        raise ValueError(
                            "Common-slope length basis was not estimable for this feature"
                        )
                    factor_codes = np.asarray(
                        [effect_codes(str(row["group"])) for row in candidate["rows"]],
                        dtype=float,
                    )
                    generation = factor_codes[:, 0]
                    phishing = factor_codes[:, 1]
                    varying_slope_covariates = np.column_stack(
                        [
                            z_length,
                            z_length**2 - quadratic_center,
                            z_length * generation,
                            z_length * phishing,
                            z_length * generation * phishing,
                        ]
                    )
                    variant_results["length_adjusted_varying_slopes"] = analyze_outcome(
                        candidate["rows"],
                        candidate["values"],
                        weighting="sample",
                        alpha=config["alpha"],
                        equivalence_bound=config["equivalence_bound"],
                        clusters=_clusters(candidate["rows"], config["cluster_field"]),
                        covariates=varying_slope_covariates,
                        covariate_names=(
                            "reference_centered_scaled_log_word_count",
                            "reference_centered_scaled_log_word_count_squared",
                            "generation_by_reference_centered_scaled_log_word_count",
                            "phishing_by_reference_centered_scaled_log_word_count",
                            "generation_by_phishing_by_reference_centered_scaled_log_word_count",
                        ),
                    )
                    variant_results["length_adjusted_varying_slopes"][
                        "length_transform"
                    ] = {
                        **transform_metadata,
                        "slope_assumption": (
                            "generation-, phishing-, and interaction-specific linear "
                            "slopes with a common quadratic curve"
                        ),
                    }
                except (ValueError, np.linalg.LinAlgError) as exc:
                    variant_errors["length_adjusted_varying_slopes"] = str(exc)

            if "length_common_support" in variants and common_length_support is not None:
                try:
                    lower, upper = common_length_support
                    retained_pairs = [
                        (row, value)
                        for row, value in zip(candidate["rows"], candidate["values"])
                        if lower
                        <= float(word_count_by_id[str(row["sample_id"])])
                        <= upper
                    ]
                    retained_rows = [row for row, _ in retained_pairs]
                    retained_values_by_id = {
                        str(row["sample_id"]): float(value)
                        for row, value in retained_pairs
                    }
                    supported, dropped = supported_rows(
                        retained_rows, min_cell_n=config["min_cell_n"]
                    )
                    if not supported:
                        raise ValueError(
                            "No stratum retains four-cell support after common-length trimming"
                        )
                    common_result = analyze_outcome(
                        supported,
                        [retained_values_by_id[str(row["sample_id"])] for row in supported],
                        weighting="sample",
                        alpha=config["alpha"],
                        equivalence_bound=config["equivalence_bound"],
                        clusters=_clusters(supported, config["cluster_field"]),
                    )
                    common_result["common_length_support"] = {
                        "method": (
                            "intersection of observed group min/max ranges followed by "
                            "four-cell stratum support filtering; not length balancing"
                        ),
                        "lower_words": lower,
                        "upper_words": upper,
                        "retained_n": len(supported),
                        "dropped_strata": dropped,
                        "retained_word_count_by_group": {
                            group: _length_summary(
                                [
                                    float(word_count_by_id[str(row["sample_id"])])
                                    for row in supported
                                    if row["group"] == group
                                ]
                            )
                            for group in GROUPS
                        },
                    }
                    variant_results["length_common_support"] = common_result
                except (ValueError, np.linalg.LinAlgError) as exc:
                    variant_errors["length_common_support"] = str(exc)

            feature_provisional = bool(candidate["provisional"] or loaded["partial_file"])
            provisional = provisional or feature_provisional
            feature_warnings = [
                warning
                for result in variant_results.values()
                for warning in result.get("warnings", [])
            ]
            primary_diagnostics = variant_results["sample_weighted"]["diagnostics"]
            if candidate["metric_kind"] == "count_or_length_sensitive":
                feature_warnings.append(
                    "Raw count/length-sensitive metric; interpret alongside word-count and rate/common-support sensitivity analyses"
                )
            if length_requested:
                feature_warnings.append(
                    "Length variants are sensitivity estimands; length may be a mediator, so compare them with the primary total association"
                )
                feature_warnings.append(
                    "The common-support variant is observed min/max range-overlap trimming, not length-distribution balancing, and is outlier-sensitive"
                )
                feature_warnings.append(
                    "The length_adjusted model assumes a common length curve; compare length_adjusted_varying_slopes to diagnose group-specific length relationships"
                )
            for variant_name, error in variant_errors.items():
                feature_warnings.append(
                    f"Sensitivity variant {variant_name} was not estimable: {error}"
                )
            if candidate["metric_kind"] == "composition":
                feature_warnings.append(
                    "Compositional topic coordinate; analyze the topic vector jointly and do not meta-align separately fitted topics"
                )
            if primary_diagnostics["zero_fraction"] >= 0.5:
                feature_warnings.append(
                    f"Zero-inflated outcome ({primary_diagnostics['zero_fraction']:.1%} zeros); OLS/HC3 is a distributional screen"
                )
            features.append(
                {
                    "family": family,
                    "name": candidate["feature"],
                    "metric_signature": loaded["metric_signature"],
                    "metric_kind": candidate["metric_kind"],
                    "status": "provisional" if feature_provisional else "complete",
                    "completeness": candidate["completeness"],
                    "dropped_strata": candidate["dropped_strata"],
                    "variants": variant_results,
                    "variant_errors": variant_errors,
                    "stratum_effects": _stratum_effects(
                        candidate["rows"],
                        candidate["values"],
                        variant_results["sample_weighted"],
                    ),
                    "classification": None,
                    "warnings": sorted(set(feature_warnings)),
                }
            )

    _apply_fdr(
        features,
        variants,
        alpha=config["alpha"],
        minimum_effect=config["minimum_effect"],
    )
    taxonomy = Counter(feature["classification"] for feature in features)
    return {
        "schema_version": SCHEMA_VERSION,
        "analysis": {
            "implementation_version": IMPLEMENTATION_VERSION,
            "run_config_signature": _run_config_signature(config),
            "estimator_signatures": _estimator_signatures(
                config, length_measurement=length_measurement
            ),
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "core_sha256": sha256_file((Path(__file__).resolve().parent / "core.py")),
            "dataset_id": config["dataset_id"],
            "independence_group": config["independence_group"],
            "independence_group_explicit": config[
                "independence_group_explicit"
            ],
            "provisional": provisional,
            "samples_path": str(config["samples"].resolve()),
            "samples_sha256": sha256_file(config["samples"]),
            "manifest": config["manifest"],
            "input_metrics": input_metrics,
            "factor_coding": {"HW": -0.5, "MG": 0.5, "B": -0.5, "P": 0.5},
            "model": "metric ~ G + P + G:P + match_stratum fixed effects",
            "primary_variant": "sample_weighted",
            "variants": variants,
            "variant_descriptions": {
                "sample_weighted": "Primary total association; each document has equal weight",
                "equal_stratum": "Each retained stratum-by-group cell has equal total weight",
                "length_adjusted": (
                    f"Secondary conditional association at {config.get('length_reference_words', 100.0):g} "
                    "words with one common linear/quadratic log-length curve"
                ),
                "length_adjusted_varying_slopes": (
                    f"Secondary conditional association at {config.get('length_reference_words', 100.0):g} "
                    "words with generation-, phishing-, and interaction-specific linear log-length slopes"
                ),
                "length_common_support": (
                    "Secondary observed min/max range-overlap restriction; does not balance "
                    "the retained length distributions"
                ),
            },
            "length_sensitivity_requested": length_requested,
            "length_reference_words": config.get("length_reference_words", 100.0),
            "length_measurement": length_measurement,
            "covariance": "CR1" if config["cluster_field"] else "HC3",
            "cluster_field": config["cluster_field"],
            "alpha": config["alpha"],
            "equivalence_bound_standardized": config["equivalence_bound"],
            "minimum_taxonomy_effect_standardized": config["minimum_effect"],
            "fdr_scope": "within dataset, family, analysis variant, and contrast",
            "standardization": "model residual SD with exact Hedges J correction",
            "standardized_se": (
                "approximate delta method including residual-scale uncertainty; "
                "uses a residual-scale independence approximation"
            ),
            "sample_metadata": sample_metadata,
        },
        "diagnostics": {
            **diagnostics,
            "families": family_diagnostics,
            "taxonomy_counts": dict(sorted(taxonomy.items())),
            "analyzed_features": len(features),
            "skipped_features": len(skipped),
        },
        "features": features,
        "skipped": skipped,
    }


def _write_csv(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(payload: Mapping[str, Any], config: Mapping[str, Any]) -> None:
    output = Path(config["output"])
    output.mkdir(parents=True, exist_ok=True)
    plot_directory = output / "plots"
    for filename in ("signed_G_P_I_heatmap.png", "top_interaction_plots.png"):
        artifact = plot_directory / filename
        if artifact.is_file():
            artifact.unlink()
    safe_payload = json_safe(payload)
    (output / "within_effects.json").write_text(
        json.dumps(safe_payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    (output / "diagnostics.json").write_text(
        json.dumps(
            json_safe({"analysis": payload["analysis"], "diagnostics": payload["diagnostics"]}),
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )

    effect_rows = []
    cell_rows = []
    stratum_rows = []
    for feature in payload["features"]:
        for variant_name, variant in feature["variants"].items():
            for effect, result in variant["contrasts"].items():
                equivalence = result.get("equivalence", {})
                effect_rows.append(
                    {
                        "dataset_id": payload["analysis"]["dataset_id"],
                        "family": feature["family"],
                        "feature": feature["name"],
                        "metric_signature": feature["metric_signature"],
                        "metric_kind": feature["metric_kind"],
                        "status": feature["status"],
                        "classification": feature.get("variant_classifications", {}).get(
                            variant_name
                        ),
                        "classification_basis": variant_name,
                        "variant": variant_name,
                        "effect": effect,
                        "n": variant["n"],
                        "n_strata": variant["n_strata"],
                        "raw_estimate": result["raw"]["estimate"],
                        "raw_se": result["raw"]["se"],
                        "raw_ci_low": result["raw"]["ci_low"],
                        "raw_ci_high": result["raw"]["ci_high"],
                        "p": result["raw"]["p"],
                        "q": result["raw"]["q"],
                        "standardized_estimate": result["standardized"]["estimate"],
                        "standardized_se": result["standardized"]["se"],
                        "standardized_ci_low": result["standardized"]["ci_low"],
                        "standardized_ci_high": result["standardized"]["ci_high"],
                        "equivalence_bound": equivalence.get("bound"),
                        "equivalence_ci90_low": equivalence.get("ci90_low"),
                        "equivalence_ci90_high": equivalence.get("ci90_high"),
                        "p_tost": equivalence.get("p_tost"),
                        "q_tost": equivalence.get("q_tost"),
                        "equivalent": equivalence.get("equivalent"),
                    }
                )
            for group in GROUPS:
                raw = variant["raw_cell_summary"][group]
                cell_rows.append(
                    {
                        "dataset_id": payload["analysis"]["dataset_id"],
                        "family": feature["family"],
                        "feature": feature["name"],
                        "metric_signature": feature["metric_signature"],
                        "metric_kind": feature["metric_kind"],
                        "status": feature["status"],
                        "variant": variant_name,
                        "group": group,
                        "n": raw["n"],
                        "raw_mean": raw["mean"],
                        "raw_sd": raw["sd"],
                        "raw_median": raw["median"],
                        "adjusted_mean": variant["adjusted_means"][group],
                    }
                )
        for item in feature.get("stratum_effects", []):
            for effect in MAIN_EFFECTS:
                stratum_rows.append(
                    {
                        "dataset_id": payload["analysis"]["dataset_id"],
                        "family": feature["family"],
                        "feature": feature["name"],
                        "metric_signature": feature["metric_signature"],
                        "metric_kind": feature["metric_kind"],
                        "status": feature["status"],
                        "stratum": item["stratum"],
                        "effect": effect,
                        "raw_estimate": item["effects_raw"][effect],
                        "standardized_common_residual_sd": item[
                            "effects_standardized_common_residual_sd"
                        ][effect],
                        "n_HW_B": item["n_by_group"]["HW-B"],
                        "n_HW_P": item["n_by_group"]["HW-P"],
                        "n_MG_B": item["n_by_group"]["MG-B"],
                        "n_MG_P": item["n_by_group"]["MG-P"],
                        "inferential_status": item["inferential_status"],
                    }
                )
    effect_fields = list(effect_rows[0]) if effect_rows else ["dataset_id", "family", "feature"]
    cell_fields = list(cell_rows[0]) if cell_rows else ["dataset_id", "family", "feature"]
    _write_csv(output / "effects_long.csv", effect_fields, effect_rows)
    _write_csv(output / "four_cell_summary.csv", cell_fields, cell_rows)
    _write_csv(
        output / "stratum_effects.csv",
        list(stratum_rows[0])
        if stratum_rows
        else ["dataset_id", "family", "feature", "stratum", "effect"],
        stratum_rows,
    )

    skipped_rows = []
    for item in payload["skipped"]:
        flat = {
            "family": item.get("family"),
            "feature": item.get("feature"),
            "reason": item.get("reason"),
            "total_rows": item.get("total_rows"),
            "finite_scalar_rows": item.get("finite_scalar_rows"),
            "missing_or_nonfinite_rows": item.get("missing_or_nonfinite_rows"),
            "vector_or_object_rows": item.get("vector_or_object_rows"),
            "invalid_scalar_rows": item.get("invalid_scalar_rows"),
            "details": json.dumps(
                {key: value for key, value in item.items() if key not in {
                    "family", "feature", "reason", "total_rows", "finite_scalar_rows",
                    "missing_or_nonfinite_rows", "vector_or_object_rows", "invalid_scalar_rows"
                }},
                ensure_ascii=False,
                sort_keys=True,
            ),
        }
        skipped_rows.append(flat)
    _write_csv(
        output / "skipped_features.csv",
        [
            "family",
            "feature",
            "reason",
            "total_rows",
            "finite_scalar_rows",
            "missing_or_nonfinite_rows",
            "vector_or_object_rows",
            "invalid_scalar_rows",
            "details",
        ],
        skipped_rows,
    )
    (output / "report.md").write_text(_make_report(payload), encoding="utf-8")

    if config["plots"]:
        plot_within_effect_heatmap(
            payload["features"],
            plot_directory / "signed_G_P_I_heatmap.png",
            variant=payload["analysis"]["primary_variant"],
            max_features=config["max_plot_features"],
        )
        plot_top_interactions(
            payload["features"],
            plot_directory / "top_interaction_plots.png",
            variant=payload["analysis"]["primary_variant"],
            count=config["top_interactions"],
        )


def _fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "NA"
    value = float(value)
    if not math.isfinite(value):
        return "NA"
    return f"{value:.{digits}f}"


def _make_report(payload: Mapping[str, Any]) -> str:
    analysis = payload["analysis"]
    diagnostics = payload["diagnostics"]
    provisional = analysis["provisional"]
    lines = [
        f"# G/P/I effect analysis: {analysis['dataset_id']}",
        "",
    ]
    if provisional:
        lines += [
            "> **PROVISIONAL:** Partial inputs or feature-level complete cases were allowed. "
            "Do not treat this as the final confirmatory inventory.",
            "",
        ]
    lines += [
        "## Design",
        "",
        f"- Samples: **{diagnostics['sample_count']}**.",
        f"- Strata: **{diagnostics['stratum_count']}**.",
        f"- Analyzed features: **{diagnostics['analyzed_features']}**; skipped: **{diagnostics['skipped_features']}**.",
        f"- Model: `{analysis['model']}`.",
        f"- Covariance: **{analysis['covariance']}**; FDR alpha: **{analysis['alpha']}**.",
        f"- Standardized interaction equivalence bound: **+/-{analysis['equivalence_bound_standardized']}**.",
        "- Standardized confidence intervals use a documented delta-method approximation; cluster/bootstrap resampling of the true independent unit is preferable for confirmatory repeated-unit designs.",
        "- `G` is the marginal machine-minus-human contrast; `P` is the marginal phishing-minus-benign contrast; `I` is the difference-in-differences.",
        "- A nonsignificant interaction is not called stable; stability requires the FDR-adjusted TOST result inside the declared bound.",
        "",
        "## Data diagnostics",
        "",
    ]
    for warning in diagnostics.get("warnings", []):
        lines.append(f"- **Warning:** {warning}")
    lines += ["", "### Group counts", "", "| Group | n |", "|---|---:|"]
    for group in GROUPS:
        lines.append(f"| {group} | {diagnostics['group_counts'][group]} |")
    if diagnostics.get("word_count_by_group"):
        lines += [
            "",
            "### Word-count structure",
            "",
            "| Group | n | Mean | Median | Min | Max |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        for group in GROUPS:
            item = diagnostics["word_count_by_group"].get(group)
            if item:
                lines.append(
                    f"| {group} | {item['n']} | {_fmt(item['mean'], 2)} | "
                    f"{_fmt(item['median'], 2)} | {_fmt(item['minimum'], 0)} | {_fmt(item['maximum'], 0)} |"
                )
        length_effects = diagnostics.get("word_count_factorial_effects", {}).get(
            analysis["primary_variant"], {}
        )
        if length_effects:
            lines += [
                "",
                "Stratum-adjusted word-count effects (raw words; diagnostic, not FDR tested):",
                "",
                "| G | P | I |",
                "|---:|---:|---:|",
                "| "
                + " | ".join(
                    _fmt(length_effects["contrasts"][effect]["raw"]["estimate"], 2)
                    for effect in ("G", "P", "I")
                )
                + " |",
            ]
        length_sensitivity = diagnostics.get("length_sensitivity", {})
        if length_sensitivity.get("requested"):
            available_variants = [
                item
                for item in analysis["variants"]
                if item.startswith("length_")
            ]
            lines += [
                "",
                "Length sensitivity was explicitly requested. Available variants: "
                + (", ".join(f"`{item}`" for item in available_variants) or "none")
                + ". These are sensitivity estimands because length may lie on the causal pathway.",
            ]

    lines += ["", "## Feature taxonomy", "", "| Classification | Count |", "|---|---:|"]
    for name, count in diagnostics["taxonomy_counts"].items():
        lines.append(f"| `{name}` | {count} |")

    variant = analysis["primary_variant"]
    for effect, title in (("G", "Generation"), ("P", "Phishing"), ("I", "Interaction")):
        ranked = []
        for feature in payload["features"]:
            result = feature["variants"][variant]["contrasts"][effect]
            estimate = result["standardized"]["estimate"]
            if estimate is not None:
                ranked.append((abs(float(estimate)), feature, result))
        lines += [
            "",
            f"## Largest standardized {title} effects",
            "",
            "| Family | Feature | Effect | 95% CI | q | Classification |",
            "|---|---|---:|---:|---:|---|",
        ]
        for _, feature, result in sorted(ranked, reverse=True, key=lambda item: item[0])[:20]:
            standardized = result["standardized"]
            lines.append(
                f"| {feature['family']} | `{feature['name']}` | {_fmt(standardized['estimate'])} | "
                f"[{_fmt(standardized['ci_low'])}, {_fmt(standardized['ci_high'])}] | "
                f"{_fmt(result['raw']['q'])} | `{feature['classification']}` |"
            )
    lines += [
        "",
        "## Interpretation boundary",
        "",
        "These are within-dataset adjusted associations. `stable_generation` and related labels mean stable across phishing intent **within this dataset**. Cross-dataset or cross-LLM transferability requires independent datasets analyzed by `meta_analyze.py`.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = build_parser()
    try:
        config = resolve_config(parser.parse_args())
        payload = run_analysis(config)
        write_outputs(payload, config)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(f"WROTE {Path(config['output']) / 'within_effects.json'}")
    print(f"WROTE {Path(config['output']) / 'report.md'}")


if __name__ == "__main__":
    main()
