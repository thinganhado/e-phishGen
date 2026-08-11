# Descriptive distribution analysis

This report compares HW-P with MG-P and HW-B with MG-B independently.
It describes the observed matched sample only (`n=11` per class per pair);
it is not a significance test or a generalization claim.

Interpretation: `effect` is the signed MG-minus-HW difference divided by
the pooled sample SD. The histogram overlap coefficient (OVL) ranges from
0 (little overlap) to 1 (complete overlap). Shape flags use Tukey outliers
and conservative histogram diagnostics; multimodality flags are tentative
at this small sample size.
UID span metrics are vector-valued in the source JSON; their rows pool all
available span elements and should not be interpreted as 11 independent
document-level observations.

## HWT-MGT

Source: `HWT-MGT\results\matched_pool_44_metrics.json`

### HW-P vs MG-P

| Feature | HW median [Q1, Q3] | MG median [Q1, Q3] | Mean HW → MG | Effect | OVL | Shape notes |
|---|---:|---:|---:|---:|---:|---|
| `average_log_probability` | -3.3362 [-3.573, -3.0121] | -2.8787 [-2.9476, -2.7288] | -3.4337 -> -2.8423 (clear MG shift; MG higher) | 0.93 | 0.55 | variance lower in MG (SD ratio 0.2669); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `detectgpt_discrepancy` | 0.0247 [-0.0116, 0.0983] | 0.0782 [0.0516, 0.1316] | 0.0505 -> 0.0769 (small MG shift; MG higher) | 0.30 | 0.45 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 4/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `detectgpt_normalized_discrepancy` | 0.14 [-0.0461, 1.0738] | 0.6376 [0.5642, 0.8329] | 0.4603 -> 0.676 (small MG shift; MG higher) | 0.28 | 0.45 | possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/3 |
| `dna_gpt_regeneration_log_probability_difference` | -0.6181 [-1.0052, -0.4021] | -0.395 [-0.4791, 0.0477] | -0.9097 -> -0.3047 (clear MG shift; MG higher) | 0.81 | 0.73 | variance lower in MG (SD ratio 0.4302); possible multimodality (peaks HW/MG 2/4; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `fast_detectgpt_analytic` | 0.3939 [-0.4004, 0.83] | 0.8404 [0.6499, 1.207] | 0.2095 -> 0.9098 (moderate MG shift; MG higher) | 0.78 | 0.45 | possible multimodality (peaks HW/MG 3/3; tentative at n=11); Tukey outliers HW/MG 0/2 |
| `fast_detectgpt_sampling` | 2.3277 [2.1257, 2.4027] | 2.3161 [2.178, 2.431] | 2.1686 -> 2.3382 (moderate MG shift; MG higher) | 0.47 | 0.82 | variance lower in MG (SD ratio 0.4873); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 2/1 |
| `lrr` | 1.8273 [1.7773, 1.904] | 1.941 [1.8934, 1.9711] | 1.8339 -> 1.9377 (clear MG shift; MG higher) | 1.08 | 0.55 | variance lower in MG (SD ratio 0.5665); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `mean_log_rank` | 1.7668 [1.6091, 2.0104] | 1.5168 [1.3792, 1.57] | 1.8975 -> 1.4696 (clear MG shift; MG lower) | -0.97 | 0.55 | variance lower in MG (SD ratio 0.2523); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/3; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `mean_token_rank` | 160.9815 [139.3828, 314.8857] | 141.0133 [96.8858, 192.8602] | 264.7519 -> 139.1183 (moderate MG shift; MG lower) | -0.70 | 0.82 | variance lower in MG (SD ratio 0.2645); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `mle_intrinsic_dimension` | 11.009 [10.0779, 11.1638] | 11.6702 [11.1997, 11.9084] | 10.7155 -> 11.5997 (clear MG shift; MG higher) | 0.98 | 0.64 | variance lower in MG (SD ratio 0.5001); possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `negative_mean_log_rank` | -1.7668 [-2.0104, -1.6091] | -1.5168 [-1.57, -1.3792] | -1.8975 -> -1.4696 (clear MG shift; MG higher) | 0.97 | 0.55 | variance lower in MG (SD ratio 0.2523); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/3; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `negative_mean_token_rank` | -160.9815 [-314.8857, -139.3828] | -141.0133 [-192.8602, -96.8858] | -264.7519 -> -139.1183 (moderate MG shift; MG higher) | 0.70 | 0.82 | variance lower in MG (SD ratio 0.2645); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `ngram_overlap_ratio` | 0.3049 [0.2222, 0.3268] | 0.3468 [0.3162, 0.3989] | 0.2713 -> 0.3522 (clear MG shift; MG higher) | 1.00 | 0.45 | possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `npr` | 1.0038 [0.9968, 1.0396] | 1.0295 [1.0154, 1.0507] | 1.0188 -> 1.0283 (small MG shift; MG higher) | 0.25 | 0.55 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `perplexity_from_causal_log_probs` | 28.1122 [20.333, 35.6694] | 17.7914 [15.3177, 19.0725] | 42.6743 -> 17.5 (moderate MG shift; MG lower) | -0.79 | 0.73 | variance lower in MG (SD ratio 0.0889); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 2/1 |
| `perplexity_gpt2_large` | 25.4036 [17.8017, 32.3035] | 15.5879 [13.6194, 17.469] | 37.3764 -> 16.3461 (moderate MG shift; MG lower) | -0.79 | 0.64 | variance lower in MG (SD ratio 0.1264); Tukey outliers HW/MG 2/1 |
| `perturbation_count` | 5 [5, 5] | 5 [5, 5] | 5 -> 5 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `phd_intrinsic_dimension` | 7.2592 [6.7018, 8.704] | 9.2823 [8.7163, 10.6426] | 7.8662 -> 9.6419 (clear MG shift; MG higher) | 0.95 | 0.55 | possible multimodality (peaks HW/MG 2/1; tentative at n=11) |
| `predictive_entropy` | 3.446 [3.1339, 3.641] | 3.0439 [2.9482, 3.1791] | 3.4588 -> 3.0534 (clear MG shift; MG lower) | -0.85 | 0.45 | variance lower in MG (SD ratio 0.2613); possible multimodality (peaks HW/MG 3/3; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `probability_fraction` | 0.5149 [0.4595, 0.5454] | 0.552 [0.5348, 0.5881] | 0.4965 -> 0.5603 (clear MG shift; MG higher) | 0.84 | 0.36 | variance lower in MG (SD ratio 0.3433); possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `rank_100_1000_ratio` | 0.0952 [0.0716, 0.1027] | 0.0603 [0.0528, 0.0649] | 0.0969 -> 0.0581 (clear MG shift; MG lower) | -1.05 | 0.36 | variance lower in MG (SD ratio 0.2781); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `rank_10_100_ratio` | 0.1782 [0.1567, 0.1933] | 0.1724 [0.1472, 0.179] | 0.1789 -> 0.1654 (small MG shift; MG lower) | -0.33 | 0.73 | possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `rank_gt1000_ratio` | 0.0396 [0.0315, 0.0563] | 0.0252 [0.0191, 0.0354] | 0.0488 -> 0.0264 (clear MG shift; MG lower) | -0.91 | 0.64 | variance lower in MG (SD ratio 0.3599); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/4; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `regeneration_count` | 10 [10, 10] | 10 [10, 10] | 10 -> 10 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `top10_entropy` | 1.3981 [1.3616, 1.6033] | 1.4098 [1.3791, 1.4516] | 1.4478 -> 1.4233 (essentially overlapping location; MG lower) | -0.19 | 0.55 | variance lower in MG (SD ratio 0.3834); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `top10_rank_ratio` | 0.6931 [0.6444, 0.7305] | 0.7328 [0.7259, 0.7762] | 0.6754 -> 0.7501 (clear MG shift; MG higher) | 0.92 | 0.55 | variance lower in MG (SD ratio 0.3846); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `total_surprisal` | 472.0294 [393.9697, 524.9837] | 290.9645 [287.7366, 345.246] | 459.6052 -> 309.83 (clear MG shift; MG lower) | -1.32 | 0.36 | variance lower in MG (SD ratio 0.5031); possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `uid_diff` | 2.7042 [2.5352, 3.4157] | 2.6682 [2.5759, 2.7382] | 2.9732 -> 2.7034 (moderate MG shift; MG lower) | -0.60 | 0.73 | variance lower in MG (SD ratio 0.5453); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 0/2 |
| `uid_diff2` | 14.2546 [12.716, 19.6662] | 13.3622 [12.5893, 14.2236] | 16.1329 -> 13.9723 (moderate MG shift; MG lower) | -0.52 | 0.73 | skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 0/2 |
| `uid_max_span` | 2.7632 [0.6295, 5.8487] | 2.2881 [0.7302, 4.5514] | 3.6426 -> 3.2514 (essentially overlapping location; MG lower) | -0.12 | 0.88 | Tukey outliers HW/MG 3/28 |
| `uid_mean` | 3.25 [2.9024, 3.3787] | 2.7095 [2.6243, 2.8731] | 3.2862 -> 2.7569 (clear MG shift; MG lower) | -0.85 | 0.55 | variance lower in MG (SD ratio 0.3236); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 2/1 |
| `uid_min_span` | 2.4905 [0.7645, 4.8831] | 1.4645 [0.3981, 3.737] | 3.2862 -> 2.4274 (small MG shift; MG lower) | -0.30 | 0.85 | Tukey outliers HW/MG 10/18 |
| `uid_variance` | 8.6151 [8.1314, 11.2066] | 8.4356 [7.8879, 8.8648] | 9.5072 -> 8.4308 (moderate MG shift; MG lower) | -0.61 | 0.73 | variance lower in MG (SD ratio 0.6457); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/2 |
| `weighted_ngram_score` | 0 [0, 0] | 0.0041 [0.0014, 0.0095] | 0.000319 -> 0.0052 (clear MG shift; MG higher) | 1.23 | 0.36 | variance higher in MG (SD ratio 4.0627); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |

Constant-valued metrics and metrics missing from either class are omitted.

### HW-B vs MG-B

| Feature | HW median [Q1, Q3] | MG median [Q1, Q3] | Mean HW → MG | Effect | OVL | Shape notes |
|---|---:|---:|---:|---:|---:|---|
| `average_log_probability` | -3.4582 [-4.0904, -3.1275] | -3.2082 [-3.3291, -3.0878] | -3.6071 -> -3.2051 (moderate MG shift; MG higher) | 0.68 | 0.45 | variance lower in MG (SD ratio 0.3557); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `detectgpt_discrepancy` | 0.0462 [0.0027, 0.0571] | 0.0248 [-0.0513, 0.0565] | 0.0272 -> 0.0074 (small MG shift; MG lower) | -0.30 | 0.91 | possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `detectgpt_normalized_discrepancy` | 0.2985 [-0.1416, 0.4298] | 0.2738 [-0.3047, 0.8764] | 0.1228 -> 0.2882 (small MG shift; MG higher) | 0.25 | 0.64 | possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `dna_gpt_regeneration_log_probability_difference` | -1.0836 [-1.8376, -0.3869] | -0.9129 [-1.2521, -0.5758] | -1.1918 -> -0.8742 (moderate MG shift; MG higher) | 0.40 | 0.64 | variance lower in MG (SD ratio 0.5382); possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `fast_detectgpt_analytic` | 0.2394 [-1.3869, 1.0658] | 0.9627 [0.184, 1.3516] | -0.0965 -> 0.7667 (moderate MG shift; MG higher) | 0.65 | 0.45 | possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `fast_detectgpt_sampling` | 2.2216 [1.9191, 2.5183] | 2.2508 [1.9802, 2.468] | 2.1314 -> 2.2187 (small MG shift; MG higher) | 0.21 | 0.73 | variance lower in MG (SD ratio 0.6103); possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `lrr` | 1.8554 [1.7547, 1.883] | 1.9299 [1.9095, 1.9439] | 1.8258 -> 1.9287 (clear MG shift; MG higher) | 1.09 | 0.45 | variance lower in MG (SD ratio 0.6565); possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 0/3 |
| `mean_log_rank` | 1.8256 [1.6771, 2.3407] | 1.6969 [1.568, 1.7662] | 1.999 -> 1.6637 (clear MG shift; MG lower) | -0.82 | 0.55 | variance lower in MG (SD ratio 0.2992); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `mean_token_rank` | 290 [203.4625, 398.636] | 137.4804 [80.3741, 194.9689] | 290.1954 -> 135.9095 (clear MG shift; MG lower) | -1.15 | 0.27 | variance lower in MG (SD ratio 0.4395); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `mle_intrinsic_dimension` | 10.4738 [10.0779, 11.426] | 11.8642 [11.4589, 12.4098] | 10.6123 -> 11.9286 (clear MG shift; MG higher) | 1.15 | 0.45 | variance lower in MG (SD ratio 0.5255); possible multimodality (peaks HW/MG 2/4; tentative at n=11) |
| `negative_mean_log_rank` | -1.8256 [-2.3407, -1.6771] | -1.6969 [-1.7662, -1.568] | -1.999 -> -1.6637 (clear MG shift; MG higher) | 0.82 | 0.55 | variance lower in MG (SD ratio 0.2992); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `negative_mean_token_rank` | -290 [-398.636, -203.4625] | -137.4804 [-194.9689, -80.3741] | -290.1954 -> -135.9095 (clear MG shift; MG higher) | 1.15 | 0.27 | variance lower in MG (SD ratio 0.4395); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `ngram_overlap_ratio` | 0.2179 [0.1993, 0.2509] | 0.2841 [0.2116, 0.3149] | 0.2272 -> 0.2679 (moderate MG shift; MG higher) | 0.59 | 0.64 | possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `npr` | 1.0066 [0.9985, 1.0217] | 1.016 [0.982, 1.0239] | 1.0074 -> 1.0053 (essentially overlapping location; MG lower) | -0.09 | 0.64 | possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `perplexity_from_causal_log_probs` | 31.7608 [23.1012, 59.7848] | 24.7343 [22.0131, 27.921] | 47.2122 -> 25.4828 (clear MG shift; MG lower) | -0.83 | 0.55 | variance lower in MG (SD ratio 0.2017); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 1/1 |
| `perplexity_gpt2_large` | 29.6834 [19.0055, 54.6765] | 22.6669 [18.1196, 26.4403] | 41.6058 -> 22.6143 (moderate MG shift; MG lower) | -0.79 | 0.55 | variance lower in MG (SD ratio 0.2068); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `perturbation_count` | 5 [5, 5] | 5 [5, 5] | 5 -> 5 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `phd_intrinsic_dimension` | 7.359 [6.546, 8.1355] | 9.8051 [9.2907, 10.1098] | 7.8232 -> 9.7456 (clear MG shift; MG higher) | 1.06 | 0.36 | variance lower in MG (SD ratio 0.5912); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 2/2 |
| `predictive_entropy` | 3.5637 [3.3548, 3.8231] | 3.2898 [3.1851, 3.6249] | 3.558 -> 3.3695 (moderate MG shift; MG lower) | -0.46 | 0.55 | variance lower in MG (SD ratio 0.5508); possible multimodality (peaks HW/MG 3/3; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `probability_fraction` | 0.4611 [0.3996, 0.539] | 0.5085 [0.479, 0.5302] | 0.472 -> 0.5084 (moderate MG shift; MG higher) | 0.47 | 0.36 | variance lower in MG (SD ratio 0.3205); possible multimodality (peaks HW/MG 4/4; tentative at n=11) |
| `rank_100_1000_ratio` | 0.1033 [0.0797, 0.1141] | 0.0725 [0.0618, 0.078] | 0.1012 -> 0.0744 (clear MG shift; MG lower) | -0.99 | 0.55 | skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `rank_10_100_ratio` | 0.1758 [0.1392, 0.2107] | 0.1667 [0.1568, 0.1926] | 0.1804 -> 0.1746 (essentially overlapping location; MG lower) | -0.13 | 0.45 | variance lower in MG (SD ratio 0.4152); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `rank_gt1000_ratio` | 0.048 [0.0384, 0.0686] | 0.029 [0.0188, 0.0338] | 0.0547 -> 0.0293 (clear MG shift; MG lower) | -0.97 | 0.36 | variance lower in MG (SD ratio 0.5404); Tukey outliers HW/MG 1/1 |
| `regeneration_count` | 10 [10, 10] | 10 [10, 10] | 10 -> 10 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `top10_entropy` | 1.4626 [1.3459, 1.5623] | 1.5074 [1.4934, 1.5631] | 1.4498 -> 1.5258 (moderate MG shift; MG higher) | 0.54 | 0.64 | variance lower in MG (SD ratio 0.5596); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 0/3 |
| `top10_rank_ratio` | 0.7017 [0.5911, 0.733] | 0.7273 [0.7111, 0.7398] | 0.6637 -> 0.7217 (moderate MG shift; MG higher) | 0.75 | 0.64 | variance lower in MG (SD ratio 0.3159); possible multimodality (peaks HW/MG 2/3; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `total_surprisal` | 565.155 [519.4945, 624.281] | 356.6073 [327.4543, 378.5808] | 560.1337 -> 352.423 (clear MG shift; MG lower) | -1.61 | 0.18 | variance lower in MG (SD ratio 0.4245); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `uid_diff` | 2.9848 [2.7165, 3.4722] | 2.7051 [2.5676, 2.9275] | 3.0668 -> 2.7274 (clear MG shift; MG lower) | -0.83 | 0.55 | possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `uid_diff2` | 15.6672 [14.6119, 20.8879] | 13.1078 [10.6867, 15.6022] | 17.0469 -> 13.2342 (clear MG shift; MG lower) | -0.98 | 0.64 | possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `uid_max_span` | 3.2784 [0.7097, 6.2351] | 2.4009 [0.7235, 4.6067] | 3.9754 -> 3.1963 (small MG shift; MG lower) | -0.23 | 0.85 | possible multimodality (peaks HW/MG 2/1; tentative at n=550); Tukey outliers HW/MG 5/22 |
| `uid_mean` | 3.3746 [2.8461, 3.9806] | 3.0472 [2.8005, 3.214] | 3.421 -> 3.0037 (moderate MG shift; MG lower) | -0.69 | 0.55 | variance lower in MG (SD ratio 0.3439); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `uid_min_span` | 2.3302 [0.6125, 4.53] | 2.1169 [0.7321, 4.1694] | 2.9823 -> 2.8121 (essentially overlapping location; MG lower) | -0.06 | 0.89 | Tukey outliers HW/MG 7/16 |
| `uid_variance` | 10.3542 [9.0678, 10.982] | 8.5618 [6.9133, 9.0414] | 9.8864 -> 8.1647 (clear MG shift; MG lower) | -1.07 | 0.45 | possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `weighted_ngram_score` | 0 [0, 0.0037] | 0 [0, 0.0022] | 0.002 -> 0.002 (essentially overlapping location; MG higher) | 0.01 | 0.82 | possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/2 |

Constant-valued metrics and metrics missing from either class are omitted.

## Phishing

Source: `Phishing\results\matched_pool_44_phishing_metrics.json`

### HW-P vs MG-P

| Feature | HW median [Q1, Q3] | MG median [Q1, Q3] | Mean HW → MG | Effect | OVL | Shape notes |
|---|---:|---:|---:|---:|---:|---|
| `authority_density` | 0 [0, 0.859] | 0 [0, 0.5] | 0.392 -> 0.3521 (essentially overlapping location; MG lower) | -0.07 | 0.82 | possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `clause_density` | 1.5 [1.3885, 1.823] | 2 [1.6605, 2.155] | 1.6477 -> 1.8937 (moderate MG shift; MG higher) | 0.62 | 0.45 | variance lower in MG (SD ratio 0.5834); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `cta_density` | 2 [1.297, 5.3065] | 5.263 [4.361, 5.6045] | 3.1616 -> 5.1999 (clear MG shift; MG higher) | 0.87 | 0.36 | possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `first_person_ratio` | 0.0305 [0.0221, 0.0518] | 0.0286 [0.018, 0.0362] | 0.0358 -> 0.029 (small MG shift; MG lower) | -0.40 | 0.64 | possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `imperative_count` | 0 [0, 0.5] | 0 [0, 0] | 0.2727 -> 0.0909 (moderate MG shift; MG lower) | -0.46 | 0.82 | variance lower in MG (SD ratio 0.6455); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `mean_parse_depth` | 2.185 [2.058, 2.3335] | 2.183 [2.1415, 2.508] | 2.1895 -> 2.3081 (moderate MG shift; MG higher) | 0.50 | 0.73 | possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `mean_sentence_len_tokens` | 13.692 [12, 15.5715] | 18.429 [15.625, 19.6665] | 13.554 -> 17.9848 (clear MG shift; MG higher) | 1.17 | 0.36 | possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `mean_word_len` | 5.327 [5.014, 5.6425] | 5.491 [5.429, 5.672] | 5.2959 -> 5.5264 (moderate MG shift; MG higher) | 0.67 | 0.55 | variance lower in MG (SD ratio 0.4793); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `noun_ratio` | 0.1846 [0.1441, 0.2228] | 0.1818 [0.1694, 0.2044] | 0.1907 -> 0.1869 (essentially overlapping location; MG lower) | -0.09 | 0.45 | variance lower in MG (SD ratio 0.415); possible multimodality (peaks HW/MG 4/3; tentative at n=11) |
| `politeness_density` | 1.98 [1.184, 3.2515] | 3.571 [3.0875, 4.5445] | 2.2048 -> 3.9658 (clear MG shift; MG higher) | 1.08 | 0.45 | possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `second_person_ratio` | 0.0608 [0.0502, 0.0865] | 0.0794 [0.0587, 0.0872] | 0.0634 -> 0.0756 (moderate MG shift; MG higher) | 0.43 | 0.73 | possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `time_pressure_density` | 0 [0, 0.769] | 0.952 [0, 1.5435] | 0.3367 -> 1.1658 (moderate MG shift; MG higher) | 0.70 | 0.73 | variance higher in MG (SD ratio 3.2237); possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `ttr` | 0.7108 [0.6334, 0.8073] | 0.7253 [0.7136, 0.7379] | 0.7215 -> 0.7255 (essentially overlapping location; MG higher) | 0.05 | 0.45 | variance lower in MG (SD ratio 0.2453); possible multimodality (peaks HW/MG 4/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `urgency_density` | 0 [0, 1.297] | 1.98 [0.5, 2.6745] | 0.8109 -> 1.7685 (moderate MG shift; MG higher) | 0.65 | 0.64 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `verb_ratio` | 0.0945 [0.0909, 0.1152] | 0.1146 [0.106, 0.1175] | 0.1044 -> 0.1167 (moderate MG shift; MG higher) | 0.56 | 0.82 | variance lower in MG (SD ratio 0.5653); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 1/2 |
| `yules_k` | 101.351 [80.054, 121.7785] | 108.407 [92.9225, 142.683] | 103.1846 -> 112.8798 (small MG shift; MG higher) | 0.27 | 0.64 | possible multimodality (peaks HW/MG 3/2; tentative at n=11) |

Constant-valued metrics and metrics missing from either class are omitted.

### HW-B vs MG-B

| Feature | HW median [Q1, Q3] | MG median [Q1, Q3] | Mean HW → MG | Effect | OVL | Shape notes |
|---|---:|---:|---:|---:|---:|---|
| `authority_density` | 0 [0, 0] | 0 [0, 1.2055] | 0.1684 -> 0.5706 (moderate MG shift; MG higher) | 0.70 | 0.64 | variance higher in MG (SD ratio 1.8266); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `clause_density` | 1.875 [1.528, 2.1715] | 1.571 [1.429, 1.9285] | 2.0413 -> 1.7149 (moderate MG shift; MG lower) | -0.48 | 0.91 | variance lower in MG (SD ratio 0.492); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `cta_density` | 1.282 [1.008, 1.6015] | 1.176 [0.4385, 3.9565] | 1.2034 -> 2.3254 (moderate MG shift; MG higher) | 0.63 | 0.45 | variance higher in MG (SD ratio 3.2332); possible multimodality (peaks HW/MG 2/3; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `first_person_ratio` | 0.0217 [0.0121, 0.0421] | 0.0435 [0.0275, 0.0483] | 0.0254 -> 0.0378 (moderate MG shift; MG higher) | 0.71 | 0.64 | possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `imperative_count` | 0 [0, 0] | 0 [0, 0.5] | 0.2727 -> 0.2727 (essentially overlapping location; MG same) | 0.00 | 0.82 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `mean_parse_depth` | 2.268 [2.066, 2.942] | 2.387 [2.2085, 2.711] | 2.5978 -> 2.4745 (small MG shift; MG lower) | -0.20 | 0.73 | variance lower in MG (SD ratio 0.5527); possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `mean_sentence_len_tokens` | 18 [15.927, 18.5] | 15.143 [14.143, 16.866] | 18.8214 -> 15.4887 (moderate MG shift; MG lower) | -0.77 | 0.55 | variance lower in MG (SD ratio 0.4506); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `mean_word_len` | 4.744 [4.6545, 4.8055] | 5.356 [5.207, 5.642] | 4.7237 -> 5.4033 (clear MG shift; MG higher) | 1.57 | 0.18 | possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 3/0 |
| `noun_ratio` | 0.1905 [0.1481, 0.2094] | 0.2037 [0.1844, 0.2214] | 0.1812 -> 0.2075 (moderate MG shift; MG higher) | 0.64 | 0.55 | variance lower in MG (SD ratio 0.5991); possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `politeness_density` | 0.935 [0.8415, 2.5485] | 2.299 [1.364, 3.123] | 1.8774 -> 2.3058 (small MG shift; MG higher) | 0.30 | 0.36 | variance lower in MG (SD ratio 0.5714); possible multimodality (peaks HW/MG 3/3; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `second_person_ratio` | 0.0093 [0.0075, 0.0237] | 0.0345 [0.0312, 0.0382] | 0.0166 -> 0.0324 (clear MG shift; MG higher) | 0.98 | 0.45 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/2 |
| `time_pressure_density` | 0 [0, 0] | 0 [0, 1.06] | 0.2518 -> 0.5218 (moderate MG shift; MG higher) | 0.44 | 0.73 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `ttr` | 0.6374 [0.6132, 0.7434] | 0.7667 [0.7478, 0.7925] | 0.6855 -> 0.7725 (clear MG shift; MG higher) | 1.03 | 0.45 | variance lower in MG (SD ratio 0.403); possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `urgency_density` | 0 [0, 0.926] | 0 [0, 0.982] | 0.497 -> 0.4969 (essentially overlapping location; MG lower) | -0.00 | 0.73 | possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `verb_ratio` | 0.0955 [0.0844, 0.1236] | 0.1111 [0.1032, 0.124] | 0.1046 -> 0.1123 (small MG shift; MG higher) | 0.33 | 0.45 | variance lower in MG (SD ratio 0.3994); possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `yules_k` | 110.345 [92.7445, 139.2045] | 70.111 [58.777, 85.224] | 110.6552 -> 70.3595 (clear MG shift; MG lower) | -1.18 | 0.36 | variance lower in MG (SD ratio 0.455); possible multimodality (peaks HW/MG 2/4; tentative at n=11) |

Constant-valued metrics and metrics missing from either class are omitted.

## Stylometric

Source: `Stylometric\results\matched_pool_44_stylometric_metrics.json`

### HW-P vs MG-P

| Feature | HW median [Q1, Q3] | MG median [Q1, Q3] | Mean HW → MG | Effect | OVL | Shape notes |
|---|---:|---:|---:|---:|---:|---|
| `character_2gram_count` | 637 [503.5, 815] | 618 [568, 692.5] | 662.4545 -> 617.7273 (small MG shift; MG lower) | -0.27 | 0.64 | variance lower in MG (SD ratio 0.4362); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `character_2gram_unique` | 254 [212.5, 267] | 234 [220.5, 241] | 244.4545 -> 227.2727 (moderate MG shift; MG lower) | -0.50 | 0.64 | variance lower in MG (SD ratio 0.4149); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `character_3gram_count` | 636 [502.5, 814] | 617 [567, 691.5] | 661.4545 -> 616.7273 (small MG shift; MG lower) | -0.27 | 0.64 | variance lower in MG (SD ratio 0.4362); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `character_3gram_unique` | 434 [365.5, 474.5] | 423 [395.5, 457.5] | 428.6364 -> 419.7273 (essentially overlapping location; MG lower) | -0.11 | 0.73 | variance lower in MG (SD ratio 0.559); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `character_4gram_count` | 635 [501.5, 813] | 616 [566, 690.5] | 660.4545 -> 615.7273 (small MG shift; MG lower) | -0.27 | 0.64 | variance lower in MG (SD ratio 0.4362); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `character_4gram_unique` | 509 [418.5, 563.5] | 493 [463, 552.5] | 506.5455 -> 495.5455 (essentially overlapping location; MG lower) | -0.10 | 0.73 | variance lower in MG (SD ratio 0.5677); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `lda_active_topic_count` | 1 [1, 2] | 1 [1, 1] | 1.4545 -> 1.0909 (moderate MG shift; MG lower) | -0.66 | 0.73 | variance lower in MG (SD ratio 0.4385); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `lda_assignment_topic_0` | 0.1056 [0.0871, 0.2166] | 0.0469 [0.0267, 0.0851] | 0.1899 -> 0.0564 (clear MG shift; MG lower) | -0.90 | 0.73 | variance lower in MG (SD ratio 0.1819); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `lda_assignment_topic_1` | 0.0606 [0.038, 0.0988] | 0.0471 [0.0356, 0.0572] | 0.1288 -> 0.044 (moderate MG shift; MG lower) | -0.66 | 0.73 | variance lower in MG (SD ratio 0.1193); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 2/1 |
| `lda_assignment_topic_2` | 0.0116 [0.0083, 0.039] | 0.01 [0, 0.0137] | 0.0477 -> 0.0249 (small MG shift; MG lower) | -0.36 | 0.82 | skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 2/1 |
| `lda_assignment_topic_3` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `lda_assignment_topic_4` | 0.686 [0.5029, 0.7812] | 0.8857 [0.8525, 0.9221] | 0.6337 -> 0.8747 (clear MG shift; MG higher) | 1.22 | 0.18 | variance lower in MG (SD ratio 0.4142); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `lda_dominant_topic_mass` | 0.9888 [0.6152, 0.9919] | 0.9913 [0.9899, 0.992] | 0.8413 -> 0.9551 (moderate MG shift; MG higher) | 0.65 | 0.73 | variance lower in MG (SD ratio 0.5689); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `lda_per_token_likelihood_bound` | -33.1224 [-34.6053, -26.5562] | -30.3896 [-32.711, -29.0028] | -32.4709 -> -31.8626 (essentially overlapping location; MG higher) | 0.09 | 0.64 | variance lower in MG (SD ratio 0.5152); Tukey outliers HW/MG 1/1 |
| `lda_topic_0` | 0.0023 [0.0017, 0.2266] | 0.0021 [0.002, 0.0023] | 0.186 -> 0.0022 (moderate MG shift; MG lower) | -0.73 | 0.73 | variance lower in MG (SD ratio 0.0012); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 2/1 |
| `lda_topic_1` | 0.0021 [0.0017, 0.003] | 0.0021 [0.002, 0.0023] | 0.1817 -> 0.0022 (moderate MG shift; MG lower) | -0.62 | 0.82 | variance lower in MG (SD ratio 0.00098); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 2/1 |
| `lda_topic_2` | 0.0023 [0.002, 0.032] | 0.0022 [0.002, 0.0025] | 0.0802 -> 0.0383 (small MG shift; MG lower) | -0.30 | 0.91 | skew changes (more right-skewed in MG); Tukey outliers HW/MG 2/1 |
| `lda_topic_3` | 0.0021 [0.0017, 0.0023] | 0.0021 [0.002, 0.0023] | 0.0021 -> 0.0022 (essentially overlapping location; MG higher) | 0.10 | 0.55 | variance lower in MG (SD ratio 0.5964); possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 1/2 |
| `lda_topic_4` | 0.5445 [0.1749, 0.9889] | 0.9913 [0.9899, 0.992] | 0.55 -> 0.9551 (clear MG shift; MG higher) | 1.11 | 0.45 | variance lower in MG (SD ratio 0.2864); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `lda_topic_entropy` | 0.0767 [0.0583, 0.7029] | 0.0618 [0.0575, 0.0706] | 0.3145 -> 0.1223 (moderate MG shift; MG lower) | -0.65 | 0.73 | variance lower in MG (SD ratio 0.5533); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `pos_adjectives` | 6 [5, 7] | 5 [5, 8] | 6.1818 -> 6.2727 (essentially overlapping location; MG higher) | 0.04 | 0.91 | possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `pos_adverbs` | 4 [1, 4.5] | 2 [2, 3] | 3.5455 -> 2.7273 (small MG shift; MG lower) | -0.39 | 0.27 | variance lower in MG (SD ratio 0.602); possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 0/2 |
| `pos_cardinal_numbers` | 0 [0, 0.5] | 0 [0, 1] | 0.3636 -> 0.3636 (essentially overlapping location; MG same) | 0.00 | 0.82 | possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `pos_conjunctions` | 2 [1, 3.5] | 2 [1, 2] | 2.3636 -> 1.7273 (moderate MG shift; MG lower) | -0.44 | 0.64 | variance lower in MG (SD ratio 0.3383); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `pos_density_1` | 18.6047 [15.1727, 22.5036] | 18.9474 [18.0632, 21.2302] | 19.0823 -> 20.3588 (small MG shift; MG higher) | 0.26 | 0.36 | variance lower in MG (SD ratio 0.5528); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `pos_density_2` | 55.8824 [53.256, 59.2857] | 57 [55.0055, 60.1303] | 58.334 -> 57.8448 (essentially overlapping location; MG lower) | -0.08 | 0.82 | variance lower in MG (SD ratio 0.5154); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `pos_density_3` | 82.069 [78.3425, 84.1022] | 80.4124 [78.7968, 83.2845] | 81.8 -> 81.8039 (essentially overlapping location; MG higher) | 0.00 | 0.55 | possible multimodality (peaks HW/MG 2/3; tentative at n=11); Tukey outliers HW/MG 1/1 |
| `pos_determiners` | 4 [4, 5.5] | 5 [4, 5.5] | 4.9091 -> 4.9091 (essentially overlapping location; MG same) | 0.00 | 0.73 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 2/3 |
| `pos_foreign_words` | 0 [0, 0] | 0 [0, 0] | 0 -> 0.0909 (moderate MG shift; MG higher) | 0.43 | 0.91 | variance higher in MG (SD ratio NA); skew changes (more right-skewed in MG); Tukey outliers HW/MG 0/1 |
| `pos_interrogatives` | 0 [0, 0] | 0 [0, 1] | 0.1818 -> 0.3636 (small MG shift; MG higher) | 0.33 | 0.64 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `pos_nouns` | 44 [33, 51] | 42 [37, 43.5] | 41.7273 -> 39.9091 (essentially overlapping location; MG lower) | -0.18 | 0.64 | variance lower in MG (SD ratio 0.5189); possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `pos_particles` | 0 [0, 0] | 0 [0, 0] | 0 -> 0.2727 (moderate MG shift; MG higher) | 0.58 | 0.82 | variance higher in MG (SD ratio NA); skew changes (more right-skewed in MG); Tukey outliers HW/MG 0/2 |
| `pos_possessive_pronouns` | 5 [3, 7] | 6 [5.5, 7.5] | 5.0909 -> 6.3636 (moderate MG shift; MG higher) | 0.46 | 0.55 | variance lower in MG (SD ratio 0.3284); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `pos_prepositions` | 11 [10.5, 13.5] | 12 [11, 12.5] | 11.4545 -> 11.1818 (essentially overlapping location; MG lower) | -0.07 | 0.55 | variance lower in MG (SD ratio 0.3841); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 3/2 |
| `pos_symbols` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `pos_verbs` | 15 [10, 16.5] | 13 [12, 15] | 14.9091 -> 13.5455 (small MG shift; MG lower) | -0.33 | 0.36 | variance lower in MG (SD ratio 0.5486); possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `sentence_mean_sentence_length` | 84.2857 [74.7083, 92.4] | 121.4 [113, 123] | 82.2602 -> 119.04 (clear MG shift; MG higher) | 1.50 | 0.09 | variance lower in MG (SD ratio 0.4728); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 2/1 |
| `sentence_variance_of_sentence_length` | 2.52e+03 [1.71e+03, 3.11e+03] | 2.8e+03 [2.27e+03, 4.37e+03] | 2.79e+03 -> 3.36e+03 (small MG shift; MG higher) | 0.35 | 0.82 | possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `surface_character_count` | 638 [504.5, 816] | 619 [569, 693.5] | 663.4545 -> 618.7273 (small MG shift; MG lower) | -0.27 | 0.64 | variance lower in MG (SD ratio 0.4362); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `surface_character_count_without_spaces` | 550 [421, 702] | 525 [483, 593] | 566.1818 -> 527.2727 (small MG shift; MG lower) | -0.26 | 0.64 | variance lower in MG (SD ratio 0.4297); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `surface_comma_percentage` | 0.4474 [0.3074, 0.5369] | 0.6085 [0.5374, 0.6927] | 0.3883 -> 0.6175 (clear MG shift; MG higher) | 1.13 | 0.45 | variance lower in MG (SD ratio 0.4556); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `surface_digit_count` | 0 [0, 1.5] | 0 [0, 2] | 1.0909 -> 0.8182 (essentially overlapping location; MG lower) | -0.18 | 0.82 | variance lower in MG (SD ratio 0.6078); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `surface_digit_ratio` | 0 [0, 0.3115] | 0 [0, 0.2884] | 0.1536 -> 0.1363 (essentially overlapping location; MG lower) | -0.08 | 0.91 | possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `surface_letter_ratio` | 80.9843 [79.4737, 81.4948] | 82.4201 [81.9916, 82.7433] | 80.5052 -> 82.4114 (clear MG shift; MG higher) | 1.29 | 0.36 | variance lower in MG (SD ratio 0.385); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `surface_punctuation_percentage` | 1.7647 [1.5449, 2.02] | 1.6371 [1.5995, 1.7444] | 1.8148 -> 1.6499 (moderate MG shift; MG lower) | -0.53 | 0.45 | variance lower in MG (SD ratio 0.2986); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `surface_question_sentence_percentage` | 0 [0, 0] | 0 [0, 0] | 3.2828 -> 0 (moderate MG shift; MG lower) | -0.57 | 0.82 | variance lower in MG (SD ratio 0); skew changes (less right-skewed in MG); Tukey outliers HW/MG 2/0 |
| `surface_semicolon_percentage` | 0 [0, 0] | 0 [0, 0] | 0.0173 -> 0 (moderate MG shift; MG lower) | -0.43 | 0.91 | variance lower in MG (SD ratio 0); skew changes (less right-skewed in MG); Tukey outliers HW/MG 1/0 |
| `surface_space_count` | 88 [81.5, 118] | 94 [86, 100.5] | 97.2727 -> 91.4545 (small MG shift; MG lower) | -0.26 | 0.45 | variance lower in MG (SD ratio 0.4816); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `surface_special_character_ratio` | 19.0157 [18.5052, 20.2684] | 17.2859 [17.17, 17.7759] | 19.3412 -> 17.4523 (clear MG shift; MG lower) | -1.34 | 0.18 | variance lower in MG (SD ratio 0.4044); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `surface_tab_count` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `surface_tab_ratio` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `surface_uppercase_count` | 75 [45.5, 109.5] | 25 [22.5, 30.5] | 80.1818 -> 26.2727 (clear MG shift; MG lower) | -1.25 | 0.36 | variance lower in MG (SD ratio 0.1278); possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `surface_uppercase_ratio` | 10.1881 [9.2678, 13.2617] | 4.1096 [4.0748, 4.6579] | 11.343 -> 4.2375 (clear MG shift; MG lower) | -1.53 | 0.09 | variance lower in MG (SD ratio 0.1551); possible multimodality (peaks HW/MG 3/3; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `surface_whitespace_ratio` | 14.4273 [13.8309, 15.559] | 14.8073 [14.4228, 15.0597] | 14.884 -> 14.7906 (essentially overlapping location; MG lower) | -0.10 | 0.45 | variance lower in MG (SD ratio 0.376); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `syntactic_apostrophe` | 1 [0, 1.5] | 0 [0, 0] | 1 -> 0.0909 (clear MG shift; MG lower) | -0.94 | 0.55 | variance lower in MG (SD ratio 0.2548); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `syntactic_brackets` | 12 [7, 15] | 4 [4, 6] | 12.3636 -> 5.0909 (clear MG shift; MG lower) | -1.15 | 0.36 | variance lower in MG (SD ratio 0.2595); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `syntactic_colon` | 1 [0, 2] | 2 [2, 2] | 1.2727 -> 2 (moderate MG shift; MG higher) | 0.64 | 0.36 | variance lower in MG (SD ratio 0.3003); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/2 |
| `syntactic_comma` | 3 [2, 3.5] | 4 [3, 4.5] | 2.6364 -> 3.8182 (clear MG shift; MG higher) | 0.86 | 0.64 | variance lower in MG (SD ratio 0.5578); possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `syntactic_dash` | 1 [1, 2] | 0 [0, 0.5] | 2.1818 -> 0.4545 (moderate MG shift; MG lower) | -0.71 | 0.91 | variance lower in MG (SD ratio 0.299); Tukey outliers HW/MG 2/1 |
| `syntactic_ellipsis` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `syntactic_exclamation` | 0 [0, 1] | 0 [0, 0] | 0.6364 -> 0 (clear MG shift; MG lower) | -0.89 | 0.55 | variance lower in MG (SD ratio 0); skew changes (less right-skewed in MG); Tukey outliers HW/MG 1/0 |
| `syntactic_full_stop` | 7 [5.5, 9] | 4 [4, 5] | 7.2727 -> 4.3636 (clear MG shift; MG lower) | -1.19 | 0.36 | variance lower in MG (SD ratio 0.3489); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `syntactic_question_mark` | 0 [0, 0] | 0 [0, 0] | 0.1818 -> 0 (moderate MG shift; MG lower) | -0.62 | 0.82 | variance lower in MG (SD ratio 0); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `syntactic_semicolon` | 0 [0, 0] | 0 [0, 0] | 0.0909 -> 0 (moderate MG shift; MG lower) | -0.43 | 0.91 | variance lower in MG (SD ratio 0); skew changes (less right-skewed in MG); Tukey outliers HW/MG 1/0 |
| `syntactic_slash` | 0 [0, 0] | 0 [0, 0] | 0.2727 -> 0.0909 (small MG shift; MG lower) | -0.27 | 0.91 | variance lower in MG (SD ratio 0.3333); Tukey outliers HW/MG 1/1 |
| `vocabulary_average_sentence_length_characters` | 84.2857 [74.7083, 92.4] | 121.4 [113, 123] | 82.2602 -> 119.04 (clear MG shift; MG higher) | 1.50 | 0.09 | variance lower in MG (SD ratio 0.4728); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 2/1 |
| `vocabulary_average_sentence_length_words` | 12 [11.2222, 14.45] | 18.25 [16.9, 18.8333] | 12.4803 -> 17.9249 (clear MG shift; MG higher) | 1.46 | 0.27 | variance lower in MG (SD ratio 0.5068); possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `vocabulary_average_word_length` | 6.8788 [6.3146, 7.1318] | 6.75 [6.5749, 6.8042] | 6.6944 -> 6.6938 (essentially overlapping location; MG lower) | -0.00 | 0.55 | variance lower in MG (SD ratio 0.4094); possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `vocabulary_brunet_w` | 9.4411 [8.8804, 9.9044] | 9.2759 [9.1918, 9.3234] | 9.3934 -> 9.21 (small MG shift; MG lower) | -0.35 | 0.36 | variance lower in MG (SD ratio 0.3705); possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 0/3 |
| `vocabulary_hapax_legomena` | 64 [51.5, 70] | 63 [56, 66.5] | 60.5455 -> 61.4545 (essentially overlapping location; MG higher) | 0.09 | 0.73 | variance lower in MG (SD ratio 0.5709); possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `vocabulary_honore_r` | 2.75e+03 [2.33e+03, 3.19e+03] | 2.85e+03 [2.54e+03, 3.33e+03] | 2.99e+03 -> 2.97e+03 (essentially overlapping location; MG lower) | -0.03 | 0.82 | variance lower in MG (SD ratio 0.5884); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `vocabulary_ratio_short_words` | 29.7619 [27.1195, 31.4878] | 27.8846 [22.8795, 29.508] | 30.477 -> 26.5591 (moderate MG shift; MG lower) | -0.76 | 0.64 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/4; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `vocabulary_sichel_s` | 0.093 [0.0716, 0.1068] | 0.1268 [0.0822, 0.1426] | 0.0986 -> 0.1192 (moderate MG shift; MG higher) | 0.46 | 0.64 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `vocabulary_simpson_d` | 0.0083 [0.0056, 0.0095] | 0.0081 [0.0061, 0.0103] | 0.0083 -> 0.008 (essentially overlapping location; MG lower) | -0.09 | 0.36 | possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `vocabulary_total_unique_words` | 77 [61.5, 82] | 75 [68, 82] | 73.6364 -> 73.6364 (essentially overlapping location; MG same) | 0.00 | 0.73 | variance lower in MG (SD ratio 0.6547); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `vocabulary_total_words` | 89 [84, 117] | 95 [87.5, 101.5] | 98.0909 -> 92.4545 (small MG shift; MG lower) | -0.25 | 0.45 | variance lower in MG (SD ratio 0.4917); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `vocabulary_yule_k` | 4.11e+03 [3.44e+03, 5.66e+03] | 4.76e+03 [4.63e+03, 5.27e+03] | 4.56e+03 -> 4.91e+03 (small MG shift; MG higher) | 0.34 | 0.36 | variance lower in MG (SD ratio 0.3319); possible multimodality (peaks HW/MG 3/2; tentative at n=11) |

Constant-valued metrics and metrics missing from either class are omitted.

### HW-B vs MG-B

| Feature | HW median [Q1, Q3] | MG median [Q1, Q3] | Mean HW → MG | Effect | OVL | Shape notes |
|---|---:|---:|---:|---:|---:|---|
| `character_2gram_count` | 665 [587, 727.5] | 613 [581.5, 658.5] | 681.8182 -> 612.2727 (moderate MG shift; MG lower) | -0.60 | 0.64 | variance lower in MG (SD ratio 0.6096); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `character_2gram_unique` | 270 [240, 278] | 239 [231, 256.5] | 262.7273 -> 241.1818 (clear MG shift; MG lower) | -0.81 | 0.45 | variance lower in MG (SD ratio 0.5202); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `character_3gram_count` | 664 [586, 726.5] | 612 [580.5, 657.5] | 680.8182 -> 611.2727 (moderate MG shift; MG lower) | -0.60 | 0.64 | variance lower in MG (SD ratio 0.6096); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `character_3gram_unique` | 438 [378.5, 506] | 448 [423.5, 473] | 443.4545 -> 440.9091 (essentially overlapping location; MG lower) | -0.05 | 0.55 | possible multimodality (peaks HW/MG 3/4; tentative at n=11) |
| `character_4gram_count` | 663 [585, 725.5] | 611 [579.5, 656.5] | 679.8182 -> 610.2727 (moderate MG shift; MG lower) | -0.60 | 0.64 | variance lower in MG (SD ratio 0.6096); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `character_4gram_unique` | 515 [457, 600.5] | 514 [497.5, 559.5] | 519.9091 -> 517.6364 (essentially overlapping location; MG lower) | -0.03 | 0.73 | possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `lda_active_topic_count` | 1 [1, 1] | 1 [1, 1] | 1.1818 -> 1.0909 (essentially overlapping location; MG lower) | -0.19 | 0.91 | variance lower in MG (SD ratio 0.5); Tukey outliers HW/MG 1/1 |
| `lda_assignment_topic_0` | 0.1261 [0.0867, 0.5924] | 0.1277 [0.1033, 0.3064] | 0.3223 -> 0.2057 (moderate MG shift; MG lower) | -0.51 | 0.55 | variance lower in MG (SD ratio 0.6281); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `lda_assignment_topic_1` | 0.1333 [0.0476, 0.3707] | 0.1393 [0.0949, 0.4653] | 0.2171 -> 0.2788 (small MG shift; MG higher) | 0.28 | 0.82 | possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `lda_assignment_topic_2` | 0.0375 [0.0176, 0.0549] | 0.0213 [0.0102, 0.0613] | 0.0733 -> 0.0932 (essentially overlapping location; MG higher) | 0.14 | 0.91 | skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/2 |
| `lda_assignment_topic_3` | 0 [0, 0] | 0 [0, 0] | 0.0352 -> 0 (moderate MG shift; MG lower) | -0.43 | 0.91 | variance lower in MG (SD ratio 0); skew changes (less right-skewed in MG); Tukey outliers HW/MG 1/0 |
| `lda_assignment_topic_4` | 0.3125 [0.292, 0.34] | 0.404 [0.392, 0.4302] | 0.3521 -> 0.4223 (moderate MG shift; MG higher) | 0.56 | 0.27 | skew changes (less right-skewed in MG); Tukey outliers HW/MG 1/2 |
| `lda_dominant_topic_mass` | 0.9928 [0.9912, 0.9934] | 0.9913 [0.9906, 0.9916] | 0.9511 -> 0.9725 (small MG shift; MG higher) | 0.20 | 0.91 | variance lower in MG (SD ratio 0.4516); Tukey outliers HW/MG 1/2 |
| `lda_per_token_likelihood_bound` | -27.1009 [-31.8792, -25.715] | -32.0755 [-33.5157, -30.6125] | -28.1384 -> -32.2211 (clear MG shift; MG lower) | -0.85 | 0.64 | possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 0/2 |
| `lda_topic_0` | 0.2357 [0.002, 0.9921] | 0.0022 [0.0022, 0.3939] | 0.4735 -> 0.253 (moderate MG shift; MG lower) | -0.47 | 0.64 | possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 0/2 |
| `lda_topic_1` | 0.0022 [0.0018, 0.4961] | 0.2096 [0.0022, 0.991] | 0.2721 -> 0.4708 (moderate MG shift; MG higher) | 0.41 | 0.73 | possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `lda_topic_2` | 0.0021 [0.0017, 0.0024] | 0.0021 [0.002, 0.0027] | 0.1122 -> 0.182 (small MG shift; MG higher) | 0.20 | 0.91 | possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 2/2 |
| `lda_topic_3` | 0.0018 [0.0016, 0.0022] | 0.0021 [0.002, 0.0022] | 0.0505 -> 0.0021 (moderate MG shift; MG lower) | -0.42 | 0.91 | variance lower in MG (SD ratio 0.0021); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/1 |
| `lda_topic_4` | 0.0018 [0.0017, 0.0022] | 0.0022 [0.002, 0.0024] | 0.0918 -> 0.0921 (essentially overlapping location; MG higher) | 0.00 | 1.00 | Tukey outliers HW/MG 1/2 |
| `lda_topic_entropy` | 0.0525 [0.0488, 0.0629] | 0.0622 [0.0598, 0.0664] | 0.1431 -> 0.1067 (essentially overlapping location; MG lower) | -0.16 | 0.91 | variance lower in MG (SD ratio 0.4973); Tukey outliers HW/MG 1/2 |
| `pos_adjectives` | 5 [4, 7.5] | 7 [4.5, 8.5] | 5.9091 -> 6.4545 (small MG shift; MG higher) | 0.22 | 0.73 | possible multimodality (peaks HW/MG 3/2; tentative at n=11) |
| `pos_adverbs` | 3 [2.5, 5] | 1 [1, 2] | 3.6364 -> 1.2727 (clear MG shift; MG lower) | -1.22 | 0.36 | variance lower in MG (SD ratio 0.4492); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `pos_cardinal_numbers` | 0 [0, 0] | 1 [0, 3] | 0.2727 -> 1.6364 (clear MG shift; MG higher) | 0.95 | 0.55 | variance higher in MG (SD ratio 2.6127); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `pos_conjunctions` | 3 [2, 3.5] | 2 [1, 3] | 2.8182 -> 2 (moderate MG shift; MG lower) | -0.53 | 0.64 | possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `pos_density_1` | 17.1171 [16.2388, 18.655] | 20 [18.7219, 22.4014] | 17.4642 -> 20.5431 (clear MG shift; MG higher) | 0.95 | 0.55 | possible multimodality (peaks HW/MG 2/3; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `pos_density_2` | 57.3034 [53.4722, 59.3937] | 59.3407 [58.7787, 63.8256] | 56.2116 -> 61.4774 (clear MG shift; MG higher) | 0.84 | 0.64 | variance lower in MG (SD ratio 0.6501); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `pos_density_3` | 80.7339 [78.412, 84.9026] | 84.6154 [84.2677, 89.3182] | 80.1082 -> 86.1623 (clear MG shift; MG higher) | 0.82 | 0.73 | variance lower in MG (SD ratio 0.3543); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `pos_determiners` | 9 [8.5, 11] | 7 [5.5, 9] | 9.4545 -> 7.1818 (moderate MG shift; MG lower) | -0.75 | 0.55 | possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `pos_foreign_words` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `pos_interrogatives` | 1 [0, 2.5] | 0 [0, 1] | 1.3636 -> 0.7273 (moderate MG shift; MG lower) | -0.47 | 0.64 | skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `pos_nouns` | 41 [37.5, 52] | 39 [37, 41.5] | 44.3636 -> 38.5455 (moderate MG shift; MG lower) | -0.68 | 0.64 | variance lower in MG (SD ratio 0.3809); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `pos_particles` | 0 [0, 1.5] | 1 [0, 1] | 0.8182 -> 0.7273 (essentially overlapping location; MG lower) | -0.10 | 0.64 | variance lower in MG (SD ratio 0.5995); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `pos_possessive_pronouns` | 1 [0, 1] | 3 [2.5, 4] | 0.8182 -> 3.5455 (clear MG shift; MG higher) | 1.42 | 0.09 | possible multimodality (peaks HW/MG 2/3; tentative at n=11); Tukey outliers HW/MG 1/1 |
| `pos_prepositions` | 13 [13, 15.5] | 13 [9, 14] | 14.4545 -> 11.9091 (moderate MG shift; MG lower) | -0.74 | 0.64 | possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `pos_symbols` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `pos_verbs` | 17 [13.5, 24.5] | 14 [12, 14.5] | 19 -> 14.5455 (moderate MG shift; MG lower) | -0.75 | 0.45 | variance lower in MG (SD ratio 0.5726); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 0/2 |
| `sentence_mean_sentence_length` | 130.5714 [96.4286, 139.125] | 91.25 [84.1429, 99.3333] | 125.6333 -> 90.8245 (clear MG shift; MG lower) | -0.93 | 0.64 | variance lower in MG (SD ratio 0.3151); skew changes (less right-skewed in MG); Tukey outliers HW/MG 1/1 |
| `sentence_variance_of_sentence_length` | 6.45e+03 [2.13e+03, 8.94e+03] | 2.2e+03 [1.94e+03, 2.89e+03] | 7.32e+03 -> 2.67e+03 (clear MG shift; MG lower) | -0.91 | 0.55 | variance lower in MG (SD ratio 0.1993); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 1/1 |
| `surface_character_count` | 666 [588, 728.5] | 614 [582.5, 659.5] | 682.8182 -> 613.2727 (moderate MG shift; MG lower) | -0.60 | 0.64 | variance lower in MG (SD ratio 0.6096); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `surface_character_count_without_spaces` | 556 [498, 614] | 522 [497.5, 563.5] | 572 -> 521.5455 (moderate MG shift; MG lower) | -0.52 | 0.64 | variance lower in MG (SD ratio 0.6024); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `surface_comma_percentage` | 0.3328 [0.2745, 0.4308] | 0.7289 [0.6552, 0.8254] | 0.4257 -> 0.7327 (clear MG shift; MG higher) | 1.15 | 0.36 | variance lower in MG (SD ratio 0.5726); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `surface_digit_count` | 0 [0, 1] | 2 [0, 6.5] | 0.4545 -> 3.0909 (clear MG shift; MG higher) | 0.91 | 0.55 | variance higher in MG (SD ratio 5.3024); possible multimodality (peaks HW/MG 2/3; tentative at n=11) |
| `surface_digit_ratio` | 0 [0, 0.1462] | 0.316 [0, 0.9752] | 0.0615 -> 0.5192 (clear MG shift; MG higher) | 0.92 | 0.55 | variance higher in MG (SD ratio 7.2618); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `surface_letter_ratio` | 77.6276 [77.1121, 78.3749] | 82.0847 [80.4238, 83.2231] | 77.9379 -> 81.5728 (clear MG shift; MG higher) | 1.47 | 0.27 | variance higher in MG (SD ratio 1.544); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `surface_punctuation_percentage` | 1.6529 [1.2743, 2.0484] | 1.7915 [1.6788, 2.1795] | 1.6604 -> 2.0093 (moderate MG shift; MG higher) | 0.74 | 0.45 | possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `surface_question_sentence_percentage` | 0 [0, 16.6667] | 0 [0, 0] | 7.1212 -> 1.5152 (moderate MG shift; MG lower) | -0.68 | 0.73 | variance lower in MG (SD ratio 0.4969); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `surface_semicolon_percentage` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `surface_space_count` | 110 [93, 119.5] | 91 [85, 96] | 110.8182 -> 91.7273 (clear MG shift; MG lower) | -0.95 | 0.64 | variance lower in MG (SD ratio 0.6646); possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 0/2 |
| `surface_special_character_ratio` | 22.0588 [21.2821, 22.375] | 17.8423 [16.7131, 18.5372] | 21.7872 -> 17.908 (clear MG shift; MG lower) | -1.64 | 0.18 | skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `surface_tab_count` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `surface_tab_ratio` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `surface_uppercase_count` | 92 [73.5, 129.5] | 25 [22.5, 28.5] | 105.7273 -> 26.2727 (clear MG shift; MG lower) | -1.38 | 0.27 | variance lower in MG (SD ratio 0.0861); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `surface_uppercase_ratio` | 14.3639 [11.3593, 19.9535] | 4.3403 [3.6993, 4.7709] | 15.4326 -> 4.3362 (clear MG shift; MG lower) | -1.46 | 0.18 | variance lower in MG (SD ratio 0.1211); possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `surface_whitespace_ratio` | 15.9783 [15.7037, 16.8682] | 14.7708 [14.491, 15.2374] | 16.2771 -> 14.9414 (clear MG shift; MG lower) | -1.30 | 0.36 | possible multimodality (peaks HW/MG 3/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `syntactic_apostrophe` | 0 [0, 2] | 1 [1, 2] | 1.0909 -> 1.5455 (small MG shift; MG higher) | 0.36 | 0.55 | possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `syntactic_brackets` | 22 [12, 28] | 0 [0, 1] | 21.6364 -> 0.7273 (clear MG shift; MG lower) | -1.54 | 0.18 | variance lower in MG (SD ratio 0.1112); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/2; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `syntactic_colon` | 1 [0, 3.5] | 1 [1, 2] | 1.9091 -> 1.6364 (essentially overlapping location; MG lower) | -0.13 | 0.82 | skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `syntactic_comma` | 2 [2, 3.5] | 5 [4, 5] | 3.0909 -> 4.4545 (moderate MG shift; MG higher) | 0.71 | 0.27 | variance lower in MG (SD ratio 0.3849); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `syntactic_dash` | 1 [0.5, 2.5] | 1 [1, 3] | 1.4545 -> 2 (small MG shift; MG higher) | 0.36 | 0.73 | possible multimodality (peaks HW/MG 3/3; tentative at n=11) |
| `syntactic_ellipsis` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `syntactic_exclamation` | 0 [0, 1] | 0 [0, 0] | 0.5455 -> 0.0909 (moderate MG shift; MG lower) | -0.63 | 0.73 | variance lower in MG (SD ratio 0.3227); skew changes (more right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `syntactic_full_stop` | 4 [3.5, 5] | 6 [5, 6.5] | 4.4545 -> 6 (clear MG shift; MG higher) | 0.81 | 0.55 | possible multimodality (peaks HW/MG 1/2; tentative at n=11); Tukey outliers HW/MG 1/1 |
| `syntactic_question_mark` | 0 [0, 1] | 0 [0, 0] | 0.6364 -> 0.0909 (moderate MG shift; MG lower) | -0.60 | 0.73 | variance lower in MG (SD ratio 0.25); Tukey outliers HW/MG 1/1 |
| `syntactic_semicolon` | 0 [0, 0] | 0 [0, 0] | 0 -> 0 (essentially overlapping location; MG same) | 0.00 | 1.00 | no prominent variance/skew/shape change |
| `syntactic_slash` | 0 [0, 0.5] | 0 [0, 0] | 1.7273 -> 0 (moderate MG shift; MG lower) | -0.65 | 0.82 | variance lower in MG (SD ratio 0); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 2/0 |
| `vocabulary_average_sentence_length_characters` | 130.5714 [96.4286, 139.125] | 91.25 [84.1429, 99.3333] | 125.6333 -> 90.8245 (clear MG shift; MG lower) | -0.93 | 0.64 | variance lower in MG (SD ratio 0.3151); skew changes (less right-skewed in MG); Tukey outliers HW/MG 1/1 |
| `vocabulary_average_sentence_length_words` | 20.8571 [16.1429, 22.5] | 15 [12.4286, 15.8482] | 20.6102 -> 14.0096 (clear MG shift; MG lower) | -1.03 | 0.45 | variance lower in MG (SD ratio 0.334); skew changes (less right-skewed in MG); possible multimodality (peaks HW/MG 1/3; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `vocabulary_average_word_length` | 6.2345 [6.0125, 6.351] | 6.6739 [6.3886, 6.7866] | 6.1545 -> 6.5791 (clear MG shift; MG higher) | 1.08 | 0.45 | possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 1/0 |
| `vocabulary_brunet_w` | 9.7153 [9.4913, 10.1612] | 9.0212 [8.9064, 9.1076] | 9.7992 -> 9.0056 (clear MG shift; MG lower) | -1.32 | 0.36 | variance lower in MG (SD ratio 0.5942); possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 0/3 |
| `vocabulary_hapax_legomena` | 57 [51, 64] | 68 [65.5, 72.5] | 60.5455 -> 69.3636 (moderate MG shift; MG higher) | 0.78 | 0.45 | variance lower in MG (SD ratio 0.5745); possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 1/1 |
| `vocabulary_honore_r` | 1.84e+03 [1.72e+03, 2.71e+03] | 3.36e+03 [3.2e+03, 4.27e+03] | 2.35e+03 -> 4.12e+03 (clear MG shift; MG higher) | 1.01 | 0.45 | variance higher in MG (SD ratio 1.5832); Tukey outliers HW/MG 1/1 |
| `vocabulary_ratio_short_words` | 36.036 [34.0972, 39.4444] | 33.3333 [28.6952, 37.5562] | 37.3361 -> 33.6283 (moderate MG shift; MG lower) | -0.69 | 0.55 | variance higher in MG (SD ratio 1.5982); possible multimodality (peaks HW/MG 2/4; tentative at n=11) |
| `vocabulary_sichel_s` | 0.16 [0.1038, 0.178] | 0.102 [0.0607, 0.1149] | 0.1499 -> 0.0904 (clear MG shift; MG lower) | -1.04 | 0.45 | variance lower in MG (SD ratio 0.617); possible multimodality (peaks HW/MG 2/2; tentative at n=11) |
| `vocabulary_simpson_d` | 0.0095 [0.0075, 0.0109] | 0.0042 [0.0036, 0.0055] | 0.0092 -> 0.0043 (clear MG shift; MG lower) | -1.49 | 0.09 | variance lower in MG (SD ratio 0.5194); possible multimodality (peaks HW/MG 3/1; tentative at n=11) |
| `vocabulary_total_unique_words` | 76 [68, 91.5] | 79 [74.5, 83] | 79.0909 -> 79.4545 (essentially overlapping location; MG higher) | 0.03 | 0.64 | possible multimodality (peaks HW/MG 2/3; tentative at n=11); Tukey outliers HW/MG 0/1 |
| `vocabulary_total_words` | 112 [90.5, 121.5] | 92 [87, 97.5] | 111.0909 -> 93.6364 (clear MG shift; MG lower) | -0.85 | 0.64 | possible multimodality (peaks HW/MG 3/2; tentative at n=11); Tukey outliers HW/MG 0/3 |
| `vocabulary_yule_k` | 3.42e+03 [3.11e+03, 4.34e+03] | 5.71e+03 [5.35e+03, 6.19e+03] | 3.89e+03 -> 5.87e+03 (clear MG shift; MG higher) | 1.36 | 0.27 | possible multimodality (peaks HW/MG 2/1; tentative at n=11); Tukey outliers HW/MG 0/1 |

Constant-valued metrics and metrics missing from either class are omitted.

