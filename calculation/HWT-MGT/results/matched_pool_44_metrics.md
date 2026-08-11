# HWT-MGT descriptive comparison

This report uses the calculated metrics to assess two separate distinctions:
whether text is human-written or machine-generated, and whether text is phishing or benign.
Individual sample values are intentionally omitted; the raw values remain in the JSON file.

## Dataset and notation

- Total samples: **44**
- `HW-P`: **11**; `MG-P`: **11**
- `HW-B`: **11**; `MG-B`: **11**
- Each pooled comparison contains 22 samples per side.
- Difference is calculated as left mean minus right mean.
- Cohen d is a standardized effect size; larger absolute values indicate stronger separation in this sample.

## HWT versus MGT

This pools phishing and benign samples: `HW = HW-P + HW-B` and `MG = MG-P + MG-B`. It directly evaluates whether the metrics distinguish human-written from machine-generated text.

| Metric | HW mean | MG mean | Difference (HW - MG) | Cohen d |
|---|---:|---:|---:|---:|
| Average log probability | -3.5204 | -3.0237 | -0.4967 | -0.8609 |
| Detectgpt discrepancy | 0.0388 | 0.0422 | -0.0033 | -0.0414 |
| Detectgpt normalized discrepancy | 0.2916 | 0.4821 | -0.1905 | -0.2582 |
| Dna gpt regeneration log probability difference | -1.0507 | -0.5895 | -0.4613 | -0.6040 |
| Fast detectgpt analytic | 0.0565 | 0.8382 | -0.7818 | -0.7351 |
| Fast detectgpt sampling | 2.1500 | 2.2785 | -0.1285 | -0.3345 |
| Lrr | 1.8298 | 1.9332 | -0.1034 | -1.3030 |
| Mean log rank | 1.9482 | 1.5667 | 0.3816 | 0.9880 |
| Mean token rank | 277.4736 | 137.5139 | 139.9597 | 0.9934 |
| Mle intrinsic dimension | 10.6639 | 11.7642 | -1.1003 | -1.2672 |
| Negative mean log rank | -1.9482 | -1.5667 | -0.3816 | -0.9880 |
| Negative mean token rank | -277.4736 | -137.5139 | -139.9597 | -0.9934 |
| Ngram overlap ratio | 0.2493 | 0.3101 | -0.0608 | -0.8009 |
| Npr | 1.0131 | 1.0168 | -0.0037 | -0.1121 |
| Perplexity from causal log probs | 44.9433 | 21.4914 | 23.4518 | 0.8788 |
| Perplexity gpt2 large | 39.4911 | 19.4802 | 20.0109 | 0.8558 |
| Phd intrinsic dimension | 7.8447 | 9.6938 | -1.8491 | -1.1685 |
| Predictive entropy | 3.5084 | 3.2115 | 0.2969 | 0.6862 |
| Probability fraction | 0.4842 | 0.5343 | -0.0501 | -0.6657 |
| Rank 100 1000 ratio | 0.0990 | 0.0663 | 0.0327 | 1.1593 |
| Rank 10 100 ratio | 0.1797 | 0.1700 | 0.0097 | 0.2253 |
| Rank gt1000 ratio | 0.0518 | 0.0279 | 0.0239 | 1.0722 |
| Top10 entropy | 1.4488 | 1.4746 | -0.0257 | -0.1871 |
| Top10 rank ratio | 0.6695 | 0.7359 | -0.0663 | -0.9218 |
| Total surprisal | 509.8695 | 331.1265 | 178.7430 | 2.0332 |
| Uid diff | 3.0200 | 2.7154 | 0.3046 | 0.7533 |
| Uid diff2 | 16.5899 | 13.6032 | 2.9867 | 0.7998 |
| Uid max span | 3.8090 | 3.2239 | 0.5851 | 0.9135 |
| Uid mean | 3.3536 | 2.8803 | 0.4733 | 0.8244 |
| Uid min span | 3.1343 | 2.6198 | 0.5145 | 0.6979 |
| Uid variance | 9.6968 | 8.2978 | 1.3990 | 0.9181 |
| Weighted ngram score | 0.0011 | 0.0036 | -0.0024 | -0.7114 |

### Outstanding observations

