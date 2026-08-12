# Generation, phishing, and interaction effects

This directory implements the analysis progression in `phd - 研究步骤指导.pdf` as two reproducible stages:

1. `analyze_within.py` estimates Generation (`G`), Phishing (`P`), and Generation-by-Phishing Interaction (`I`) effects within one four-group dataset.
2. `meta_analyze.py` compares those signed effect profiles across genuinely independent datasets and quantifies direction consistency, magnitude, and heterogeneity.

The scripts characterize features. They do not train a detector, and their convenience taxonomies never replace the reported estimates, confidence intervals, and diagnostics.

## 1. Within-dataset model

For every finite, varying scalar metric, the script fits

```text
metric ~ Generation + Phishing + Generation:Phishing + match_stratum fixed effects
```

Generation and phishing use centered `-0.5/+0.5` coding. Consequently, the model coefficients directly equal the PDF contrasts:

```text
G = ((MG-P - HW-P) + (MG-B - HW-B)) / 2
P = ((HW-P - HW-B) + (MG-P - MG-B)) / 2
I =  (MG-P - HW-P) - (MG-B - HW-B)
```

The output also retains the four conditional contrasts:

```text
G_B  = MG-B - HW-B
G_P  = MG-P - HW-P
P_HW = HW-P - HW-B
P_MG = MG-P - MG-B
```

Every contrast is reported both in raw metric units and standardized by the fitted model's residual SD with the exact Hedges small-sample correction. The standardized SE includes residual-scale uncertainty through a documented delta-method approximation. Under HC3/CR1 this uses a residual-scale independence approximation; for confirmatory repeated-unit analyses, bootstrap the complete standardized contrast by resampling the true independent cluster. The default covariance is HC3. When repeated documents, prompts, campaigns, recipients, or templates are identifiable, pass their independent-unit field using `--cluster-field`; the script then uses CR1 cluster-robust covariance and cluster-based degrees of freedom.

### Interaction equivalence

A nonsignificant interaction is not evidence that interaction is absent. The script therefore runs two one-sided equivalence tests (TOST) against a declared standardized smallest effect size of interest, default `+/-0.2`. Its FDR-adjusted equivalence result is used by the feature taxonomy.

Choose this bound scientifically before inspecting results. `0.2` is an operational default, not a universal law.

### Run the completed current outputs

From the repository root:

```powershell
python effects/analyze_within.py --manifest effects/example_within_manifest.json
```

This manifest uses the currently complete Phishing and Stylometric outputs. To inspect the HWT/MGT checkpoint as explicitly provisional, add:

```powershell
python effects/analyze_within.py `
  --dataset-id scaled_8980_interim `
  --independence-group ephishgen_hwt_mgt_corpora `
  --samples scaled_stratified_pool_8980.json `
  --metrics hwt_mgt=calculation/HWT-MGT/results/scaled_stratified_pool_8980_metrics.partial.json `
  --allow-partial `
  --output effects/results/scaled_8980_hwt_interim
```

`--allow-partial` does not turn missing values into zero. Vector-valued UID outputs, constant features, invalid values, and features lacking all four factorial cells are skipped and documented. The current partially calculated PHD/MLE features have no machine rows and will therefore be rejected automatically.

Checkpoint detection does not rely only on the filename. The loader also treats explicit non-final status/partial flags, resumable outputs without `finished_utc`, extractor errors, missing rows, and incomplete declared feature inventories as provisional. New calculation writers should emit `status`, `expected_features` (or `feature_count`), extractor/version metadata, and a final completion marker.

The default permits a stratum with one observation in each factorial cell and flags it as sparse. Use `--min-cell-n 2` or higher as a stricter sensitivity analysis when the dataset has enough support. Small-sample inference for the matched 44-sample pool remains exploratory.

### Recommended future manifest

Copy `example_within_manifest.json` for each new dataset. Important fields are:

