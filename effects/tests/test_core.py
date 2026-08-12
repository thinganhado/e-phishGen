from __future__ import annotations

import math
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from effects.core import (
    analyze_outcome,
    benjamini_hochberg,
    classify_feature,
    equivalence_test,
    json_safe,
    random_effects_summary,
)
from effects.io_utils import feature_candidates, load_metric_family
from effects.analyze_within import build_parser as within_parser
from effects.analyze_within import resolve_config as resolve_within_config
from effects.analyze_within import run_analysis
from effects.analyze_within import write_outputs as write_within_outputs
from effects.meta_analyze import _cross_dataset_taxonomy
from effects.meta_analyze import build_parser as meta_parser
from effects.meta_analyze import resolve_config as resolve_meta_config
from effects.meta_analyze import run_meta


def synthetic_factorial_rows():
    bases = {"HW-B": 0.0, "MG-B": 2.0, "HW-P": 3.0, "MG-P": 9.0}
    rows, values = [], []
    index = 0
    for stratum, offset in (("A", 0.0), ("B", 100.0)):
        for group in ("HW-B", "HW-P", "MG-B", "MG-P"):
            for residual in (-1.0, 1.0):
                rows.append(
                    {
                        "sample_id": f"S{index}",
                        "group": group,
                        "match_stratum": stratum,
                    }
                )
                values.append(offset + bases[group] + residual)
                index += 1
    return rows, values


class WithinEffectTests(unittest.TestCase):
    def test_exact_centered_factorial_contrasts(self):
        rows, values = synthetic_factorial_rows()
        result = analyze_outcome(rows, values, equivalence_bound=0.2)
        expected = {
            "G_B": 2.0,
            "G_P": 6.0,
            "P_HW": 3.0,
            "P_MG": 7.0,
            "G": 4.0,
            "P": 5.0,
            "I": 4.0,
        }
        for name, value in expected.items():
            self.assertAlmostEqual(
                result["contrasts"][name]["raw"]["estimate"], value, places=10
            )

        contrasts = result["contrasts"]
        self.assertAlmostEqual(
            contrasts["I"]["raw"]["estimate"],
            contrasts["G_P"]["raw"]["estimate"]
            - contrasts["G_B"]["raw"]["estimate"],
        )
        self.assertAlmostEqual(
            contrasts["I"]["raw"]["estimate"],
            contrasts["P_MG"]["raw"]["estimate"]
            - contrasts["P_HW"]["raw"]["estimate"],
        )

    def test_positive_affine_rescaling_preserves_standardized_effects(self):
        rows, values = synthetic_factorial_rows()
        original = analyze_outcome(rows, values)
        transformed = analyze_outcome(rows, [3.0 * value + 7.0 for value in values])
        for effect in ("G", "P", "I"):
            self.assertAlmostEqual(
                original["contrasts"][effect]["standardized"]["estimate"],
                transformed["contrasts"][effect]["standardized"]["estimate"],
                places=10,
            )

    def test_declared_covariate_adjustment_recovers_conditional_generation_effect(self):
        rows, values, length = [], [], []
        index = 0
        centered_replicates = np.arange(20, dtype=float) - 9.5
        quadratic_mean = float(np.mean(centered_replicates**2))
        for group in ("HW-B", "HW-P", "MG-B", "MG-P"):
            generation = 0.5 if group.startswith("MG-") else -0.5
            phishing = 0.5 if group.endswith("-P") else -0.5
            for replicate in centered_replicates:
                covariate = replicate / 10.0 + 2.0 * generation + 0.5 * phishing
                residual = 0.001 * (replicate**2 - quadratic_mean)
                rows.append(
                    {
                        "sample_id": f"C{index}",
                        "group": group,
                        "match_stratum": "one",
                    }
                )
                length.append(covariate)
                values.append(2.0 * generation + 5.0 * covariate + residual)
                index += 1
        unadjusted = analyze_outcome(rows, values)
        adjusted = analyze_outcome(
            rows,
            values,
            covariates=np.asarray(length),
            covariate_names=("length",),
        )
        self.assertGreater(unadjusted["contrasts"]["G"]["raw"]["estimate"], 10.0)
        self.assertAlmostEqual(
            adjusted["contrasts"]["G"]["raw"]["estimate"], 2.0, places=10
        )

    def test_equal_stratum_and_sample_weighting_are_distinct(self):
        rows, values = [], []
        index = 0
        for stratum, replicates, generation_effect in (("A", 10, 2.0), ("B", 1, 20.0)):
            for group in ("HW-B", "HW-P", "MG-B", "MG-P"):
                is_machine = group.startswith("MG-")
                for replicate in range(replicates):
                    rows.append(
                        {
                            "sample_id": f"W{index}",
                            "group": group,
                            "match_stratum": stratum,
                        }
                    )
                    # Balanced tiny residuals retain the exact cell mean.
                    residual = (replicate - (replicates - 1) / 2.0) * 0.001
                    values.append(100.0 * (stratum == "B") + generation_effect * is_machine + residual)
                    index += 1
        sample = analyze_outcome(rows, values, weighting="sample")
        equal = analyze_outcome(rows, values, weighting="equal_stratum")
        self.assertAlmostEqual(
            sample["contrasts"]["G"]["raw"]["estimate"], 40.0 / 11.0, places=8
        )
        self.assertAlmostEqual(
            equal["contrasts"]["G"]["raw"]["estimate"], 11.0, places=8
        )

    def test_tost_requires_narrow_interval(self):
        narrow = equivalence_test(0.0, 0.03, 100, 0.2)
        wide = equivalence_test(0.0, 0.20, 20, 0.2)
        self.assertTrue(narrow["equivalent"])
        self.assertFalse(wide["equivalent"])
        self.assertGreater(wide["p_tost"], 0.05)

    def test_small_detectable_but_equivalent_interaction_can_be_stable(self):
        contrasts = {}
        for name, estimate, q_value, q_tost in (
            ("G", 0.8, 0.001, 1.0),
            ("P", 0.05, 0.5, 0.001),
            ("I", 0.10, 0.001, 0.001),
        ):
            contrasts[name] = {
                "raw": {"q": q_value},
                "standardized": {"estimate": estimate},
                "equivalence": {"q_tost": q_tost},
            }
        self.assertEqual(
            classify_feature(contrasts, alpha=0.05, minimum_effect=0.2),
            "stable_generation",
        )

    def test_bh_is_bounded_and_monotonic_by_p(self):
        p_values = [0.04, 0.001, None, 0.02, 0.9]
        adjusted = benjamini_hochberg(p_values)
        valid = sorted(
            (p, q) for p, q in zip(p_values, adjusted) if p is not None
        )
        self.assertTrue(all(0 <= q <= 1 for _, q in valid))
        self.assertEqual([q for _, q in valid], sorted(q for _, q in valid))
        self.assertIsNone(adjusted[2])


