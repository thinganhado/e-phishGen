# HWT-MGT calculation modules

These modules implement the metric calculations documented in the repository-level [`METRICS.md`](https://github.com/). They intentionally do not preprocess text or load models. Source-specific model loading, file reading, tokenization, and input preparation adapters are in [`preprocess/`](preprocess/README.md).

Dependency declarations copied from the original repositories, together with the recommended two-environment split, are in [`requirements/`](requirements/README.md).

The caller must provide the required prepared values:

- `logits` and next-token `labels` for probability, entropy, rank, and rank-bucket metrics;
- token log-probabilities or NLL values for Average Log-Probability and Perplexity;
- original/perturbed or original/regenerated scores for discrepancy metrics;
- token surprisal vectors for GPT-Who UID metrics;
- already-tokenized sequences for n-gram metrics;
- contextual embedding matrices for PHD/MLE intrinsic dimension.

Because the directory name contains a hyphen, use it as a script/module directory on `PYTHONPATH`, or load modules by file path. For example:

```python
from average_log_probability import average_log_probability

score = average_log_probability(logits, next_token_labels)
```

The modules use PyTorch. `phd_intrinsic_dimension.py` additionally uses SciPy, and `mle_intrinsic_dimension.py` additionally uses `scikit-dimension`.

## Modules

| Module | Main function |
|---|---|
| `predictive_entropy.py` | `predictive_entropy` |
| `top10_entropy.py` | `top10_entropy` |
| `perplexity.py` | `perplexity_from_log_probs`, `perplexity_from_nll` |
| `average_log_probability.py` | `average_log_probability` |
| `mean_token_rank.py`, `mean_log_rank.py` | `mean_token_rank`, `mean_log_rank` |
| `top10_rank_ratio.py`, `rank_10_100_ratio.py`, `rank_100_1000_ratio.py`, `rank_gt1000_ratio.py` | corresponding rank-bucket ratio function |
| `probability_fraction.py` | `probability_fraction` |
| `detectgpt_curvature.py` | `detectgpt_discrepancy` |
| `dna_gpt_score.py` | `dna_gpt_score` |
| `fast_detectgpt_criterion.py` | `sampling_discrepancy`, `analytic_sampling_discrepancy` |
| `lrr.py`, `npr.py` | `lrr`, `npr` |
| `uid_mean.py`, `total_surprisal.py`, `uid_variance.py`, `uid_diff.py`, `uid_diff2.py` | corresponding UID function |
| `uid_min_span.py`, `uid_max_span.py` | `uid_min_span`, `uid_max_span` |
| `ngram_overlap_ratio.py`, `weighted_ngram_score.py` | corresponding n-gram function |
| `phd_intrinsic_dimension.py`, `mle_intrinsic_dimension.py` | corresponding intrinsic-dimension function |
| `negative_mean_token_rank.py`, `negative_mean_log_rank.py` | detector-oriented signed rank functions |