- `dataset_id`: unique analysis ID;
- `independence_group`: the underlying corpus/cohort; nested or resampled pools from the same corpora must share this value;
- `samples`: the explicit local dataset path—metadata paths embedded in calculation outputs are not followed;
- `metrics`: family/path/signature entries;
- `cluster_field`: preferably `base_document_id`, `prompt_id`, `campaign_id`, or another genuine independent unit when rows are related;
- `equivalence_bound`: the preregistered standardized interaction bound.

Manifest booleans must be real JSON `true`/`false` values; strings such as `"false"` are rejected. Unknown manifest fields are also rejected so misspelled safety settings cannot be ignored.

Measurement signatures prevent identically named but differently calculated metrics from being pooled. Include reference model/tokenizer revisions, preprocessing version, and any frozen learned artifact in a signature. LDA topic indices are not aligned when separate topic models are fitted, so `meta_analyze.py` excludes `lda_*` by default.

Even with `--include-lda`, LDA features require an explicit non-automatic signature identifying the same frozen vocabulary/topic artifact. This prevents separately fitted topic 0/topic 1 coordinates from being treated as if they were aligned.

### Within-dataset outputs

Each output directory contains:

- `within_effects.json`: complete machine-readable analysis;
- `effects_long.csv`: one row per feature, variant, and contrast;
- `four_cell_summary.csv`: raw and adjusted four-group means;
- `stratum_effects.csv`: descriptive stratum-specific G/P/I estimates on the common full-model residual-SD scale;
- `skipped_features.csv`: explicit skip reason and completeness counts;
- `diagnostics.json`: design, provenance, length, duplicate, and family diagnostics;
- `report.md`: readable effect summary;
- `plots/signed_G_P_I_heatmap.png`: signed standardized feature profiles;
- `plots/top_interaction_plots.png`: four-cell plots for the largest interactions.

The primary result is sample-weighted. By default, an equal-stratum-weighted sensitivity result is also fitted so a dominant scenario/goal stratum cannot silently determine the conclusion. Disable it only with `--no-equal-stratum`.

### Declared length sensitivity

Length can be part of the generation or phishing effect, so it is never controlled away silently. Add `--length-sensitivity` (or set `"length_sensitivity": true` in the manifest) to fit three secondary estimands. Conditional contrasts use the predeclared physical reference set by `--length-reference-words` (default 100), rather than a dataset-specific mean:

- `length_adjusted`: adds centered linear and quadratic log-word-count terms and assumes that curve is common to all four groups;
- `length_adjusted_varying_slopes`: additionally allows generation-, phishing-, and interaction-specific linear log-length slopes, showing how sensitive the adjusted G/P/I estimates are to the common-slope assumption;
- `length_common_support`: intersects the observed group min/max word-count ranges, then retains only strata that still have four-cell support.

The unadjusted `sample_weighted` model remains primary. The output records range-overlap bounds, before/after group counts and length summaries, per-feature variant failures, and an explicit mediator warning. Observed min/max overlap is outlier-sensitive and does **not** balance the retained length distributions; it is a restriction check, not length matching or weighting. These variants help show whether a feature effect is largely length-dependent; they do not identify a direct causal effect by themselves.

If every row has text, length is recomputed for every row using the recorded Unicode regex rule so mixed token-count definitions cannot enter one run. A complete provided `word_count` field is used uniformly only when at least one row has no text. The measurement method is part of the length-variant estimator signature.

Every feature also receives descriptive per-stratum G/P/I estimates. They use the primary model's residual SD for a common vertical scale and intentionally omit per-stratum p-values, which would be unstable in sparse matched cells.

## 2. Cross-dataset stability

Once several independent four-cell datasets have been analyzed:

```powershell
python effects/meta_analyze.py --manifest effects/example_meta_manifest.json
```

For every compatible feature and each of `G`, `P`, and `I`, the script reports:

