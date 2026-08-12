"""Input validation, schema adaptation, and dataset diagnostics."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

from .core import GROUPS, factorial_support, is_finite_scalar, supported_rows


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _unique_by_id(rows: Sequence[Mapping[str, Any]], source: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for position, raw in enumerate(rows):
        if not isinstance(raw, Mapping):
            raise ValueError(f"{source}: row {position} is not an object")
        sample_id = raw.get("sample_id")
        if not isinstance(sample_id, str) or not sample_id:
            raise ValueError(f"{source}: row {position} has no nonempty sample_id")
        if sample_id in indexed:
            raise ValueError(f"{source}: duplicate sample_id {sample_id!r}")
        indexed[sample_id] = dict(raw)
    return indexed


def load_samples(path: Path, min_cell_n: int = 1) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load and validate the dataset containing the four factorial groups."""

    payload = read_json(path)
    if not isinstance(payload, Mapping) or not isinstance(payload.get("samples"), list):
        raise ValueError(f"{path}: expected an object containing a samples list")
    indexed = _unique_by_id(payload["samples"], str(path))
    rows = list(indexed.values())
    if not rows:
        raise ValueError(f"{path}: samples list is empty")

    groups = Counter(str(row.get("group")) for row in rows)
    unknown = sorted(set(groups) - set(GROUPS))
    missing = sorted(set(GROUPS) - set(groups))
    if unknown or missing:
        raise ValueError(
            f"{path}: factorial groups invalid; unknown={unknown}, missing={missing}"
        )

    has_stratum = ["match_stratum" in row and row["match_stratum"] is not None for row in rows]
    if any(has_stratum) and not all(has_stratum):
        raise ValueError(f"{path}: match_stratum is present for only some samples")
    if not any(has_stratum):
        for row in rows:
            row["match_stratum"] = "__all__"
    else:
        for row in rows:
            row["match_stratum"] = str(row["match_stratum"])

    problems, table = factorial_support(rows, min_cell_n=min_cell_n)
    if problems:
        preview = "; ".join(problems[:5])
        suffix = f"; plus {len(problems) - 5} more" if len(problems) > 5 else ""
        raise ValueError(
            f"{path}: dataset lacks four-cell support within strata: {preview}{suffix}"
        )
    metadata = {key: value for key, value in payload.items() if key != "samples"}
    metadata["factorial_cell_counts"] = table
    return rows, metadata


def _normalise_signature_value(value: Any, key: str | None = None) -> Any:
    """Remove dataset-specific paths/counts while retaining extractor settings."""

    excluded = {
        "dataset",
        "sample_count",
        "n_samples",
        "started_utc",
        "finished_utc",
        "device",
    }
    if key in excluded:
        return None
    if isinstance(value, Mapping):
        return {
            str(item_key): normalized
            for item_key, item_value in sorted(value.items())
            if (normalized := _normalise_signature_value(item_value, str(item_key)))
            is not None
        }
    if isinstance(value, list):
        return [_normalise_signature_value(item) for item in value]
    if isinstance(value, str):
        # Model and source paths are machine-specific, but their final artifact
        # name normally identifies the measurement configuration.
        if "\\" in value or "/" in value:
            return Path(value.replace("\\", "/")).name
    return value


