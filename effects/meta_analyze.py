#!/usr/bin/env python
"""Compare standardized G/P/I profiles across independent datasets.

Inputs are ``within_effects.json`` files produced by ``analyze_within.py``.
The default random-effects estimator is Paule-Mandel with modified
Hartung-Knapp inference. Prediction intervals are emitted when at least three
independent datasets contribute to a feature/effect.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
from scipy.stats import spearmanr

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from effects.core import (  # noqa: E402
    benjamini_hochberg,
    json_safe,
    random_effects_summary,
)
from effects.io_utils import read_json, sha256_file  # noqa: E402
from effects.plotting import (  # noqa: E402
    plot_dataset_feature_heatmap,
    plot_square_matrix,
)


SCHEMA_VERSION = "ephishgen.effects.meta.v2"
WITHIN_SCHEMA = "ephishgen.effects.within.v2"
IMPLEMENTATION_VERSION = "1.1.0"
EFFECTS = ("G", "P", "I")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Random-effects pooling, direction consistency, heterogeneity, prediction "
            "intervals, and dataset-profile comparisons for within_effects.json files."
        )
    )
    parser.add_argument("inputs", nargs="*", type=Path, help="within_effects.json files")
    parser.add_argument("--manifest", type=Path, help="JSON manifest listing inputs/output")
    parser.add_argument("--output", type=Path, help="Output directory")
    parser.add_argument("--variant", help="Within-dataset variant (default sample_weighted)")
    parser.add_argument("--alpha", type=float, help="Inference/FDR alpha (default 0.05)")
    parser.add_argument(
        "--equivalence-bound", type=float, help="Standardized +/- interaction SESOI (default 0.2)"
    )
    parser.add_argument(
        "--minimum-effect", type=float, help="Minimum pooled standardized effect (default 0.2)"
    )
    parser.add_argument(
        "--minimum-direction-consistency",
        type=float,
        help="Minimum dominant-sign proportion (default 0.8)",
    )
    parser.add_argument(
        "--neutral-bound",
        type=float,
        help="Effects within +/- this value are neutral for sign consistency (default 0)",
    )
    parser.add_argument(
        "--allow-dependent",
        action="store_true",
        default=None,
        help="Allow overlapping/same-cohort inputs (robustness comparison, not valid meta-analysis)",
    )
    parser.add_argument(
        "--allow-provisional",
        action="store_true",
        default=None,
        help="Include within analyses marked provisional",
    )
    parser.add_argument(
        "--include-lda",
        action="store_true",
        default=None,
        help="Include LDA coordinates (only valid with a shared frozen aligned topic model)",
    )
    parser.add_argument("--no-plots", action="store_true", default=None)
    parser.add_argument("--max-plot-features", type=int, help="Heatmap column limit (default 50)")
    return parser


def _resolve_path(value: str | Path | None, base: Path) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def resolve_config(args: argparse.Namespace) -> dict[str, Any]:
    manifest: dict[str, Any] = {}
    base = Path.cwd()
    if args.manifest:
        manifest_path = args.manifest.resolve()
        manifest = read_json(manifest_path)
        if not isinstance(manifest, Mapping):
            raise ValueError("Meta manifest must be a JSON object")
        manifest = dict(manifest)
        allowed_manifest_fields = {
            "inputs",
            "output",
            "variant",
            "alpha",
            "equivalence_bound",
            "minimum_effect",
            "minimum_direction_consistency",
            "neutral_bound",
            "allow_dependent",
            "allow_provisional",
            "include_lda",
            "no_plots",
            "max_plot_features",
        }
        unknown_fields = sorted(set(manifest) - allowed_manifest_fields)
        if unknown_fields:
            raise ValueError(
                "Unknown meta-manifest fields: " + ", ".join(unknown_fields)
            )
        base = manifest_path.parent
    inputs = [path.resolve() for path in args.inputs]
    if not inputs:
        raw_inputs = manifest.get("inputs", [])
        if not isinstance(raw_inputs, list):
            raise ValueError("Meta manifest inputs must be a list")
        inputs = [_resolve_path(item, base) for item in raw_inputs]
    output = args.output.resolve() if args.output else _resolve_path(manifest.get("output"), base)
    if not inputs or output is None:
        raise ValueError("At least one input and an output directory are required")

    def setting(name: str, cli_value: Any, default: Any) -> Any:
        return cli_value if cli_value is not None else manifest.get(name, default)

    def boolean_setting(name: str, cli_value: Any, default: bool) -> bool:
        value = setting(name, cli_value, default)
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be a JSON boolean, not {value!r}")
        return value

    config = {
        "inputs": inputs,
        "output": output,
        "variant": str(setting("variant", args.variant, "sample_weighted")),
        "alpha": float(setting("alpha", args.alpha, 0.05)),
        "equivalence_bound": float(
            setting("equivalence_bound", args.equivalence_bound, 0.2)
        ),
        "minimum_effect": float(setting("minimum_effect", args.minimum_effect, 0.2)),
        "minimum_direction_consistency": float(
            setting(
                "minimum_direction_consistency",
                args.minimum_direction_consistency,
                0.8,
            )
        ),
        "neutral_bound": float(setting("neutral_bound", args.neutral_bound, 0.0)),
        "allow_dependent": boolean_setting(
            "allow_dependent", args.allow_dependent, False
        ),
        "allow_provisional": boolean_setting(
            "allow_provisional", args.allow_provisional, False
        ),
        "include_lda": boolean_setting("include_lda", args.include_lda, False),
        "plots": not boolean_setting("no_plots", args.no_plots, False),
        "max_plot_features": int(
            setting("max_plot_features", args.max_plot_features, 50)
        ),
        "manifest": str(args.manifest.resolve()) if args.manifest else None,
    }
    numeric_settings = {
        "alpha": config["alpha"],
        "equivalence_bound": config["equivalence_bound"],
        "minimum_effect": config["minimum_effect"],
        "minimum_direction_consistency": config["minimum_direction_consistency"],
        "neutral_bound": config["neutral_bound"],
    }
    if not all(math.isfinite(float(value)) for value in numeric_settings.values()):
        raise ValueError("All numeric meta-analysis settings must be finite")
    if not (0 < config["alpha"] < 0.5):
        raise ValueError("alpha must be between 0 and 0.5")
    if config["equivalence_bound"] <= 0 or config["minimum_effect"] < 0:
        raise ValueError("Effect thresholds must be positive")
    if not (0.5 <= config["minimum_direction_consistency"] <= 1.0):
        raise ValueError("minimum-direction-consistency must be in [0.5, 1]")
    if config["neutral_bound"] < 0:
        raise ValueError("neutral-bound must be nonnegative")
    if config["max_plot_features"] < 1:
        raise ValueError("max-plot-features must be at least 1")
    if config["variant"] == "length_common_support":
        raise ValueError(
            "length_common_support is a dataset-specific observed-range restriction and "
            "is intentionally within-dataset only; meta-analyze sample_weighted, "
            "equal_stratum, or a fixed-reference length-adjusted variant instead"
        )
    return config


def load_within_inputs(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    loaded = []
    dataset_ids = set()
    for path in config["inputs"]:
        payload = read_json(path)
        if not isinstance(payload, Mapping) or payload.get("schema_version") != WITHIN_SCHEMA:
            raise ValueError(f"{path}: expected schema {WITHIN_SCHEMA}; rerun analyze_within.py")
        analysis = payload.get("analysis", {})
        dataset_id = str(analysis.get("dataset_id", ""))
        if not dataset_id or dataset_id in dataset_ids:
            raise ValueError(f"{path}: missing or duplicate dataset_id {dataset_id!r}")
        dataset_ids.add(dataset_id)
        if analysis.get("provisional") and not config["allow_provisional"]:
            raise ValueError(
                f"{path}: analysis is provisional; pass --allow-provisional only for exploratory comparison"
            )
        if config["variant"] not in analysis.get("variants", []):
            raise ValueError(
                f"{path}: variant {config['variant']!r} is unavailable; "
                f"found {analysis.get('variants', [])}"
            )
        loaded.append(
            {
                "path": str(path.resolve()),
                "sha256": sha256_file(path),
                "dataset_id": dataset_id,
                "independence_group": str(
                    analysis.get("independence_group") or dataset_id
                ),
                "independence_group_explicit": bool(
                    analysis.get("independence_group_explicit", False)
                ),
                "provisional": bool(analysis.get("provisional")),
                "standardization_method": str(
                    analysis.get("standardization", "unspecified")
                ),
                "standardized_se_method": str(
                    analysis.get("standardized_se", "unspecified")
                ),
                "estimator_signature": str(
                    analysis.get("estimator_signatures", {}).get(config["variant"], "")
                ),
                "implementation_version": str(
                    analysis.get("implementation_version", "unspecified")
                ),
                "sample_ids": set(payload.get("diagnostics", {}).get("sample_ids", [])),
                "payload": payload,
            }
        )
        if not loaded[-1]["estimator_signature"]:
            raise ValueError(
                f"{path}: missing estimator signature for variant {config['variant']!r}; "
                "rerun analyze_within.py"
            )

    implicit_groups = [
        source["dataset_id"]
        for source in loaded
        if not source["independence_group_explicit"]
    ]
    if implicit_groups and not config["allow_dependent"]:
        raise ValueError(
            "Meta-analysis requires an explicit independence_group in every within analysis; "
            f"missing for {implicit_groups}. Re-run those analyses with --independence-group, "
            "or use --allow-dependent only for a labelled robustness comparison."
        )

    dependence = []
    if implicit_groups:
        dependence.append(
            {
                "type": "implicit_independence_group",
                "datasets": implicit_groups,
                "reasons": [
                    "independence_group was not explicitly declared; independence cannot be verified"
                ],
            }
        )
    for left_index, left in enumerate(loaded):
        for right in loaded[left_index + 1 :]:
            reasons = []
            if left["independence_group"] == right["independence_group"]:
                reasons.append(f"same independence_group={left['independence_group']!r}")
            overlap = len(left["sample_ids"] & right["sample_ids"])
            if overlap:
                reasons.append(f"{overlap} overlapping sample IDs")
            if reasons:
                dependence.append(
                    {
                        "left": left["dataset_id"],
                        "right": right["dataset_id"],
                        "reasons": reasons,
                    }
                )
    if dependence and not config["allow_dependent"]:
        detail = "; ".join(
            f"{item['left']} vs {item['right']}: {', '.join(item['reasons'])}"
            for item in dependence[:5]
        )
        raise ValueError(
            "Inputs are not independent: " + detail + ". Use --allow-dependent only to label a robustness comparison."
        )
    for item in loaded:
        item["dependence_warnings"] = dependence
    signatures = sorted({item["estimator_signature"] for item in loaded})
    if len(signatures) > 1:
        raise ValueError(
            f"Within inputs have incompatible {config['variant']} estimator signatures: "
            + ", ".join(signatures)
            + ". Re-run that variant with the same estimator specification."
        )
    return loaded


def _extract_effects(
    inputs: Sequence[Mapping[str, Any]], config: Mapping[str, Any]
) -> tuple[dict[tuple[str, str, str, str], list[dict[str, Any]]], dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    signatures_by_name: dict[tuple[str, str], set[str]] = defaultdict(set)
    excluded = Counter()
    dataset_profiles: dict[str, dict[tuple[str, str, str, str], float]] = defaultdict(dict)
    for source in inputs:
        for feature in source["payload"].get("features", []):
            name = str(feature["name"])
            if name.startswith("lda_") and not config["include_lda"]:
                excluded["lda_requires_shared_frozen_model"] += 1
                continue
            if feature.get("status") == "provisional" and not config["allow_provisional"]:
                excluded["provisional_feature"] += 1
                continue
            family = str(feature["family"])
            signature = str(feature.get("metric_signature", "UNSPECIFIED"))
            if name.startswith("lda_") and signature.startswith("auto:"):
                excluded["lda_requires_explicit_shared_model_signature"] += 1
                continue
            signatures_by_name[(family, name)].add(signature)
            variant = feature.get("variants", {}).get(config["variant"], {})
            for effect in EFFECTS:
                standardized = (
                    variant.get("contrasts", {})
                    .get(effect, {})
                    .get("standardized", {})
                )
                estimate, standard_error = standardized.get("estimate"), standardized.get("se")
                if estimate is None or standard_error is None:
                    excluded["missing_standardized_effect_or_se"] += 1
                    continue
                estimate, standard_error = float(estimate), float(standard_error)
                if not math.isfinite(estimate) or not math.isfinite(standard_error) or standard_error <= 0:
                    excluded["invalid_standardized_effect_or_se"] += 1
                    continue
                key = (family, name, signature, effect)
                item = {
                    "dataset_id": source["dataset_id"],
                    "estimate": estimate,
                    "se": standard_error,
                    "status": feature.get("status", "unknown"),
                    "estimator_signature": source["estimator_signature"],
                    "variant_metadata": {
                        key: variant[key]
                        for key in (
                            "weighting",
                            "additional_covariates",
                            "length_transform",
                            "common_length_support",
                        )
                        if key in variant
                    },
                }
                grouped[key].append(item)
                dataset_profiles[source["dataset_id"]][key] = estimate
    signature_splits = [
        {"family": family, "feature": name, "signatures": sorted(signatures)}
        for (family, name), signatures in sorted(signatures_by_name.items())
        if len(signatures) > 1
    ]
    diagnostics = {
        "excluded": dict(excluded),
        "measurement_signature_splits": signature_splits,
        "dataset_profiles": dataset_profiles,
    }
    return grouped, diagnostics


def _apply_meta_fdr(rows: list[dict[str, Any]], alpha: float) -> None:
    scopes: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        scopes[(row["family"], row["effect"])].append(row)
    for scoped in scopes.values():
        for row, q_value in zip(
            scoped, benjamini_hochberg([row["summary"]["p"] for row in scoped])
        ):
            row["summary"]["q"] = q_value
        for row, q_value in zip(
            scoped,
            benjamini_hochberg(
                [row["summary"]["equivalence"]["p_tost"] for row in scoped]
            ),
        ):
            equivalence = row["summary"]["equivalence"]
            equivalence["q_tost"] = q_value
            equivalence["equivalent_unadjusted"] = equivalence["equivalent"]
            equivalence["equivalent"] = bool(q_value is not None and q_value < alpha)


def _cross_dataset_taxonomy(
    meta_rows: Sequence[Mapping[str, Any]],
    config: Mapping[str, Any],
    robustness_comparison_only: bool,
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in meta_rows:
        grouped[(row["family"], row["feature"], row["metric_signature"])][row["effect"]] = row
    output = []
    for (family, feature, signature), effects in sorted(grouped.items()):
        if not all(effect in effects for effect in EFFECTS):
            role = "incomplete_effect_profile"
        else:
            generation, phishing, interaction = (
                effects[effect]["summary"] for effect in EFFECTS
            )

            def supported(summary: Mapping[str, Any]) -> bool:
                return bool(
                    summary.get("q") is not None
                    and summary["q"] < config["alpha"]
                    and abs(summary["pooled"]) >= config["minimum_effect"]
                    and summary.get("sign_consistency") is not None
                    and summary["sign_consistency"]
                    >= config["minimum_direction_consistency"]
                )

            pooled_interaction_supported = bool(
                interaction.get("q") is not None
                and interaction["q"] < config["alpha"]
                and abs(interaction["pooled"]) >= config["minimum_effect"]
            )
            interaction_direction_supported = supported(interaction)
            interaction_equivalent = bool(
                interaction["equivalence"].get("equivalent")
            )
            prediction_equivalent = bool(
                interaction["equivalence"].get("prediction_interval_inside_bounds")
            )
            minimum_k = min(summary["k"] for summary in (generation, phishing, interaction))
            if pooled_interaction_supported:
                if minimum_k < 3:
                    role = "provisional_pooled_interaction_candidate"
                elif not interaction_direction_supported:
                    role = "direction_inconsistent_interaction"
                elif not interaction.get("prediction_excludes_zero", False):
                    role = "candidate_cross_dataset_interaction_dependent"
                else:
                    role = "cross_dataset_interaction_dependent"
            elif interaction_equivalent and minimum_k >= 3 and not prediction_equivalent:
                role = "interaction_mean_small_but_heterogeneous"
            elif interaction_equivalent:
                generation_supported = supported(generation)
                phishing_supported = supported(phishing)
                if generation_supported and phishing_supported:
                    role = "stable_dual"
                elif generation_supported:
                    role = "stable_generation"
                elif phishing_supported:
                    role = "stable_phishing"
                else:
                    role = "no_supported_stable_main_effect"
                if minimum_k < 3:
                    role = "provisional_" + role
                elif (
                    generation_supported
                    and not generation.get("prediction_excludes_zero", False)
                ) or (
                    phishing_supported
                    and not phishing.get("prediction_excludes_zero", False)
                ):
                    role = "candidate_" + role
            else:
                role = "inconclusive_interaction_stability"
            if minimum_k < 3 and not role.startswith("provisional_"):
                role = "provisional_" + role
        feature_is_provisional = any(
            study.get("status") == "provisional"
            for effect_row in effects.values()
            for study in effect_row["summary"].get("studies", [])
        )
        if feature_is_provisional and not role.startswith("provisional_"):
            role = "provisional_" + role
        if robustness_comparison_only:
            role = "dependent_robustness_" + role
        output.append(
            {
                "family": family,
                "feature": feature,
                "metric_signature": signature,
                "classification": role,
            }
        )
    return output


def run_meta(config: Mapping[str, Any]) -> dict[str, Any]:
    if config["variant"] == "length_common_support":
        raise ValueError(
            "length_common_support is a dataset-specific observed-range restriction "
            "and cannot be meta-analyzed as one common estimand"
        )
    inputs = load_within_inputs(config)
    grouped, extraction_diagnostics = _extract_effects(inputs, config)
    rows = []
    for (family, feature, signature, effect), studies in sorted(grouped.items()):
        summary = random_effects_summary(
            [study["estimate"] for study in studies],
            [study["se"] for study in studies],
            [study["dataset_id"] for study in studies],
            alpha=config["alpha"],
            neutral_bound=config["neutral_bound"],
            equivalence_bound=config["equivalence_bound"],
        )
        summary["studies"] = studies
        rows.append(
            {
                "family": family,
                "feature": feature,
                "metric_signature": signature,
                "effect": effect,
                "summary": summary,
            }
        )
    _apply_meta_fdr(rows, config["alpha"])
    dependence = inputs[0]["dependence_warnings"] if inputs else []
    taxonomy = _cross_dataset_taxonomy(
        rows, config, robustness_comparison_only=bool(dependence)
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "analysis": {
            "implementation_version": IMPLEMENTATION_VERSION,
            "estimator_signatures": sorted(
                {source["estimator_signature"] for source in inputs}
            ),
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "core_sha256": sha256_file((Path(__file__).resolve().parent / "core.py")),
            "variant": config["variant"],
            "alpha": config["alpha"],
            "equivalence_bound_standardized": config["equivalence_bound"],
            "minimum_effect_standardized": config["minimum_effect"],
            "minimum_direction_consistency": config[
                "minimum_direction_consistency"
            ],
            "neutral_bound": config["neutral_bound"],
            "allow_dependent": config["allow_dependent"],
            "allow_provisional": config["allow_provisional"],
            "include_lda": config["include_lda"],
            "random_effects": "Paule-Mandel tau^2; modified Hartung-Knapp CI",
            "prediction_interval": "t(k-2) approximation for k>=3",
            "standardization_methods": sorted(
                {source["standardization_method"] for source in inputs}
            ),
            "standardized_se_methods": sorted(
                {source["standardized_se_method"] for source in inputs}
            ),
            "standardized_se_limitation": (
                "Pooled inference inherits each within-dataset standardized-SE "
                "approximation. Current within outputs use a delta method with a "
                "residual-scale independence approximation; independent-unit bootstrap "
                "SEs are preferable for confirmatory clustered analyses."
            ),
            "fdr_scope": "family and effect across compatible features",
            "manifest": config["manifest"],
            "inputs": [
                {
                    key: source[key]
                    for key in (
                        "path",
                        "sha256",
                        "dataset_id",
                        "independence_group",
                        "independence_group_explicit",
                        "provisional",
                        "standardization_method",
                        "standardized_se_method",
                        "estimator_signature",
                        "implementation_version",
                    )
                }
                for source in inputs
            ],
        },
        "diagnostics": {
            "dataset_count": len(inputs),
            "dependent_input_pairs": dependence,
            "robustness_comparison_only": bool(dependence),
            "excluded": extraction_diagnostics["excluded"],
            "measurement_signature_splits": extraction_diagnostics[
                "measurement_signature_splits"
            ],
            "meta_effect_rows": len(rows),
            "taxonomy_counts": dict(
                Counter(item["classification"] for item in taxonomy)
            ),
        },
        "effects": rows,
        "taxonomy": taxonomy,
        "_dataset_profiles": extraction_diagnostics["dataset_profiles"],
    }


def _profile_similarity(
    payload: Mapping[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, tuple[list[str], np.ndarray, np.ndarray]]]:
    profiles = payload["_dataset_profiles"]
    datasets = sorted(profiles)
    rows = []
    matrices = {}
    for effect in EFFECTS:
        correlation = np.full((len(datasets), len(datasets)), np.nan)
        agreement = np.full_like(correlation, np.nan)
        for left_index, left in enumerate(datasets):
            for right_index, right in enumerate(datasets):
                common = sorted(
                    key
                    for key in set(profiles[left]) & set(profiles[right])
                    if key[3] == effect
                )
                if not common:
                    continue
                left_values = np.asarray([profiles[left][key] for key in common])
                right_values = np.asarray([profiles[right][key] for key in common])
                if len(common) >= 2 and np.ptp(left_values) > 0 and np.ptp(right_values) > 0:
                    rho = float(spearmanr(left_values, right_values).statistic)
                else:
                    rho = 1.0 if left == right else float("nan")
                sign = float(np.mean(np.sign(left_values) == np.sign(right_values)))
                correlation[left_index, right_index] = rho
                agreement[left_index, right_index] = sign
                rows.append(
                    {
                        "effect": effect,
                        "dataset_left": left,
                        "dataset_right": right,
                        "common_features": len(common),
                        "spearman_rho": rho,
                        "sign_agreement": sign,
                    }
                )
        matrices[effect] = (datasets, correlation, agreement)
    return rows, matrices


def _write_csv(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _flatten_meta_row(row: Mapping[str, Any]) -> dict[str, Any]:
    summary = row["summary"]
    equivalence = summary["equivalence"]
    lodo = summary.get("leave_one_dataset_out") or {}
    return {
        "family": row["family"],
        "feature": row["feature"],
        "metric_signature": row["metric_signature"],
        "effect": row["effect"],
        "k": summary["k"],
        "datasets": ";".join(summary["datasets"]),
        "dataset_effects": ";".join(
            f"{study['dataset_id']}={study['estimate']:.12g}"
            for study in summary.get("studies", [])
        ),
        "pooled": summary["pooled"],
        "pooled_se": summary["pooled_se"],
        "ci_low": summary["ci_low"],
        "ci_high": summary["ci_high"],
        "p": summary["p"],
        "q": summary["q"],
        "tau2": summary["tau2"],
        "tau": summary["tau"],
        "heterogeneity_Q": summary["heterogeneity_Q"],
        "heterogeneity_Q_df": summary["heterogeneity_Q_df"],
        "heterogeneity_Q_p": summary["heterogeneity_Q_p"],
        "I2": summary["I2"],
        "prediction_low": summary["prediction_low"],
        "prediction_high": summary["prediction_high"],
        "prediction_excludes_zero": summary["prediction_excludes_zero"],
        "median": summary["median"],
        "q25": summary["q25"],
        "q75": summary["q75"],
        "n_positive": summary["n_positive"],
        "n_negative": summary["n_negative"],
        "n_neutral": summary["n_neutral"],
        "dominant_direction": summary["dominant_direction"],
        "sign_consistency": summary["sign_consistency"],
        "weighted_sign_consistency": summary["weighted_sign_consistency"],
        "p_tost": equivalence["p_tost"],
        "q_tost": equivalence["q_tost"],
        "equivalent": equivalence["equivalent"],
        "prediction_interval_inside_equivalence_bounds": equivalence[
            "prediction_interval_inside_bounds"
        ],
        "lodo_minimum": lodo.get("minimum"),
        "lodo_maximum": lodo.get("maximum"),
        "lodo_max_absolute_change": lodo.get("max_absolute_change"),
        "warnings": "; ".join(summary["warnings"]),
    }


def write_outputs(payload: dict[str, Any], config: Mapping[str, Any]) -> None:
    output = Path(config["output"])
    output.mkdir(parents=True, exist_ok=True)
    plot_directory = output / "plots"
    for effect in EFFECTS:
        for suffix in (
            "dataset_feature_heatmap.png",
            "profile_spearman.png",
            "sign_agreement.png",
        ):
            artifact = plot_directory / f"{effect}_{suffix}"
            if artifact.is_file():
                artifact.unlink()
    profile_rows, profile_matrices = _profile_similarity(payload)
    profiles = payload.pop("_dataset_profiles")
    safe = json_safe(payload)
    (output / "meta_effects.json").write_text(
        json.dumps(safe, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    flat = [_flatten_meta_row(row) for row in payload["effects"]]
    _write_csv(
        output / "meta_effects.csv",
        list(flat[0]) if flat else ["family", "feature", "effect"],
        flat,
    )
    _write_csv(
        output / "feature_taxonomy.csv",
        ["family", "feature", "metric_signature", "classification"],
        payload["taxonomy"],
    )
    _write_csv(
        output / "dataset_profile_similarity.csv",
        [
            "effect",
            "dataset_left",
            "dataset_right",
            "common_features",
            "spearman_rho",
            "sign_agreement",
        ],
        profile_rows,
    )
    (output / "report.md").write_text(_make_report(payload), encoding="utf-8")

    if config["plots"]:
        datasets = sorted(profiles)
        for effect in EFFECTS:
            keys = sorted(
                {
                    key
                    for profile in profiles.values()
                    for key in profile
                    if key[3] == effect
                }
            )
            labels = [
                f"{family}:{feature}@{signature[:8]}"
                for family, feature, signature, _ in keys
            ]
            matrix = np.asarray(
                [
                    [profiles[dataset].get(key, np.nan) for key in keys]
                    for dataset in datasets
                ],
                dtype=float,
            )
            plot_dataset_feature_heatmap(
                matrix,
                datasets,
                labels,
                effect,
                plot_directory / f"{effect}_dataset_feature_heatmap.png",
                max_features=config["max_plot_features"],
            )
            labels_matrix, correlation, agreement = profile_matrices[effect]
            plot_square_matrix(
                correlation,
                labels_matrix,
                f"{effect} effect-profile Spearman correlation",
                plot_directory / f"{effect}_profile_spearman.png",
            )
            plot_square_matrix(
                agreement,
                labels_matrix,
                f"{effect} effect sign agreement",
                plot_directory / f"{effect}_sign_agreement.png",
                vmin=0.0,
                vmax=1.0,
            )


def _fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "NA"
    value = float(value)
    return "NA" if not math.isfinite(value) else f"{value:.{digits}f}"


def _make_report(payload: Mapping[str, Any]) -> str:
    analysis, diagnostics = payload["analysis"], payload["diagnostics"]
    lines = [
        "# Cross-dataset G/P/I stability analysis",
        "",
        f"- Dataset inputs: **{diagnostics['dataset_count']}**.",
        f"- Within-dataset variant: `{analysis['variant']}`.",
        f"- Model: {analysis['random_effects']}.",
        f"- Interaction equivalence bound: **+/-{analysis['equivalence_bound_standardized']}** standardized units.",
        "- Prediction intervals, rather than pooled p-values alone, describe the plausible effect in a new dataset.",
        "",
    ]
    if diagnostics["robustness_comparison_only"]:
        lines += [
            "> **INDEPENDENCE NOT ESTABLISHED:** Inputs overlap/share a cohort, or at least "
            "one input lacks an explicit independence group. Treat this output as a robustness "
            "comparison, not a meta-analysis of independent studies.",
            "",
        ]
    lines += [
        "> **STANDARDIZED-SE LIMITATION:** "
        + analysis["standardized_se_limitation"],
        "",
    ]
    if diagnostics["dataset_count"] < 5:
        lines += [
            "> Heterogeneity and direction consistency are exploratory with fewer than about five independent datasets.",
            "",
        ]
    lines += ["## Dataset inputs", "", "| Dataset | Independence group | Provisional |", "|---|---|---:|"]
    for item in analysis["inputs"]:
        lines.append(
            f"| {item['dataset_id']} | {item['independence_group']} | {item['provisional']} |"
        )
    lines += ["", "## Cross-dataset feature taxonomy", "", "| Classification | Count |", "|---|---:|"]
    for name, count in sorted(diagnostics["taxonomy_counts"].items()):
        lines.append(f"| `{name}` | {count} |")

    for effect, title in (("G", "Generation"), ("P", "Phishing"), ("I", "Interaction")):
        rows = [row for row in payload["effects"] if row["effect"] == effect]
        rows.sort(key=lambda row: abs(row["summary"]["pooled"]), reverse=True)
        lines += [
            "",
            f"## Largest pooled {title} effects",
            "",
            "| Family | Feature | k | Pooled | 95% CI | Prediction interval | Sign consistency | I2 | q |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for row in rows[:20]:
            summary = row["summary"]
            lines.append(
                f"| {row['family']} | `{row['feature']}` | {summary['k']} | {_fmt(summary['pooled'])} | "
                f"[{_fmt(summary['ci_low'])}, {_fmt(summary['ci_high'])}] | "
                f"[{_fmt(summary['prediction_low'])}, {_fmt(summary['prediction_high'])}] | "
                f"{_fmt(summary['sign_consistency'])} | {_fmt(summary['I2'], 1)} | {_fmt(summary['q'])} |"
            )
    lines += [
        "",
        "## Interpretation boundary",
        "",
        "A pooled effect can be large while still being unsuitable for transfer when its prediction interval is wide, direction consistency is low, or leave-one-dataset-out estimates change materially. LLM transfer additionally requires multiple LLMs crossed with datasets; datasets tied one-to-one to LLMs cannot separate those sources of variation.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = build_parser()
    try:
        config = resolve_config(parser.parse_args())
        payload = run_meta(config)
        write_outputs(payload, config)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(f"WROTE {Path(config['output']) / 'meta_effects.json'}")
    print(f"WROTE {Path(config['output']) / 'report.md'}")


if __name__ == "__main__":
    main()