class FeatureScreenTests(unittest.TestCase):
    def _rows(self):
        rows = []
        for group in ("HW-B", "HW-P", "MG-B", "MG-P"):
            for index in range(2):
                rows.append(
                    {
                        "sample_id": f"{group}-{index}",
                        "group": group,
                        "match_stratum": "one",
                        "metrics": {
                            "good": index + (10 if group.startswith("MG-") else 0),
                            "constant": 1.0,
                            "vector": [1.0, 2.0],
                            **(
                                {"human_only": float(index)}
                                if group.startswith("HW-")
                                else {}
                            ),
                        },
                    }
                )
        return rows

    def test_vectors_constants_and_group_confounded_partial_are_skipped(self):
        candidates, skipped = feature_candidates(
            self._rows(), allow_partial=True, min_cell_n=2
        )
        self.assertEqual([item["feature"] for item in candidates], ["good"])
        reasons = {item["feature"]: item["reason"] for item in skipped}
        self.assertEqual(reasons["constant"], "constant_or_near_constant")
        self.assertEqual(reasons["vector"], "non_scalar_vector_or_object")
        self.assertEqual(reasons["human_only"], "insufficient_four_cell_support")


class MetaAnalysisTests(unittest.TestCase):
    def test_stable_and_heterogeneous_examples(self):
        stable = random_effects_summary([0.75, 0.81, 0.69, 0.88], [0.15] * 4)
        heterogeneous = random_effects_summary([0.10, 2.10, 0.31, 1.75], [0.15] * 4)
        self.assertAlmostEqual(stable["pooled"], 0.7825, places=4)
        self.assertAlmostEqual(stable["tau2"], 0.0, places=10)
        self.assertAlmostEqual(stable["I2"], 0.0, places=10)
        self.assertGreater(heterogeneous["tau2"], 0.9)
        self.assertGreater(heterogeneous["I2"], 95.0)
        self.assertLess(heterogeneous["prediction_low"], 0.0)
        self.assertGreater(heterogeneous["prediction_high"], 0.0)

    def test_json_safe_removes_nonfinite_values(self):
        converted = json_safe({"a": float("nan"), "b": np.float64(1.5)})
        self.assertIsNone(converted["a"])
        self.assertEqual(converted["b"], 1.5)