- The strongest HWT/MGT separation is in `lrr` (Cohen d = -1.303): MG has the higher mean.
- Other comparatively strong HWT/MGT differences are `mle_intrinsic_dimension` (d = -1.267), `phd_intrinsic_dimension` (d = -1.169), rank 100-1000 ratio (d = 1.159), mean token rank (d = 0.993), and mean log rank (d = 0.988).
- The two perplexity measures also separate the groups substantially: both are higher for HW, with d about 0.86. Average log probability shows a similar pattern, with MG having the higher (less negative) mean.
- `detectgpt_discrepancy` is nearly unchanged between HW and MG (d = -0.041), and `npr` is also weak (d = -0.112); these metrics do not distinguish authorship strongly in this sample.


## Phishing versus benign

This pools authorship sources: `P = HW-P + MG-P` and `B = HW-B + MG-B`. It directly evaluates whether the metrics distinguish phishing from benign text.

| Metric | P mean | B mean | Difference (P - B) | Cohen d |
|---|---:|---:|---:|---:|
| Average log probability | -3.1380 | -3.4061 | 0.2681 | 0.4357 |
| Detectgpt discrepancy | 0.0637 | 0.0173 | 0.0464 | 0.6026 |
| Detectgpt normalized discrepancy | 0.5682 | 0.2055 | 0.3627 | 0.5031 |
| Dna gpt regeneration log probability difference | -0.6072 | -1.0330 | 0.4257 | 0.5536 |
| Fast detectgpt analytic | 0.5596 | 0.3351 | 0.2245 | 0.1986 |
| Fast detectgpt sampling | 2.2534 | 2.1751 | 0.0783 | 0.2021 |
| Lrr | 1.8858 | 1.8772 | 0.0085 | 0.0896 |
| Mean log rank | 1.6836 | 1.8314 | -0.1478 | -0.3469 |
| Mean token rank | 201.9351 | 213.0525 | -11.1174 | -0.0704 |
| Mle intrinsic dimension | 11.1576 | 11.2704 | -0.1128 | -0.1092 |
| Negative mean log rank | -1.6836 | -1.8314 | 0.1478 | 0.3469 |
| Negative mean token rank | -201.9351 | -213.0525 | 11.1174 | 0.0704 |
| Ngram overlap ratio | 0.3118 | 0.2476 | 0.0642 | 0.8543 |
| Npr | 1.0236 | 1.0064 | 0.0172 | 0.5427 |
| Perplexity from causal log probs | 30.0871 | 36.3475 | -6.2604 | -0.2152 |
| Perplexity gpt2 large | 26.8612 | 32.1101 | -5.2488 | -0.2068 |
| Phd intrinsic dimension | 8.7540 | 8.7844 | -0.0304 | -0.0165 |
| Predictive entropy | 3.2561 | 3.4638 | -0.2076 | -0.4654 |
| Probability fraction | 0.5284 | 0.4902 | 0.0382 | 0.4961 |
| Rank 100 1000 ratio | 0.0775 | 0.0878 | -0.0103 | -0.3182 |
| Rank 10 100 ratio | 0.1722 | 0.1775 | -0.0054 | -0.1241 |
| Rank gt1000 ratio | 0.0376 | 0.0420 | -0.0044 | -0.1726 |
| Top10 entropy | 1.4356 | 1.4878 | -0.0523 | -0.3856 |
| Top10 rank ratio | 0.7127 | 0.6927 | 0.0200 | 0.2540 |
| Total surprisal | 384.7176 | 456.2784 | -71.5608 | -0.5891 |
| Uid diff | 2.8383 | 2.8971 | -0.0589 | -0.1362 |
| Uid diff2 | 15.0526 | 15.1406 | -0.0880 | -0.0218 |
| Uid max span | 3.4470 | 3.5858 | -0.1388 | -0.1973 |
| Uid mean | 3.0216 | 3.2123 | -0.1908 | -0.3100 |
| Uid min span | 2.8568 | 2.8972 | -0.0404 | -0.0516 |
| Uid variance | 8.9690 | 9.0255 | -0.0565 | -0.0336 |
| Weighted ngram score | 0.0028 | 0.0020 | 0.0008 | 0.2100 |

### Outstanding observations

- The largest phishing/benign separation is `ngram_overlap_ratio` (d = 0.854), with a higher mean for phishing samples.
- DetectGPT discrepancy (d = 0.603), total surprisal (d = -0.589), DNA regeneration difference (d = 0.554), NPR (d = 0.543), and normalized DetectGPT discrepancy (d = 0.503) show moderate separation.
- Phishing has lower predictive entropy (d = -0.465) and lower perplexity (d about -0.21) than benign text. Thus, the direction is metric-dependent rather than uniformly higher for phishing.
- Rank-based measures are weak for phishing/benign separation: mean token rank has d = -0.070, and the rank-bucket ratios are all below |d| = 0.32.
- Intrinsic-dimension and UID metrics are effectively unchanged between phishing and benign text; PHD has d = -0.017 and UID variance has d = -0.034.