- dataset-specific signed standardized effects;
- dominant-direction consistency and its exact binomial interval;
- median, interquartile range, and range;
- Paule-Mandel random-effects variance `tau^2` and `tau`;
- Cochran's `Q`, `Q` p-value, and `I^2`;
- modified Hartung-Knapp pooled effect and confidence interval;
- a prediction interval for a new dataset when at least three datasets exist;
- leave-one-dataset-out pooled estimates;
- FDR-adjusted pooled-effect and equivalence tests.

It also produces signed dataset-by-feature heatmaps plus pairwise Spearman correlation and sign-agreement matrices for complete dataset effect profiles.

Meta-analysis checks a per-variant estimator signature in addition to each metric's measurement signature. Reporting thresholds and unused sensitivity switches do not affect compatibility. Formula/coding, weighting or length specification, covariance family, standardization, and length-measurement definitions do. `length_common_support` is intentionally not meta-pooled because each dataset's observed range defines a different restricted population; use it as a within-dataset sensitivity only.

### Independence safeguards

By default, meta-analysis stops when inputs overlap by sample ID or share an `independence_group`. `--allow-dependent` exists only to create a visibly labelled robustness comparison. It does not make dependent pools statistically independent.

An explicit `independence_group` is required for meta-eligible within-dataset outputs. If it was omitted, `meta_analyze.py` stops unless `--allow-dependent` is supplied, in which case every taxonomy label is prefixed `dependent_robustness_`. Disjoint resamples from the same corpus are still dependent even when they share no sample IDs.

With one dataset, heterogeneity is not estimable. With two, a pooled estimate is possible but no prediction interval is reported. `tau^2`, `I^2`, direction consistency, and prediction intervals should remain exploratory until approximately five or more genuinely independent datasets contribute.

### Cross-dataset outputs

- `meta_effects.json` and `meta_effects.csv`;
- `feature_taxonomy.csv`;
- `dataset_profile_similarity.csv`;
- `report.md`;
- `plots/G_*`, `plots/P_*`, and `plots/I_*` heatmaps/correlation matrices.

## Taxonomy

Within one dataset, possible labels include:

- `stable_generation`;
- `stable_phishing`;
- `stable_dual`;
- `interaction_dependent`;
- `detectable_but_small_interaction`;
- `inconclusive_interaction`;
- `uninformative_within_bounds`.

Here, “stable” means stable across phishing intent **inside that dataset**, supported by interaction equivalence. It does not mean transferable.

Cross-dataset labels additionally use direction consistency, pooled magnitude, interaction equivalence, heterogeneity, and prediction intervals. A feature can have a large pooled effect yet remain unstable for a new dataset.

## Interpretation and design requirements

The scripts cannot repair confounding in the data design. In the current pool, all human documents come from the HWT corpus and all machine documents from `ephishLLM.json`; `G` is therefore a corpus/provenance-associated difference, not an isolated causal generation effect. The scripts flag this when the sample `source` field exposes it.

For the new dataset intended to isolate effects:

1. Cross generation source and intent within the same base scenarios or source documents.
2. Retain `base_document_id`, `prompt_id`, generation batch, LLM ID/version, decoding settings, dataset/corpus ID, and campaign/author identifiers.
3. Use scenario/goal labels defined before generation rather than derived from the analyzed text.
4. Deliberately cross several datasets with several LLMs; one dataset per LLM leaves dataset and LLM confounded.
5. Preserve length as an observed outcome. Report the total association first, then a declared length-standardized or common-support sensitivity analysis; do not silently control away length because it can be part of the effect.
6. Freeze learned measurement artifacts on training/external data before comparing datasets, especially LDA vocabularies/topics.
7. For eventual detector evaluation, perform feature selection, scaling, and threshold fitting inside training folds, followed by leave-one-dataset-out and leave-one-LLM-out tests.

## Tests

No additional test framework is required:

```powershell
python -m unittest discover -s effects/tests -v
```

The tests cover exact `G/P/I` algebra, standardization invariance, sample versus equal-stratum estimands, TOST behavior, FDR, conservative partial/vector handling, and stable versus heterogeneous meta-analysis examples.