class ConfigurationAndIntegrationTests(unittest.TestCase):
    def test_cli_signature_overrides_inline_manifest_signature(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "dataset_id": "demo",
                        "samples": "samples.json",
                        "output": "output",
                        "metrics": [
                            {
                                "family": "family",
                                "path": "metrics.json",
                                "signature": "MANIFEST_SIGNATURE",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            args = within_parser().parse_args(
                [
                    "--manifest",
                    str(manifest),
                    "--signature",
                    "family=CLI_SIGNATURE",
                ]
            )
            config = resolve_within_config(args)
            self.assertEqual(config["metrics"][0][2], "CLI_SIGNATURE")

    def test_sparse_partial_feature_is_reported_not_fatal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            samples = []
            results = []
            for index, group in enumerate(("HW-B", "HW-P", "MG-B", "MG-P")):
                sample = {
                    "sample_id": f"ID{index}",
                    "group": group,
                    "match_stratum": "one",
                    "word_count": 10 + index,
                }
                samples.append(sample)
                results.append(
                    {
                        **sample,
                        "metrics": {"sparse_metric": float(index)},
                        "errors": {},
                    }
                )
            samples_path = root / "samples.json"
            metrics_path = root / "metrics.partial.json"
            samples_path.write_text(json.dumps({"samples": samples}), encoding="utf-8")
            metrics_path.write_text(
                json.dumps({"metadata": {}, "results": results}), encoding="utf-8"
            )
            config = {
                "dataset_id": "sparse",
                "samples": samples_path,
                "metrics": [("test", metrics_path, "test_signature")],
                "output": root / "output",
                "independence_group": "sparse",
                "independence_group_explicit": True,
                "allow_partial": True,
                "cluster_field": None,
                "alpha": 0.05,
                "equivalence_bound": 0.2,
                "minimum_effect": 0.2,
                "min_cell_n": 1,
                "equal_stratum": False,
                "plots": False,
                "max_plot_features": 10,
                "top_interactions": 3,
                "manifest": None,
            }
            payload = run_analysis(config)
            self.assertEqual(payload["features"], [])
            self.assertEqual(payload["skipped"][0]["reason"], "model_not_estimable")
            self.assertIn(
                "sample_weighted",
                payload["diagnostics"]["word_count_factorial_effect_errors"],
            )

    def test_length_sensitivity_and_stratum_outputs_are_materialized(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            samples, results = [], []
            shifts = {"HW-B": 0, "HW-P": 2, "MG-B": 4, "MG-P": 6}
            sample_index = 0
            for group, shift in shifts.items():
                for replicate in range(10):
                    word_count = 20 + shift + replicate
                    sample = {
                        "sample_id": f"L{sample_index}",
                        "group": group,
                        "match_stratum": "one",
                        "word_count": word_count,
                    }
                    metric = (
                        0.3 * word_count
                        + (2.0 if group.startswith("MG-") else 0.0)
                        + (replicate % 3) * 0.05
                    )
                    samples.append(sample)
                    results.append(
                        {**sample, "metrics": {"metric": metric}, "errors": {}}
                    )
                    sample_index += 1
            samples_path = root / "samples.json"
            metrics_path = root / "metrics.json"
            samples_path.write_text(json.dumps({"samples": samples}), encoding="utf-8")
            metrics_path.write_text(
                json.dumps({"metadata": {}, "results": results}), encoding="utf-8"
            )
            config = {
                "dataset_id": "length-demo",
                "samples": samples_path,
                "metrics": [("test", metrics_path, "test_signature")],
                "output": root / "output",
                "independence_group": "length-demo-source",
                "independence_group_explicit": True,
                "allow_partial": False,
                "cluster_field": None,
                "alpha": 0.05,
                "equivalence_bound": 0.2,
                "minimum_effect": 0.2,
                "min_cell_n": 1,
                "equal_stratum": True,
                "length_sensitivity": True,
                "length_reference_words": 27.0,
                "plots": False,
                "max_plot_features": 10,
                "top_interactions": 3,
                "manifest": None,
            }
            payload = run_analysis(config)
            feature = payload["features"][0]
            self.assertEqual(
                set(feature["variants"]),
                {
                    "sample_weighted",
                    "equal_stratum",
                    "length_adjusted",
                    "length_adjusted_varying_slopes",
                    "length_common_support",
                },
            )
            self.assertEqual(len(feature["stratum_effects"]), 1)
            self.assertEqual(
                set(feature["variant_classifications"]), set(feature["variants"])
            )
            self.assertEqual(
                feature["stratum_effects"][0]["inferential_status"],
                "descriptive_only",
            )
            common = feature["variants"]["length_common_support"]
            self.assertLess(common["n"], len(samples))
            support = common["common_length_support"]
            self.assertIn("not length balancing", support["method"])
            self.assertIn("retained_word_count_by_group", support)
            self.assertEqual(
                feature["variants"]["length_adjusted_varying_slopes"]
                ["length_transform"]["reference_word_count"],
                27.0,
            )
            plots = config["output"] / "plots"
            plots.mkdir(parents=True)
            stale = plots / "signed_G_P_I_heatmap.png"
            stale.write_bytes(b"stale")
            write_within_outputs(payload, config)
            self.assertFalse(stale.exists())
            effect_header = (config["output"] / "effects_long.csv").read_text(
                encoding="utf-8-sig"
            ).splitlines()[0]
            self.assertIn("classification_basis", effect_header)
            stratum_header = (config["output"] / "stratum_effects.csv").read_text(
                encoding="utf-8-sig"
            ).splitlines()[0]
            self.assertIn("metric_signature", stratum_header)

    def test_manifest_boolean_strings_and_invalid_independence_group_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.json"
            base = {
                "dataset_id": "demo",
                "samples": "samples.json",
                "output": "output",
                "metrics": {"family": "metrics.json"},
            }
            manifest.write_text(
                json.dumps({**base, "allow_partial": "false"}), encoding="utf-8"
            )
            args = within_parser().parse_args(["--manifest", str(manifest)])
            with self.assertRaisesRegex(ValueError, "JSON boolean"):
                resolve_within_config(args)
            manifest.write_text(
                json.dumps({**base, "independence_group": "   "}), encoding="utf-8"
            )
            args = within_parser().parse_args(["--manifest", str(manifest)])
            with self.assertRaisesRegex(ValueError, "nonempty string"):
                resolve_within_config(args)

    def test_renamed_resumable_checkpoint_is_detected_from_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            samples = [
                {
                    "sample_id": f"S{index}",
                    "group": group,
                    "match_stratum": "one",
                }
                for index, group in enumerate(("HW-B", "HW-P", "MG-B", "MG-P"))
            ]
            path = root / "renamed_metrics.json"
            path.write_text(
                json.dumps(
                    {
                        "metadata": {"resumable": True, "sample_count": 4},
                        "results": [
                            {**sample, "metrics": {"metric": index}, "errors": {}}
                            for index, sample in enumerate(samples)
                        ],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "resumable checkpoint"):
                load_metric_family(path, "family", samples, allow_partial=False)
            loaded = load_metric_family(path, "family", samples, allow_partial=True)
            self.assertTrue(loaded["partial_file"])
            self.assertFalse(loaded["partial_filename"])

    def test_invalid_meta_neutral_bound_is_rejected(self):
        args = meta_parser().parse_args(
            ["input.json", "--output", "out", "--neutral-bound", "-0.01"]
        )
        with self.assertRaisesRegex(ValueError, "neutral-bound"):
            resolve_meta_config(args)

    def test_meta_manifest_boolean_string_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "meta.json"
            manifest.write_text(
                json.dumps(
                    {
                        "inputs": ["within.json"],
                        "output": "out",
                        "allow_dependent": "false",
                    }
                ),
                encoding="utf-8",
            )
            args = meta_parser().parse_args(["--manifest", str(manifest)])
            with self.assertRaisesRegex(ValueError, "JSON boolean"):
                resolve_meta_config(args)

    def test_dependent_single_dataset_taxonomy_is_not_definitive(self):
        summaries = {}
        for effect in ("G", "P", "I"):
            summary = random_effects_summary(
                [0.5 if effect == "I" else 0.8], [0.05], labels=["D1"]
            )
            summary["q"] = 0.001
            summary["studies"] = [
                {"dataset_id": "D1", "estimate": summary["pooled"], "se": 0.05, "status": "complete"}
            ]
            summaries[effect] = {
                "family": "family",
                "feature": "metric",
                "metric_signature": "signature",
                "effect": effect,
                "summary": summary,
            }
        config = {
            "alpha": 0.05,
            "minimum_effect": 0.2,
            "minimum_direction_consistency": 0.8,
        }
        taxonomy = _cross_dataset_taxonomy(
            list(summaries.values()), config, robustness_comparison_only=True
        )
        label = taxonomy[0]["classification"]
        self.assertTrue(label.startswith("dependent_robustness_provisional_"))

    def test_direction_inconsistent_interaction_is_not_called_definitive(self):
        rows = []
        for effect in ("G", "P", "I"):
            summary = {
                "k": 4,
                "pooled": 0.8,
                "q": 0.001,
                "sign_consistency": 0.5 if effect == "I" else 1.0,
                "prediction_excludes_zero": effect != "I",
                "equivalence": {
                    "equivalent": False,
                    "prediction_interval_inside_bounds": False,
                },
                "studies": [],
            }
            rows.append(
                {
                    "family": "family",
                    "feature": "metric",
                    "metric_signature": "signature",
                    "effect": effect,
                    "summary": summary,
                }
            )
        taxonomy = _cross_dataset_taxonomy(
            rows,
            {
                "alpha": 0.05,
                "minimum_effect": 0.2,
                "minimum_direction_consistency": 0.8,
            },
            robustness_comparison_only=False,
        )
        self.assertEqual(
            taxonomy[0]["classification"], "direction_inconsistent_interaction"
        )

    def test_implicit_independence_group_is_robustness_only_end_to_end(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            within_path = root / "within.json"
            contrasts = {
                effect: {"standardized": {"estimate": 0.5, "se": 0.1}}
                for effect in ("G", "P", "I")
            }
            within_path.write_text(
                json.dumps(
                    {
                        "schema_version": "ephishgen.effects.within.v2",
                        "analysis": {
                            "dataset_id": "implicit-demo",
                            "independence_group": "implicit-demo",
                            "independence_group_explicit": False,
                            "provisional": False,
                            "variants": ["sample_weighted"],
                            "standardization": "Hedges standardization",
                            "standardized_se": "approximate delta method",
                            "estimator_signatures": {
                                "sample_weighted": "test-estimator-signature"
                            },
                        },
                        "diagnostics": {"sample_ids": ["S1"]},
                        "features": [
                            {
                                "family": "family",
                                "name": "metric",
                                "metric_signature": "signature",
                                "status": "complete",
                                "variants": {
                                    "sample_weighted": {"contrasts": contrasts}
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            config = {
                "inputs": [within_path],
                "output": root / "meta",
                "variant": "sample_weighted",
                "alpha": 0.05,
                "equivalence_bound": 0.2,
                "minimum_effect": 0.2,
                "minimum_direction_consistency": 0.8,
                "neutral_bound": 0.0,
                "allow_dependent": True,
                "allow_provisional": False,
                "include_lda": False,
                "plots": False,
                "max_plot_features": 10,
                "manifest": None,
            }
            payload = run_meta(config)
            self.assertTrue(payload["diagnostics"]["robustness_comparison_only"])
            self.assertEqual(
                payload["diagnostics"]["dependent_input_pairs"][0]["type"],
                "implicit_independence_group",
            )
            self.assertTrue(
                payload["taxonomy"][0]["classification"].startswith(
                    "dependent_robustness_"
                )
            )
            self.assertIn(
                "delta method",
                payload["analysis"]["standardized_se_methods"][0],
            )


if __name__ == "__main__":
    unittest.main()