## Annotation-group context

These four means show whether a pooled separation is consistent across the underlying annotations.

| Metric | HW-P | MG-P | HW-B | MG-B |
|---|---:|---:|---:|---:|
| Average log probability | -3.4337 | -2.8423 | -3.6071 | -3.2051 |
| Detectgpt discrepancy | 0.0505 | 0.0769 | 0.0272 | 0.0074 |
| Detectgpt normalized discrepancy | 0.4603 | 0.6760 | 0.1228 | 0.2882 |
| Dna gpt regeneration log probability difference | -0.9097 | -0.3047 | -1.1918 | -0.8742 |
| Fast detectgpt analytic | 0.2095 | 0.9098 | -0.0965 | 0.7667 |
| Fast detectgpt sampling | 2.1686 | 2.3382 | 2.1314 | 2.2187 |
| Lrr | 1.8339 | 1.9377 | 1.8258 | 1.9287 |
| Mean log rank | 1.8975 | 1.4696 | 1.9990 | 1.6637 |
| Mean token rank | 264.7519 | 139.1183 | 290.1954 | 135.9095 |
| Mle intrinsic dimension | 10.7155 | 11.5997 | 10.6123 | 11.9286 |
| Negative mean log rank | -1.8975 | -1.4696 | -1.9990 | -1.6637 |
| Negative mean token rank | -264.7519 | -139.1183 | -290.1954 | -135.9095 |
| Ngram overlap ratio | 0.2713 | 0.3522 | 0.2272 | 0.2679 |
| Npr | 1.0188 | 1.0283 | 1.0074 | 1.0053 |
| Perplexity from causal log probs | 42.6743 | 17.5000 | 47.2122 | 25.4828 |
| Perplexity gpt2 large | 37.3764 | 16.3461 | 41.6058 | 22.6143 |
| Phd intrinsic dimension | 7.8662 | 9.6419 | 7.8232 | 9.7456 |
| Predictive entropy | 3.4588 | 3.0534 | 3.5580 | 3.3695 |
| Probability fraction | 0.4965 | 0.5603 | 0.4720 | 0.5084 |
| Rank 100 1000 ratio | 0.0969 | 0.0581 | 0.1012 | 0.0744 |
| Rank 10 100 ratio | 0.1789 | 0.1654 | 0.1804 | 0.1746 |
| Rank gt1000 ratio | 0.0488 | 0.0264 | 0.0547 | 0.0293 |
| Top10 entropy | 1.4478 | 1.4233 | 1.4498 | 1.5258 |
| Top10 rank ratio | 0.6754 | 0.7501 | 0.6637 | 0.7217 |
| Total surprisal | 459.6052 | 309.8300 | 560.1337 | 352.4230 |
| Uid diff | 2.9732 | 2.7034 | 3.0668 | 2.7274 |
| Uid diff2 | 16.1329 | 13.9723 | 17.0469 | 13.2342 |
| Uid max span | 3.6426 | 3.2514 | 3.9754 | 3.1963 |
| Uid mean | 3.2862 | 2.7569 | 3.4210 | 3.0037 |
| Uid min span | 3.2862 | 2.4274 | 2.9823 | 2.8121 |
| Uid variance | 9.5072 | 8.4308 | 9.8864 | 8.1647 |
| Weighted ngram score | 0.0003 | 0.0052 | 0.0020 | 0.0020 |

## How to read the separation

- The `Difference` column shows the direction and magnitude in the metric's original units.
- The `Cohen d` column makes separation more comparable across metrics with different scales. Inspect the largest absolute values first.
- A positive `HW - MG` value means the metric is higher for human-written text; a negative value means it is higher for machine-generated text.
- A positive `P - B` value means the metric is higher for phishing text; a negative value means it is higher for benign text.
- These are descriptive comparisons, not statistical significance tests or trained classification results.
- `uid_min_span` and `uid_max_span` are reduced to one mean per sample before group aggregation; raw vectors are not printed.
- All 34 metric fields were present for all 44 samples, with zero recorded calculation errors.

## Reproducibility

The complete per-sample values remain available in `matched_pool_44_metrics.json`.