def automatic_metric_signature(family: str, metadata: Mapping[str, Any]) -> str:
    normalized = {
        "family": family,
        "metadata": _normalise_signature_value(dict(metadata)),
    }
    encoded = json.dumps(normalized, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return "auto:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]


def load_metric_family(
    path: Path,
    family: str,
    samples: Sequence[Mapping[str, Any]],
    allow_partial: bool,
    signature_override: str | None = None,
) -> dict[str, Any]:
    """Load one calculation output and align it to samples by sample_id."""

    payload = read_json(path)
    if not isinstance(payload, Mapping) or not isinstance(payload.get("results"), list):
        raise ValueError(f"{path}: expected an object containing a results list")
    metadata = payload.get("metadata", {})
    if not isinstance(metadata, Mapping):
        metadata = {"raw_metadata": metadata}
    metric_index = _unique_by_id(payload["results"], str(path))
    sample_index = {str(row["sample_id"]): row for row in samples}
    extra = sorted(set(metric_index) - set(sample_index))
    missing = sorted(set(sample_index) - set(metric_index))
    if extra:
        raise ValueError(f"{path}: contains {len(extra)} IDs absent from the samples file")

    partial_reasons: list[str] = []
    if path.name.endswith(".partial.json"):
        partial_reasons.append("filename ends in .partial.json")
    explicit_status = payload.get("status", metadata.get("status"))
    if explicit_status is not None:
        if not isinstance(explicit_status, str) or not explicit_status.strip():
            raise ValueError(f"{path}: status must be a nonempty string when present")
        normalized_status = explicit_status.strip().lower()
        if normalized_status not in {"complete", "completed", "final", "success", "succeeded"}:
            partial_reasons.append(f"explicit status is {explicit_status!r}")
    if payload.get("partial") is True or metadata.get("partial") is True:
        partial_reasons.append("explicit partial flag is true")
    if metadata.get("resumable") is True and not metadata.get("finished_utc"):
        partial_reasons.append("resumable checkpoint has no finished_utc marker")
    if missing:
        partial_reasons.append(f"missing {len(missing)} sample rows")

    observed_features: set[str] = set()
    rows_with_errors = 0
    for sample_id, row in metric_index.items():
        metrics = row.get("metrics", {})
        errors = row.get("errors", {})
        if not isinstance(metrics, Mapping) or not isinstance(errors, Mapping):
            raise ValueError(f"{path}: invalid metrics/errors object for {sample_id}")
        observed_features.update(str(key) for key in metrics)
        rows_with_errors += bool(errors)
    if rows_with_errors:
        partial_reasons.append(f"{rows_with_errors} result rows contain extractor errors")

    expected_inventory = payload.get(
        "expected_features", metadata.get("expected_features")
    )
    missing_inventory: list[str] = []
    incomplete_expected_features: dict[str, int] = {}
    if expected_inventory is not None:
        if not isinstance(expected_inventory, list) or not all(
            isinstance(item, str) and item for item in expected_inventory
        ):
            raise ValueError(f"{path}: expected_features must be a list of nonempty strings")
        missing_inventory = sorted(set(expected_inventory) - observed_features)
        if missing_inventory:
            partial_reasons.append(
                f"expected feature inventory is missing {len(missing_inventory)} features"
            )
        incomplete_expected_features = {
            feature: sum(
                feature not in row.get("metrics", {})
                or row.get("metrics", {}).get(feature) is None
                for row in metric_index.values()
            )
            for feature in expected_inventory
        }
        incomplete_expected_features = {
            feature: count
            for feature, count in incomplete_expected_features.items()
            if count
        }
        if incomplete_expected_features:
            partial_reasons.append(
                f"{len(incomplete_expected_features)} expected features are incomplete across result rows"
            )
    incomplete_observed_features = {
        feature: sum(
            feature not in row.get("metrics", {})
            or row.get("metrics", {}).get(feature) is None
            for row in metric_index.values()
        )
        for feature in observed_features
    }
    incomplete_observed_features = {
        feature: count
        for feature, count in incomplete_observed_features.items()
        if count
    }
    if incomplete_observed_features:
        partial_reasons.append(
            f"{len(incomplete_observed_features)} observed features are absent/null in some result rows"
        )
    expected_count = metadata.get("feature_count", payload.get("feature_count"))
    if expected_count is not None:
        if isinstance(expected_count, bool) or not isinstance(expected_count, int):
            raise ValueError(f"{path}: feature_count must be an integer when present")
        if expected_count != len(observed_features):
            partial_reasons.append(
                f"feature_count={expected_count} but observed {len(observed_features)} feature names"
            )

    partial_reasons = list(dict.fromkeys(partial_reasons))
    detected_partial = bool(partial_reasons)
    if detected_partial and not allow_partial:
        raise ValueError(
            f"{path}: incomplete/provisional metric input requires --allow-partial: "
            + "; ".join(partial_reasons)
        )

    aligned = []
    conflicts = []
    for sample in samples:
        sample_id = str(sample["sample_id"])
        metric_row = metric_index.get(sample_id, {})
        for field in ("group", "match_stratum"):
            if field in metric_row and metric_row[field] is not None:
                if str(metric_row[field]) != str(sample[field]):
                    conflicts.append(
                        f"{sample_id}:{field}={metric_row[field]!r} vs {sample[field]!r}"
                    )
        metrics = metric_row.get("metrics", {})
        errors = metric_row.get("errors", {})
        aligned.append(
            {
                **dict(sample),
                "metrics": dict(metrics),
                "metric_errors": dict(errors),
            }
        )
    if conflicts:
        raise ValueError(f"{path}: core-label conflicts: {'; '.join(conflicts[:5])}")

    signature = signature_override or automatic_metric_signature(family, metadata)
    return {
        "family": family,
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "partial_file": detected_partial,
        "partial_filename": path.name.endswith(".partial.json"),
        "partial_reasons": partial_reasons,
        "explicit_status": explicit_status,
        "missing_sample_rows": len(missing),
        "observed_feature_count": len(observed_features),
        "expected_feature_count": expected_count,
        "missing_expected_features": missing_inventory,
        "incomplete_expected_features": incomplete_expected_features,
        "incomplete_observed_features": incomplete_observed_features,
        "rows_with_errors": rows_with_errors,
        "metadata": dict(metadata),
        "metric_signature": signature,
        "rows": aligned,
    }


def metric_kind(name: str) -> str:
    lowered = name.lower()
    if lowered.startswith("lda_topic_") or lowered.startswith("lda_assignment_"):
        return "composition"
    if any(token in lowered for token in ("ratio", "density", "percentage", "fraction", "rate")):
        return "rate_or_proportion"
    if any(
        token in lowered
        for token in (
            "count",
            "total_words",
            "hapax",
            "character_",
            "syntactic_",
            "pos_nouns",
            "pos_verbs",
            "pos_adjectives",
            "pos_adverbs",
        )
    ):
        return "count_or_length_sensitive"
    return "continuous_score"


def feature_candidates(
    family_rows: Sequence[Mapping[str, Any]],
    allow_partial: bool,
    min_cell_n: int,
    near_constant_tolerance: float = 1e-12,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Separate analyzable scalar features from conservative skip records."""

    keys = sorted(set().union(*(row.get("metrics", {}) for row in family_rows)))
    candidates: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    total = len(family_rows)
    for key in keys:
        present_values = [row.get("metrics", {}).get(key) for row in family_rows if key in row.get("metrics", {})]
        vector_count = sum(isinstance(value, (list, dict, tuple)) for value in present_values)
        invalid_count = sum(
            value is not None
            and not isinstance(value, (list, dict, tuple))
            and not is_finite_scalar(value)
            for value in present_values
        )
        finite_rows = [
            row
            for row in family_rows
            if is_finite_scalar(row.get("metrics", {}).get(key))
        ]
        missing_count = total - len(finite_rows)
        completeness = {
            "total_rows": total,
            "finite_scalar_rows": len(finite_rows),
            "missing_or_nonfinite_rows": missing_count,
            "vector_or_object_rows": vector_count,
            "invalid_scalar_rows": invalid_count,
            "finite_by_group": {
                group: sum(row["group"] == group for row in finite_rows) for group in GROUPS
            },
        }
        if vector_count:
            skipped.append({"feature": key, "reason": "non_scalar_vector_or_object", **completeness})
            continue
        if invalid_count:
            skipped.append({"feature": key, "reason": "invalid_nonnumeric_or_nonfinite_value", **completeness})
            continue
        if missing_count and not allow_partial:
            skipped.append({"feature": key, "reason": "incomplete_feature", **completeness})
            continue
        analysis_rows = finite_rows
        dropped_strata: list[str] = []
        if missing_count:
            analysis_rows, dropped_strata = supported_rows(
                analysis_rows, min_cell_n=min_cell_n
            )
        problems, support = factorial_support(analysis_rows, min_cell_n=min_cell_n)
        if problems or not analysis_rows:
            skipped.append(
                {
                    "feature": key,
                    "reason": "insufficient_four_cell_support",
                    "dropped_strata": dropped_strata,
                    "support": support,
                    **completeness,
                }
            )
            continue
        values = [float(row["metrics"][key]) for row in analysis_rows]
        if max(values) - min(values) <= near_constant_tolerance:
            skipped.append({"feature": key, "reason": "constant_or_near_constant", **completeness})
            continue
        candidates.append(
            {
                "feature": key,
                "rows": analysis_rows,
                "values": values,
                "dropped_strata": dropped_strata,
                "completeness": completeness,
                "metric_kind": metric_kind(key),
                "provisional": bool(missing_count or dropped_strata),
            }
        )
    return candidates, skipped


def dataset_diagnostics(samples: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    groups = Counter(str(row["group"]) for row in samples)
    strata = defaultdict(Counter)
    for row in samples:
        strata[str(row.get("match_stratum", "__all__"))][str(row["group"])] += 1

    source_generation = defaultdict(Counter)
    for row in samples:
        source = str(row.get("source", "__missing__"))
        generation = "MG" if str(row["group"]).startswith("MG-") else "HW"
        source_generation[source][generation] += 1
    source_table = {
        source: {kind: int(counts.get(kind, 0)) for kind in ("HW", "MG")}
        for source, counts in sorted(source_generation.items())
    }
    generation_source_confounded = bool(
        len(source_table) > 1
        and all(not (counts["HW"] and counts["MG"]) for counts in source_table.values())
    )

    lengths_by_group: dict[str, list[float]] = {group: [] for group in GROUPS}
    for row in samples:
        value = row.get("word_count")
        if not is_finite_scalar(value) and isinstance(row.get("text"), str):
            value = len(re.findall(r"\b\w+\b", row["text"], flags=re.UNICODE))
        if is_finite_scalar(value):
            lengths_by_group[str(row["group"])].append(float(value))
    length_summary = {}
    for group, values in lengths_by_group.items():
        if values:
            ordered = sorted(values)
            midpoint = len(ordered) // 2
            median = (
                ordered[midpoint]
                if len(ordered) % 2
                else (ordered[midpoint - 1] + ordered[midpoint]) / 2.0
            )
            length_summary[group] = {
                "n": len(ordered),
                "mean": sum(ordered) / len(ordered),
                "median": float(median),
                "minimum": ordered[0],
                "maximum": ordered[-1],
            }

    text_clusters: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in samples:
        if isinstance(row.get("text"), str):
            digest = hashlib.sha256(row["text"].encode("utf-8")).hexdigest()
            text_clusters[digest].append(row)
    duplicate_clusters = [cluster for cluster in text_clusters.values() if len(cluster) > 1]
    duplicates_by_group = Counter(
        str(row["group"]) for cluster in duplicate_clusters for row in cluster
    )

    warnings = []
    if generation_source_confounded:
        warnings.append(
            "Generation is perfectly confounded with source provenance; G is a corpus-associated effect"
        )
    if duplicate_clusters:
        warnings.append(
            f"Found {len(duplicate_clusters)} exact-text duplicate clusters affecting "
            f"{sum(len(cluster) for cluster in duplicate_clusters)} rows"
        )
    if length_summary:
        means = [summary["mean"] for summary in length_summary.values()]
        if min(means) > 0 and max(means) / min(means) >= 1.25:
            warnings.append(
                "Word-length distributions differ materially across groups; run a declared length sensitivity analysis"
            )
    sparse_strata = [
        stratum
        for stratum, counts in strata.items()
        if min(counts.get(group, 0) for group in GROUPS) < 2
    ]
    if sparse_strata:
        warnings.append(
            f"{len(sparse_strata)} strata have fewer than two observations in at least one cell; "
            "retain only as sparse fixed-effect adjustment and inspect stricter sensitivity results"
        )

    return {
        "sample_count": len(samples),
        "group_counts": {group: int(groups.get(group, 0)) for group in GROUPS},
        "stratum_count": len(strata),
        "sparse_strata_below_two_per_cell": sorted(sparse_strata),
        "stratum_cell_counts": {
            stratum: {group: int(counts.get(group, 0)) for group in GROUPS}
            for stratum, counts in sorted(strata.items())
        },
        "source_by_generation": source_table,
        "generation_source_confounded": generation_source_confounded,
        "word_count_by_group": length_summary,
        "exact_text_duplicate_clusters": len(duplicate_clusters),
        "rows_in_exact_text_duplicate_clusters": sum(len(cluster) for cluster in duplicate_clusters),
        "duplicate_rows_by_group": {
            group: int(duplicates_by_group.get(group, 0)) for group in GROUPS
        },
        "sample_ids": sorted(str(row["sample_id"]) for row in samples),
        "warnings": warnings,
    }
