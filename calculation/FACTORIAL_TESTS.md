# Factorial feature tests

This analysis uses the four result cells HW-P, MG-P, HW-B, and MG-B.
The model is a stratum-adjusted 2x2 linear model with generation, phishing,
and generation x phishing interaction terms. Rows share matching strata but
are not one-to-one document pairs, so paired tests were not used.

Each cell contains 11 observations. Values below are adjusted contrasts
reported as estimate [bootstrap 95% interval], with Benjamini-Hochberg q
values computed separately for each contrast across features. Standard errors
use HC3 heteroskedasticity-robust covariance. Results are exploratory because
the sample is small and the features are correlated.

| Contrast | Meaning |
|---|---|
| G_P | MG-P - HW-P: generation effect in phishing |
| G_B | MG-B - HW-B: generation effect in benign text |
| P_HW | HW-P - HW-B: phishing effect in human text |
| P_MG | MG-P - MG-B: phishing effect in machine text |
| interaction | G_P - G_B = P_MG - P_HW |

## HWT-MGT

Source: `HWT-MGT\results\matched_pool_44_metrics.json`

| Feature | G_P | G_B | P_HW | P_MG | Interaction | Transferability reading |
|---|---:|---:|---:|---:|---:|---|
| `average_log_probability` | 0.5914 [0.3112, 0.8337], q=0.0423 | 0.4019 [-0.021, 0.8231], q=0.2579 | 0.1734 [-0.2768, 0.6257], q=0.9624 | 0.3628 [0.1994, 0.5288], q=0.0481 | 0.1894 [-0.3069, 0.6685], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `detectgpt_discrepancy` | 0.0264 [-0.0294, 0.0817], q=0.579 | -0.0197 [-0.067, 0.0253], q=0.6369 | 0.0234 [-0.0318, 0.0735], q=0.9624 | 0.0695 [0.0188, 0.118], q=0.1583 | 0.0461 [-0.0293, 0.1162], q=0.9481 | generation opposing/unclear; phishing consistent; small/uncertain |
| `detectgpt_normalized_discrepancy` | 0.2156 [-0.3386, 0.864], q=0.5951 | 0.1654 [-0.3238, 0.6121], q=0.6857 | 0.3376 [-0.143, 0.7633], q=0.9624 | 0.3877 [-0.185, 0.9999], q=0.46 | 0.0502 [-0.6827, 0.8339], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `dna_gpt_regeneration_log_probability_difference` | 0.605 [0.3047, 0.8892], q=0.0485 | 0.3176 [-0.2579, 0.9003], q=0.5104 | 0.282 [-0.2782, 0.8276], q=0.9624 | 0.5695 [0.2335, 0.9004], q=0.0568 | 0.2874 [-0.3617, 0.9371], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `fast_detectgpt_analytic` | 0.7003 [0.2519, 1.1655], q=0.0817 | 0.8632 [-0.076, 1.8106], q=0.2579 | 0.306 [-0.4509, 1.1537], q=0.9624 | 0.1431 [-0.4693, 0.8998], q=0.8667 | -0.1629 [-1.2504, 0.914], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `fast_detectgpt_sampling` | 0.1697 [-0.035, 0.3698], q=0.3439 | 0.0873 [-0.2501, 0.4379], q=0.7405 | 0.0371 [-0.2805, 0.39], q=0.9624 | 0.1195 [-0.0789, 0.3341], q=0.5498 | 0.0824 [-0.3091, 0.4796], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `lrr` | 0.1038 [0.0559, 0.1526], q=0.0411 | 0.103 [0.0455, 0.1581], q=0.0818 | 0.0081 [-0.0513, 0.0691], q=0.9624 | 0.009 [-0.031, 0.0514], q=0.8667 | 0.000874 [-0.0677, 0.0692], q=0.9868 | generation consistent; phishing consistent; small/uncertain |
| `mean_log_rank` | -0.4278 [-0.586, -0.2546], q=0.0411 | -0.3353 [-0.6212, -0.0646], q=0.1865 | -0.1016 [-0.4206, 0.2096], q=0.9624 | -0.194 [-0.2942, -0.0891], q=0.0507 | -0.0925 [-0.4133, 0.2373], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `mean_token_rank` | -125.6336 [-197.0665, -50.938], q=0.0926 | -154.2859 [-238.831, -66.1338], q=0.0818 | -25.4435 [-127.7235, 77.8749], q=0.9624 | 3.2088 [-37.9936, 47.1097], q=0.9195 | 28.6523 [-85.8431, 142.8201], q=0.9481 | generation consistent; phishing opposing/unclear; small/uncertain |
| `mle_intrinsic_dimension` | 0.8842 [0.4509, 1.3468], q=0.0468 | 1.3163 [0.6014, 2.0387], q=0.0818 | 0.1032 [-0.7253, 0.8621], q=0.9624 | -0.3289 [-0.6834, 0.035], q=0.3936 | -0.4321 [-1.2715, 0.4518], q=0.9481 | generation consistent; phishing opposing/unclear; small/uncertain |
| `negative_mean_log_rank` | 0.4278 [0.2442, 0.5906], q=0.0411 | 0.3353 [0.0469, 0.6092], q=0.1865 | 0.1016 [-0.1926, 0.3985], q=0.9624 | 0.194 [0.0944, 0.285], q=0.0507 | 0.0925 [-0.2178, 0.4206], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `negative_mean_token_rank` | 125.6336 [52.4998, 197.666], q=0.0926 | 154.2859 [68.9294, 233.3824], q=0.0818 | 25.4435 [-82.1269, 126.9061], q=0.9624 | -3.2088 [-44.4799, 40.8836], q=0.9195 | -28.6523 [-140.064, 96.6298], q=0.9481 | generation consistent; phishing opposing/unclear; small/uncertain |
| `ngram_overlap_ratio` | 0.0809 [0.0458, 0.1168], q=0.0375 | 0.0407 [-0.0094, 0.0869], q=0.3081 | 0.0441 [0.0037, 0.0837], q=0.9624 | 0.0843 [0.0382, 0.1323], q=0.0507 | 0.0402 [-0.0173, 0.1026], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `npr` | 0.0095 [-0.0157, 0.0348], q=0.6182 | -0.0022 [-0.0193, 0.0157], q=0.8828 | 0.0114 [-0.0102, 0.034], q=0.9624 | 0.0231 [0.0013, 0.0453], q=0.2538 | 0.0117 [-0.0193, 0.0433], q=0.9481 | generation opposing/unclear; phishing consistent; small/uncertain |
| `perplexity_from_causal_log_probs` | -25.1743 [-36.9621, -11.8945], q=0.0793 | -21.7294 [-42.1083, -4.546], q=0.1865 | -4.538 [-26.0887, 16.2117], q=0.9624 | -7.9828 [-11.7428, -4.0864], q=0.1818 | -3.4449 [-24.9833, 18.4076], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `perplexity_gpt2_large` | -21.0303 [-31.5942, -9.058], q=0.0793 | -18.9915 [-35.8767, -3.1489], q=0.1865 | -4.2294 [-24.8559, 15.4172], q=0.9624 | -6.2682 [-10.1039, -2.3534], q=0.1818 | -2.0388 [-22.183, 19.6118], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `phd_intrinsic_dimension` | 1.7757 [0.7768, 2.7071], q=0.0411 | 1.9224 [0.7751, 3.0119], q=0.0942 | 0.043 [-1.1223, 1.2253], q=0.9801 | -0.1037 [-1.0926, 0.865], q=0.9195 | -0.1467 [-1.6914, 1.4445], q=0.9481 | generation consistent; phishing opposing/unclear; small/uncertain |
| `predictive_entropy` | -0.4055 [-0.6064, -0.1963], q=0.0667 | -0.1884 [-0.4983, 0.1215], q=0.4784 | -0.0991 [-0.4348, 0.2281], q=0.9624 | -0.3161 [-0.4575, -0.1613], q=0.0507 | -0.217 [-0.5645, 0.1572], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `probability_fraction` | 0.0638 [0.0255, 0.0969], q=0.0667 | 0.0364 [-0.0235, 0.0932], q=0.4653 | 0.0245 [-0.038, 0.0878], q=0.9624 | 0.0519 [0.0284, 0.074], q=0.0357 | 0.0274 [-0.0403, 0.0957], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `rank_100_1000_ratio` | -0.0388 [-0.0579, -0.0233], q=0.0411 | -0.0267 [-0.0429, -0.01], q=0.0942 | -0.0043 [-0.0249, 0.0177], q=0.9624 | -0.0163 [-0.0292, -0.0051], q=0.1818 | -0.0121 [-0.0382, 0.0105], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `rank_10_100_ratio` | -0.0135 [-0.0431, 0.0151], q=0.569 | -0.0058 [-0.0366, 0.026], q=0.8425 | -0.0015 [-0.0338, 0.032], q=0.9801 | -0.0092 [-0.0328, 0.0129], q=0.7717 | -0.0077 [-0.0507, 0.033], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `rank_gt1000_ratio` | -0.0224 [-0.0324, -0.0132], q=0.0423 | -0.0254 [-0.0443, -0.0086], q=0.111 | -0.0059 [-0.0255, 0.0105], q=0.9624 | -0.0029 [-0.0129, 0.0065], q=0.8093 | 0.003 [-0.0166, 0.0243], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `top10_entropy` | -0.0245 [-0.099, 0.0567], q=0.6701 | 0.076 [-0.0308, 0.1785], q=0.3929 | -0.002 [-0.1207, 0.1116], q=0.9801 | -0.1025 [-0.1533, -0.051], q=0.0507 | -0.1005 [-0.2191, 0.0398], q=0.9481 | generation opposing/unclear; phishing consistent; small/uncertain |
| `top10_rank_ratio` | 0.0747 [0.0392, 0.1116], q=0.0511 | 0.058 [0.0086, 0.1051], q=0.2003 | 0.0117 [-0.0449, 0.0666], q=0.9624 | 0.0284 [0.001, 0.0567], q=0.1818 | 0.0167 [-0.0443, 0.0781], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `total_surprisal` | -149.7753 [-205.8039, -92.647], q=0.0076 | -207.7107 [-257.8712, -153.0748], q=4.03e-05 | -100.5285 [-172.5404, -26.1803], q=0.9624 | -42.593 [-72.0702, -12.246], q=0.1818 | 57.9355 [-23.3917, 132.1265], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `uid_diff` | -0.2698 [-0.4555, -0.0749], q=0.1554 | -0.3394 [-0.597, -0.0602], q=0.1865 | -0.0937 [-0.3314, 0.1717], q=0.9624 | -0.0241 [-0.2442, 0.1963], q=0.9195 | 0.0696 [-0.291, 0.4157], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `uid_diff2` | -2.1606 [-3.9586, -0.2558], q=0.2261 | -3.8127 [-6.2408, -1.284], q=0.1145 | -0.914 [-3.0025, 1.1858], q=0.9624 | 0.7381 [-1.5088, 3.027], q=0.8093 | 1.6521 [-1.6627, 4.833], q=0.9481 | generation consistent; phishing opposing/unclear; small/uncertain |
| `uid_mean` | -0.5294 [-0.7945, -0.2422], q=0.0659 | -0.4173 [-0.8315, 0.0581], q=0.2579 | -0.1348 [-0.6287, 0.3327], q=0.9624 | -0.2468 [-0.4216, -0.0559], q=0.1485 | -0.112 [-0.6505, 0.4138], q=0.9481 | generation consistent; phishing consistent; small/uncertain |
| `uid_variance` | -1.0764 [-1.8444, -0.33], q=0.1286 | -1.7217 [-2.7578, -0.6639], q=0.0942 | -0.3791 [-1.2421, 0.5846], q=0.9624 | 0.2661 [-0.6656, 1.1286], q=0.8093 | 0.6453 [-0.6366, 1.9017], q=0.9481 | generation consistent; phishing opposing/unclear; small/uncertain |
| `weighted_ngram_score` | 0.0049 [0.0032, 0.0065], q=0.0159 | 2.94e-05 [-0.0024, 0.0025], q=0.9861 | -0.0017 [-0.0032, -8.59e-05], q=0.9624 | 0.0032 [0.000639, 0.0057], q=0.1818 | 0.0048 [0.0018, 0.0081], q=0.9441 | generation consistent; phishing opposing/unclear; small/uncertain |

Skipped non-scalar metrics: `perturbation_count`, `regeneration_count`, `uid_max_span`, `uid_min_span`.

### Candidate transferable features

| Type | Feature | Minimum q | Evidence across both cells |
|---|---|---:|---|
| MGT | `total_surprisal` | 4.03e-05 | both q<0.05 |
| MGT | `weighted_ngram_score` | 0.0159 | one q<0.05 |
| MGT | `ngram_overlap_ratio` | 0.0375 | one q<0.05 |
| MGT | `lrr` | 0.0411 | one q<0.05 |
| MGT | `mean_log_rank` | 0.0411 | one q<0.05 |
| MGT | `negative_mean_log_rank` | 0.0411 | one q<0.05 |
| MGT | `phd_intrinsic_dimension` | 0.0411 | one q<0.05 |
| MGT | `rank_100_1000_ratio` | 0.0411 | one q<0.05 |
| MGT | `average_log_probability` | 0.0423 | one q<0.05 |
| MGT | `rank_gt1000_ratio` | 0.0423 | one q<0.05 |
| MGT | `mle_intrinsic_dimension` | 0.0468 | one q<0.05 |
| MGT | `dna_gpt_regeneration_log_probability_difference` | 0.0485 | one q<0.05 |
| MGT | `top10_rank_ratio` | 0.0511 | direction only |
| MGT | `uid_mean` | 0.0659 | direction only |
| MGT | `predictive_entropy` | 0.0667 | direction only |
| MGT | `probability_fraction` | 0.0667 | direction only |
| MGT | `perplexity_from_causal_log_probs` | 0.0793 | direction only |
| MGT | `perplexity_gpt2_large` | 0.0793 | direction only |
| MGT | `fast_detectgpt_analytic` | 0.0817 | direction only |
| MGT | `mean_token_rank` | 0.0818 | direction only |
| MGT | `negative_mean_token_rank` | 0.0818 | direction only |
| MGT | `uid_variance` | 0.0942 | direction only |
| MGT | `uid_diff2` | 0.1145 | direction only |
| MGT | `uid_diff` | 0.1554 | direction only |
| MGT | `fast_detectgpt_sampling` | 0.3439 | direction only |
| MGT | `rank_10_100_ratio` | 0.569 | direction only |
| MGT | `detectgpt_normalized_discrepancy` | 0.5951 | direction only |
| phishing | `probability_fraction` | 0.0357 | one q<0.05 |
| phishing | `average_log_probability` | 0.0481 | one q<0.05 |
| phishing | `mean_log_rank` | 0.0507 | direction only |
| phishing | `negative_mean_log_rank` | 0.0507 | direction only |
| phishing | `ngram_overlap_ratio` | 0.0507 | direction only |
| phishing | `predictive_entropy` | 0.0507 | direction only |
| phishing | `top10_entropy` | 0.0507 | direction only |
| phishing | `dna_gpt_regeneration_log_probability_difference` | 0.0568 | direction only |
| phishing | `uid_mean` | 0.1485 | direction only |
| phishing | `detectgpt_discrepancy` | 0.1583 | direction only |
| phishing | `perplexity_from_causal_log_probs` | 0.1818 | direction only |
| phishing | `perplexity_gpt2_large` | 0.1818 | direction only |
| phishing | `rank_100_1000_ratio` | 0.1818 | direction only |
| phishing | `top10_rank_ratio` | 0.1818 | direction only |
| phishing | `total_surprisal` | 0.1818 | direction only |
| phishing | `npr` | 0.2538 | direction only |
| phishing | `detectgpt_normalized_discrepancy` | 0.46 | direction only |
| phishing | `fast_detectgpt_sampling` | 0.5498 | direction only |
| phishing | `rank_10_100_ratio` | 0.7717 | direction only |
| phishing | `rank_gt1000_ratio` | 0.8093 | direction only |
| phishing | `fast_detectgpt_analytic` | 0.8667 | direction only |
| phishing | `lrr` | 0.8667 | direction only |
| phishing | `uid_diff` | 0.9195 | direction only |

## Phishing

Source: `Phishing\results\matched_pool_44_phishing_metrics.json`

| Feature | G_P | G_B | P_HW | P_MG | Interaction | Transferability reading |
|---|---:|---:|---:|---:|---:|---|
| `authority_density` | -0.0399 [-0.4701, 0.3983], q=0.9027 | 0.4023 [0.0167, 0.8623], q=0.267 | 0.2236 [-0.1358, 0.5945], q=0.5901 | -0.2185 [-0.7002, 0.2581], q=0.4791 | -0.4422 [-1.0671, 0.1156], q=0.3921 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `clause_density` | 0.246 [-0.0146, 0.4892], q=0.4492 | -0.3264 [-0.8761, 0.1034], q=0.471 | -0.3935 [-0.9332, 0.0163], q=0.585 | 0.1788 [-0.0782, 0.4091], q=0.354 | 0.5724 [0.0614, 1.1542], q=0.319 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `cta_density` | 2.0383 [0.7385, 3.5681], q=0.2249 | 1.122 [-0.1353, 2.4687], q=0.335 | 1.9583 [0.8642, 2.979], q=0.0737 | 2.8745 [1.2524, 4.4841], q=0.0243 | 0.9163 [-1.0375, 2.8553], q=0.5894 | generation consistent; phishing consistent; small/uncertain |
| `first_person_ratio` | -0.0068 [-0.0155, 0.0016], q=0.5256 | 0.0124 [2.61e-05, 0.0227], q=0.2706 | 0.0104 [-0.000837, 0.0206], q=0.585 | -0.0088 [-0.0186, 0.001], q=0.354 | -0.0192 [-0.0329, -0.004], q=0.3155 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `imperative_count` | -0.1818 [-0.4545, 0.0909], q=0.519 | -2.78e-17 [-0.3636, 0.3636], q=1 | 2.22e-16 [-0.4545, 0.3636], q=1 | -0.1818 [-0.4545, -5.55e-17], q=0.354 | -0.1818 [-0.6364, 0.2727], q=0.6472 | generation consistent; phishing opposing/unclear; small/uncertain |
| `mean_parse_depth` | 0.1185 [-0.0262, 0.2689], q=0.4929 | -0.1233 [-0.6379, 0.3147], q=0.7702 | -0.4083 [-0.8722, -0.0084], q=0.4325 | -0.1665 [-0.4098, 0.0945], q=0.354 | 0.2418 [-0.2161, 0.8144], q=0.5894 | generation opposing/unclear; phishing consistent; small/uncertain |
| `mean_sentence_len_tokens` | 4.4308 [2.0643, 6.5988], q=0.0276 | -3.3326 [-6.2746, -0.7057], q=0.2307 | -5.2674 [-8.5246, -2.5191], q=0.0357 | 2.4961 [0.3411, 4.712], q=0.14 | 7.7635 [4.2737, 11.7875], q=0.0218 | generation opposing/unclear; phishing opposing/unclear; evidence of interaction |
| `mean_word_len` | 0.2305 [-0.0097, 0.4658], q=0.4079 | 0.6795 [0.4808, 0.8627], q=1.11e-05 | 0.5722 [0.3346, 0.8222], q=0.0059 | 0.1231 [-0.0626, 0.3095], q=0.354 | -0.4491 [-0.7686, -0.1589], q=0.1425 | generation consistent; phishing consistent; small/uncertain |
| `noun_ratio` | -0.0038 [-0.0388, 0.0269], q=0.9027 | 0.0263 [0.0011, 0.0509], q=0.267 | 0.0095 [-0.0249, 0.046], q=0.8485 | -0.0207 [-0.0388, -0.0031], q=0.2108 | -0.0301 [-0.0716, 0.0098], q=0.4232 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `politeness_density` | 1.761 [1.0044, 2.504], q=0.0276 | 0.4285 [-0.5803, 1.3717], q=0.6897 | 0.3275 [-0.6302, 1.2151], q=0.8485 | 1.66 [0.8339, 2.4335], q=0.0233 | 1.3325 [0.0755, 2.6143], q=0.3582 | generation consistent; phishing consistent; small/uncertain |
| `second_person_ratio` | 0.0123 [-0.0063, 0.0306], q=0.4929 | 0.0158 [0.0088, 0.0232], q=0.0986 | 0.0467 [0.0321, 0.0641], q=0.0018 | 0.0432 [0.0318, 0.054], q=6.81e-05 | -0.0035 [-0.0244, 0.0149], q=0.7947 | generation consistent; phishing consistent; small/uncertain |
| `time_pressure_density` | 0.8291 [0.0875, 1.6526], q=0.4079 | 0.27 [-0.2006, 0.7422], q=0.526 | 0.0849 [-0.3336, 0.4357], q=0.8485 | 0.644 [-0.1529, 1.482], q=0.354 | 0.5591 [-0.3189, 1.4915], q=0.5382 | generation consistent; phishing consistent; small/uncertain |
| `ttr` | 0.004 [-0.0357, 0.0393], q=0.9027 | 0.087 [0.0339, 0.1361], q=0.0761 | 0.0359 [-0.0219, 0.0954], q=0.7475 | -0.047 [-0.0704, -0.0219], q=0.0243 | -0.0829 [-0.1447, -0.0201], q=0.3155 | generation consistent; phishing opposing/unclear; small/uncertain |
| `urgency_density` | 0.9575 [-0.0528, 2.0389], q=0.4079 | -9.09e-05 [-0.5082, 0.5639], q=1 | 0.3139 [-0.3686, 1.066], q=0.8043 | 1.2715 [0.3442, 2.2257], q=0.0829 | 0.9576 [-0.2237, 2.146], q=0.3921 | generation opposing/unclear; phishing consistent; small/uncertain |
| `verb_ratio` | 0.0122 [0.0013, 0.0235], q=0.4629 | 0.0077 [-0.0094, 0.0268], q=0.6642 | -0.000155 [-0.0172, 0.0197], q=1 | 0.0044 [-0.0058, 0.0149], q=0.5164 | 0.0045 [-0.0157, 0.0247], q=0.7947 | generation consistent; phishing opposing/unclear; small/uncertain |
| `yules_k` | 9.6952 [-13.1095, 29.8781], q=0.5842 | -40.2956 [-59.7516, -18.5361], q=0.0413 | -7.4705 [-31.4829, 18.232], q=0.8485 | 42.5203 [25.168, 58.3938], q=0.004 | 49.9908 [18.8773, 78.7262], q=0.1011 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |

### Candidate transferable features

| Type | Feature | Minimum q | Evidence across both cells |
|---|---|---:|---|
| MGT | `mean_word_len` | 1.11e-05 | one q<0.05 |
| MGT | `politeness_density` | 0.0276 | one q<0.05 |
| MGT | `ttr` | 0.0761 | direction only |
| MGT | `second_person_ratio` | 0.0986 | direction only |
| MGT | `cta_density` | 0.2249 | direction only |
| MGT | `time_pressure_density` | 0.4079 | direction only |
| MGT | `verb_ratio` | 0.4629 | direction only |
| MGT | `imperative_count` | 0.519 | direction only |
| phishing | `second_person_ratio` | 6.81e-05 | both q<0.05 |
| phishing | `mean_word_len` | 0.0059 | one q<0.05 |
| phishing | `politeness_density` | 0.0233 | one q<0.05 |
| phishing | `cta_density` | 0.0243 | one q<0.05 |
| phishing | `urgency_density` | 0.0829 | direction only |
| phishing | `mean_parse_depth` | 0.354 | direction only |
| phishing | `time_pressure_density` | 0.354 | direction only |

## Stylometric

Source: `Stylometric\results\matched_pool_44_stylometric_metrics.json`

| Feature | G_P | G_B | P_HW | P_MG | Interaction | Transferability reading |
|---|---:|---:|---:|---:|---:|---|
| `character_2gram_count` | -44.7273 [-149.5477, 63.2068], q=0.8065 | -69.5455 [-139.6432, -3.7091], q=0.369 | -19.3636 [-129.1909, 87.0568], q=0.8806 | 5.4545 [-54.7273, 68.4727], q=0.9942 | 24.8182 [-98.9159, 154.8341], q=0.916 | generation consistent; phishing opposing/unclear; small/uncertain |
| `character_2gram_unique` | -17.1818 [-39.0909, 6.8273], q=0.6173 | -21.5455 [-40.7295, -4.7227], q=0.1935 | -18.2727 [-45.7273, 6.5455], q=0.5867 | -13.9091 [-27.0909, -1.6341], q=0.2591 | 4.3636 [-23.8455, 34.3659], q=0.916 | generation consistent; phishing consistent; small/uncertain |
| `character_3gram_count` | -44.7273 [-149.1023, 63.9114], q=0.8065 | -69.5455 [-137.0091, -4.8159], q=0.369 | -19.3636 [-130.5545, 83.3], q=0.8806 | 5.4545 [-57.1023, 69.2068], q=0.9942 | 24.8182 [-93.1818, 157.3636], q=0.916 | generation consistent; phishing opposing/unclear; small/uncertain |
| `character_3gram_unique` | -8.9091 [-58.7364, 48.9795], q=0.9989 | -2.5455 [-40.4682, 32.5455], q=1 | -14.8182 [-74.0023, 37.9182], q=0.8737 | -21.1818 [-56.1818, 11.1909], q=0.6929 | -6.3636 [-64.6386, 60.5477], q=0.916 | generation consistent; phishing consistent; small/uncertain |
| `character_4gram_count` | -44.7273 [-142.2205, 62.9136], q=0.8065 | -69.5455 [-137.5773, 0.8545], q=0.369 | -19.3636 [-124.0932, 82.4636], q=0.8806 | 5.4545 [-54.9227, 67.0932], q=0.9942 | 24.8182 [-100.8205, 147.1409], q=0.916 | generation consistent; phishing opposing/unclear; small/uncertain |
| `character_4gram_unique` | -11 [-81.8205, 62.1932], q=0.9989 | -2.2727 [-42.7591, 36.7568], q=1 | -13.3636 [-82.1273, 53.8227], q=0.8806 | -22.0909 [-69.0045, 28.5932], q=0.8119 | -8.7273 [-91.575, 73.8318], q=0.916 | generation consistent; phishing consistent; small/uncertain |
| `lda_active_topic_count` | -0.3636 [-0.6364, -0.0909], q=0.443 | -0.0909 [-0.5455, 0.1818], q=0.8069 | 0.2727 [-0.1818, 0.6364], q=0.5867 | -9.44e-16 [-0.1818, 0.1818], q=1 | -0.2727 [-0.7273, 0.1818], q=0.5887 | generation consistent; phishing opposing/unclear; small/uncertain |
| `lda_assignment_topic_0` | -0.1335 [-0.2299, -0.0503], q=0.2037 | -0.1166 [-0.2574, 0.0345], q=0.4046 | -0.1324 [-0.2823, 0.0239], q=0.5574 | -0.1493 [-0.2251, -0.0718], q=0.0981 | -0.0169 [-0.1883, 0.1447], q=0.916 | generation consistent; phishing consistent; small/uncertain |
| `lda_assignment_topic_1` | -0.0848 [-0.1731, -0.0058], q=0.4448 | 0.0617 [-0.0929, 0.2156], q=0.7064 | -0.0883 [-0.2268, 0.0601], q=0.5867 | -0.2348 [-0.3407, -0.1368], q=0.0249 | -0.1465 [-0.3126, 0.0236], q=0.5115 | generation opposing/unclear; phishing consistent; small/uncertain |
| `lda_assignment_topic_2` | -0.0227 [-0.0655, 0.0268], q=0.8065 | 0.0199 [-0.0937, 0.1265], q=0.8675 | -0.0256 [-0.1152, 0.0369], q=0.8294 | -0.0682 [-0.1557, 0.0159], q=0.4369 | -0.0426 [-0.1536, 0.0793], q=0.7259 | generation opposing/unclear; phishing consistent; small/uncertain |
| `lda_assignment_topic_3` | -6.94e-18 [-1.39e-17, 0], q=1 | -0.0352 [-0.1057, 0], q=0.4766 | -0.0352 [-0.1057, 0], q=0.5867 | -6.94e-18 [-1.39e-17, 0], q=1 | 0.0352 [0, 0.1057], q=0.5748 | generation consistent; phishing consistent; small/uncertain |
| `lda_assignment_topic_4` | 0.241 [0.1325, 0.3404], q=0.0118 | 0.0702 [-0.0303, 0.1491], q=0.3785 | 0.2816 [0.1587, 0.3911], q=0.0102 | 0.4523 [0.3843, 0.513], q=1.97e-09 | 0.1708 [0.0351, 0.3125], q=0.2466 | generation consistent; phishing consistent; small/uncertain |
| `lda_dominant_topic_mass` | 0.1138 [0.0061, 0.2225], q=0.443 | 0.0214 [-0.0565, 0.1228], q=0.8069 | -0.1098 [-0.2231, 0.0049], q=0.5196 | -0.0174 [-0.0894, 0.0379], q=0.9366 | 0.0924 [-0.0456, 0.2158], q=0.5748 | generation consistent; phishing consistent; small/uncertain |
| `lda_per_token_likelihood_bound` | 0.6083 [-3.0813, 5.063], q=0.9989 | -4.0826 [-7.4316, -1.4201], q=0.1935 | -4.3325 [-8.8364, -0.7798], q=0.5514 | 0.3585 [-2.5302, 3.3624], q=0.9942 | 4.6909 [0.2949, 9.7973], q=0.5115 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `lda_topic_0` | -0.1838 [-0.3676, -0.000251], q=0.443 | -0.2205 [-0.5306, 0.121], q=0.4488 | -0.2874 [-0.5897, -0.0137], q=0.512 | -0.2508 [-0.4828, -0.0712], q=0.2387 | 0.0366 [-0.3209, 0.4055], q=0.916 | generation consistent; phishing consistent; small/uncertain |
| `lda_topic_1` | -0.1794 [-0.4487, 0.000251], q=0.5121 | 0.1987 [-0.1234, 0.5396], q=0.5028 | -0.0905 [-0.3605, 0.1795], q=0.8294 | -0.4686 [-0.738, -0.2689], q=0.0559 | -0.3781 [-0.7582, -6.11e-05], q=0.4183 | generation opposing/unclear; phishing consistent; small/uncertain |
| `lda_topic_2` | -0.0419 [-0.1453, 0.0617], q=0.8065 | 0.0698 [-0.2002, 0.3404], q=0.8069 | -0.0319 [-0.2239, 0.1139], q=0.8806 | -0.1437 [-0.4133, 0.0721], q=0.5856 | -0.1118 [-0.4022, 0.1784], q=0.7183 | generation opposing/unclear; phishing consistent; small/uncertain |
| `lda_topic_3` | 5.36e-05 [-0.000273, 0.000349], q=1 | -0.0484 [-0.1456, 0.000425], q=0.4766 | -0.0484 [-0.1456, 0.000486], q=0.5867 | 6.97e-05 [-0.000175, 0.000293], q=1 | 0.0484 [-0.000474, 0.1456], q=0.5748 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `lda_topic_4` | 0.4051 [0.1726, 0.6341], q=0.0452 | 0.00034 [-0.1797, 0.1803], q=1 | 0.4582 [0.1659, 0.727], q=0.0608 | 0.863 [0.6834, 0.9891], q=8.18e-08 | 0.4048 [0.0948, 0.7195], q=0.2265 | generation consistent; phishing consistent; small/uncertain |
| `lda_topic_entropy` | -0.1922 [-0.3693, -0.0211], q=0.443 | -0.0364 [-0.2548, 0.1368], q=0.8556 | 0.1714 [-0.0378, 0.3732], q=0.5574 | 0.0156 [-0.1301, 0.1745], q=0.9942 | -0.1558 [-0.4076, 0.1005], q=0.5748 | generation consistent; phishing consistent; small/uncertain |
| `pos_adjectives` | 0.0909 [-1.6364, 1.8182], q=1 | 0.5455 [-1.275, 2.1818], q=0.7912 | 0.2727 [-1.2727, 1.9091], q=0.8806 | -0.1818 [-2, 1.5455], q=0.9942 | -0.4545 [-2.8205, 2], q=0.916 | generation consistent; phishing opposing/unclear; small/uncertain |
| `pos_adverbs` | -0.8182 [-2.1818, 0.5455], q=0.7284 | -2.3636 [-3.4545, -1.2727], q=0.0299 | -0.0909 [-1.6364, 1.3659], q=0.9633 | 1.4545 [0.6364, 2.4545], q=0.105 | 1.5455 [-0.2727, 3.2727], q=0.485 | generation consistent; phishing opposing/unclear; small/uncertain |
| `pos_cardinal_numbers` | 0 [-0.4545, 0.3659], q=1 | 1.3636 [0.5432, 2.2727], q=0.1096 | 0.0909 [-0.3636, 0.6364], q=0.8806 | -1.2727 [-2.2727, -0.3636], q=0.1162 | -1.3636 [-2.3636, -0.3636], q=0.2265 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `pos_conjunctions` | -0.6364 [-1.8182, 0.3659], q=0.7284 | -0.8182 [-1.6364, -2.68e-16], q=0.3478 | -0.4545 [-1.5455, 0.8182], q=0.816 | -0.2727 [-1.0023, 0.4568], q=0.814 | 0.1818 [-1.2727, 1.5455], q=0.916 | generation consistent; phishing consistent; small/uncertain |
| `pos_density_1` | 1.2765 [-1.2955, 3.7548], q=0.8065 | 3.0789 [1.3258, 4.8863], q=0.1566 | 1.6181 [-0.8734, 4.137], q=0.7292 | -0.1843 [-2.1208, 1.6896], q=0.9942 | -1.8024 [-4.9279, 1.4919], q=0.6941 | generation consistent; phishing opposing/unclear; small/uncertain |
| `pos_density_2` | -0.4892 [-4.2296, 3.4825], q=0.9989 | 5.2658 [0.9439, 9.0265], q=0.1891 | 2.1224 [-2.8048, 6.6002], q=0.7786 | -3.6326 [-6.4734, -0.5748], q=0.2216 | -5.755 [-10.8266, 0.2212], q=0.4183 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `pos_density_3` | 0.0039 [-3.6241, 3.86], q=1 | 6.0541 [0.8498, 11.4793], q=0.1935 | 1.6919 [-4.0785, 7.8617], q=0.8294 | -4.3583 [-7.0164, -1.7125], q=0.0981 | -6.0502 [-12.6174, -0.0694], q=0.4183 | generation consistent; phishing opposing/unclear; small/uncertain |
| `pos_determiners` | -2.66e-15 [-1.3636, 1.0909], q=1 | -2.2727 [-4.2727, -0.4523], q=0.1935 | -4.5455 [-6.2727, -2.9091], q=0.0102 | -2.2727 [-3.8182, -0.7273], q=0.105 | 2.2727 [-0.0932, 4.6364], q=0.4183 | generation consistent; phishing consistent; small/uncertain |
| `pos_foreign_words` | 0.0909 [0, 0.2727], q=0.7284 | -1.22e-17 [-3.65e-17, 0], q=1 | -2.24e-17 [-6.71e-17, 0], q=1 | 0.0909 [0, 0.2727], q=0.6549 | 0.0909 [0, 0.2727], q=0.5748 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `pos_interrogatives` | 0.1818 [-0.1841, 0.5455], q=0.8065 | -0.6364 [-1.4545, 0.2727], q=0.4666 | -1.1818 [-2, -0.3636], q=0.1564 | -0.3636 [-0.9091, 0.1818], q=0.7215 | 0.8182 [-0.2727, 1.8182], q=0.5317 | generation opposing/unclear; phishing consistent; small/uncertain |
| `pos_nouns` | -1.8182 [-9, 5.55], q=0.9398 | -5.8182 [-10.9091, -0.2705], q=0.2866 | -2.6364 [-10.9159, 5.9114], q=0.8294 | 1.3636 [-2.8182, 5.5455], q=0.8246 | 4 [-5.4591, 13.1841], q=0.7149 | generation consistent; phishing opposing/unclear; small/uncertain |
| `pos_particles` | 0.2727 [-2.5e-16, 0.6364], q=0.6173 | -0.0909 [-0.7273, 0.4545], q=0.9078 | -0.8182 [-1.4545, -0.3614], q=0.1318 | -0.4545 [-0.8182, 2.23e-16], q=0.3372 | 0.3636 [-0.2727, 1.0909], q=0.6246 | generation opposing/unclear; phishing consistent; small/uncertain |
| `pos_possessive_pronouns` | 1.2727 [-0.4545, 2.6364], q=0.6924 | 2.7273 [2.0909, 3.3636], q=0.000628 | 4.2727 [2.9091, 5.8182], q=0.0102 | 2.8182 [2, 3.6364], q=0.0022 | -1.4545 [-3.3636, -3.99e-15], q=0.5748 | generation consistent; phishing consistent; small/uncertain |
| `pos_prepositions` | -0.2727 [-2.5477, 2], q=0.9989 | -2.5455 [-4.3636, -0.5455], q=0.2414 | -3 [-5.2727, -0.5455], q=0.512 | -0.7273 [-2.5455, 0.9091], q=0.814 | 2.2727 [-0.6364, 5.0023], q=0.5748 | generation consistent; phishing consistent; small/uncertain |
| `pos_verbs` | -1.3636 [-3.7273, 0.9091], q=0.8065 | -4.4545 [-8.0932, -0.5432], q=0.2179 | -4.0909 [-7.4545, -0.5455], q=0.512 | -1 [-3.7295, 1.5455], q=0.814 | 3.0909 [-1.3636, 7.2727], q=0.5748 | generation consistent; phishing consistent; small/uncertain |
| `sentence_mean_sentence_length` | 36.7798 [26.9448, 45.5457], q=4.22e-05 | -34.8089 [-65.691, -12.3124], q=0.1096 | -43.3731 [-72.9637, -22.389], q=0.0547 | 28.2156 [19.3728, 36.7485], q=0.0021 | 71.5887 [47.2555, 103.14], q=0.0027 | generation opposing/unclear; phishing opposing/unclear; evidence of interaction |
| `sentence_variance_of_sentence_length` | 568.2733 [-659.596, 1.79e+03], q=0.8065 | -4.65e+03 [-8.57e+03, -1.41e+03], q=0.1244 | -4.53e+03 [-8.26e+03, -1.13e+03], q=0.1854 | 687.2214 [-325.6167, 1.74e+03], q=0.5856 | 5.22e+03 [1.59e+03, 9.3e+03], q=0.1953 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `surface_character_count` | -44.7273 [-149.3773, 66.8227], q=0.8065 | -69.5455 [-136.275, -4.8136], q=0.369 | -19.3636 [-127.3705, 82.1], q=0.8806 | 5.4545 [-58.6545, 68.3955], q=0.9942 | 24.8182 [-89.6841, 153.1432], q=0.916 | generation consistent; phishing opposing/unclear; small/uncertain |
| `surface_character_count_without_spaces` | -38.9091 [-125.8409, 53.1909], q=0.8065 | -50.4545 [-107.9273, 6.0955], q=0.4488 | -5.8182 [-98.8455, 91.0136], q=0.9633 | 5.7273 [-46.7295, 57.275], q=0.9942 | 11.5455 [-95.9114, 121.075], q=0.916 | generation consistent; phishing opposing/unclear; small/uncertain |
| `surface_comma_percentage` | 0.2292 [0.1164, 0.3309], q=0.0453 | 0.307 [0.1422, 0.4543], q=0.0302 | -0.0373 [-0.213, 0.1244], q=0.8806 | -0.1152 [-0.2109, -0.0201], q=0.202 | -0.0778 [-0.2669, 0.1122], q=0.7259 | generation consistent; phishing consistent; small/uncertain |
| `surface_digit_count` | -0.2727 [-1.4545, 0.8205], q=0.9461 | 2.6364 [0.6364, 4.6364], q=0.1246 | 0.6364 [-0.3636, 1.8182], q=0.5867 | -2.2727 [-4.3636, -0.0909], q=0.2352 | -2.9091 [-5.4545, -0.3636], q=0.2265 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `surface_digit_ratio` | -0.0173 [-0.1859, 0.1379], q=0.9989 | 0.4577 [0.1391, 0.8328], q=0.1244 | 0.0922 [-0.033, 0.2248], q=0.5574 | -0.3829 [-0.7774, -0.0486], q=0.2387 | -0.475 [-0.8857, -0.1325], q=0.2265 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `surface_letter_ratio` | 1.9062 [1.0733, 2.7504], q=0.009 | 3.6349 [2.2876, 4.7271], q=0.000628 | 2.5673 [1.5489, 3.5093], q=0.007 | 0.8386 [-0.2032, 2.0746], q=0.4779 | -1.7287 [-3.1976, -0.1693], q=0.2466 | generation consistent; phishing consistent; small/uncertain |
| `surface_punctuation_percentage` | -0.1649 [-0.3546, 0.0376], q=0.6173 | 0.3489 [0.0096, 0.7013], q=0.2325 | 0.1544 [-0.1455, 0.451], q=0.7041 | -0.3595 [-0.6451, -0.1158], q=0.1134 | -0.5139 [-0.9006, -0.1316], q=0.2265 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `surface_question_sentence_percentage` | -3.2828 [-6.8182, -3.55e-15], q=0.5121 | -5.6061 [-10.9091, -0.303], q=0.2414 | -3.8384 [-9.6465, 1.5215], q=0.5867 | -1.5152 [-3.0303, -1.33e-15], q=0.7678 | 2.3232 [-3.7879, 8.1326], q=0.7615 | generation consistent; phishing consistent; small/uncertain |
| `surface_semicolon_percentage` | -0.0173 [-0.052, 0], q=0.7284 | 1.3e-17 [0, 3.89e-17], q=1 | 0.0173 [0, 0.052], q=0.5867 | -6.94e-18 [-1.39e-17, 0], q=1 | -0.0173 [-0.052, 0], q=0.5748 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `surface_space_count` | -5.8182 [-19.275, 7.55], q=0.8095 | -19.0909 [-29.1886, -9.4523], q=0.1244 | -13.5455 [-27.3682, 0.1818], q=0.5574 | -0.2727 [-9.3659, 9.4545], q=1 | 13.2727 [-3.0045, 30.1818], q=0.5748 | generation consistent; phishing consistent; small/uncertain |
| `surface_special_character_ratio` | -1.8889 [-2.6785, -1.2078], q=0.0056 | -3.8792 [-4.7856, -2.8715], q=1.11e-05 | -2.446 [-3.343, -1.4875], q=0.007 | -0.4557 [-1.3107, 0.3204], q=0.6929 | 1.9903 [0.787, 3.233], q=0.1331 | generation consistent; phishing consistent; small/uncertain |
| `surface_uppercase_count` | -53.9091 [-73.2773, -33.9068], q=0.0096 | -79.4545 [-111.4545, -50.0864], q=0.0034 | -25.5455 [-63.9114, 9.9114], q=0.5867 | -6.04e-14 [-3.7295, 4], q=1 | 25.5455 [-9.6795, 63.7364], q=0.5748 | generation consistent; phishing consistent; small/uncertain |
| `surface_uppercase_ratio` | -7.1055 [-9.0588, -5.3331], q=9.16e-05 | -11.0965 [-15.3219, -7.3555], q=0.000628 | -4.0896 [-8.4745, 0.1912], q=0.512 | -0.0987 [-0.6225, 0.4223], q=0.9942 | 3.991 [-0.3224, 8.4908], q=0.4183 | generation consistent; phishing consistent; small/uncertain |
| `surface_whitespace_ratio` | -0.0935 [-0.8119, 0.6756], q=0.9989 | -1.3357 [-1.9159, -0.7689], q=0.0055 | -1.3931 [-2.2344, -0.6063], q=0.0617 | -0.1508 [-0.6218, 0.3069], q=0.8371 | 1.2423 [0.2658, 2.2273], q=0.2265 | generation consistent; phishing consistent; small/uncertain |
| `syntactic_apostrophe` | -0.9091 [-1.3636, -0.4545], q=0.1209 | 0.4545 [-0.4545, 1.3636], q=0.5913 | -0.0909 [-0.9091, 0.7273], q=0.9212 | -1.4545 [-2, -0.9091], q=0.019 | -1.3636 [-2.3636, -0.3636], q=0.2466 | generation opposing/unclear; phishing consistent; small/uncertain |
| `syntactic_brackets` | -7.2727 [-10.7273, -4], q=0.0452 | -20.9091 [-26.5455, -15.4545], q=0.000264 | -9.2727 [-15.8182, -2.9045], q=0.2226 | 4.3636 [3.2727, 5.6364], q=0.000193 | 13.6364 [7.0909, 20], q=0.0819 | generation consistent; phishing opposing/unclear; small/uncertain |
| `syntactic_colon` | 0.7273 [-0.1818, 1.3636], q=0.5121 | -0.2727 [-1.8182, 1.2727], q=0.8768 | -0.6364 [-2.0909, 0.8182], q=0.7308 | 0.3636 [-0.7273, 1.2727], q=0.814 | 1 [-0.7273, 2.7273], q=0.5784 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `syntactic_comma` | 1.1818 [0.3636, 1.9091], q=0.2746 | 1.3636 [0.0909, 2.3636], q=0.2414 | -0.4545 [-1.8182, 0.8182], q=0.8294 | -0.6364 [-1.1818, -0.0886], q=0.3412 | -0.1818 [-1.5455, 1.3636], q=0.916 | generation consistent; phishing consistent; small/uncertain |
| `syntactic_dash` | -1.7273 [-3.6364, -0.2727], q=0.4423 | 0.5455 [-0.4545, 1.4545], q=0.5913 | 0.7273 [-0.8182, 2.7273], q=0.7491 | -1.5455 [-2.4545, -0.5455], q=0.1035 | -2.2727 [-4.3636, -0.3636], q=0.2719 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `syntactic_exclamation` | -0.6364 [-1.1818, -0.2727], q=0.1821 | -0.4545 [-0.9091, 3.33e-16], q=0.2645 | 0.0909 [-0.5455, 0.8182], q=0.8806 | -0.0909 [-0.2727, -1.94e-16], q=0.814 | -0.1818 [-0.9091, 0.4545], q=0.8418 | generation consistent; phishing opposing/unclear; small/uncertain |
| `syntactic_full_stop` | -2.9091 [-4.2727, -1.4545], q=0.0295 | 1.5455 [0.1818, 2.8182], q=0.1935 | 2.8182 [1.0909, 4.4545], q=0.0715 | -1.6364 [-2.5455, -0.6364], q=0.0974 | -4.4545 [-6.4545, -2.4523], q=0.021 | generation opposing/unclear; phishing opposing/unclear; evidence of interaction |
| `syntactic_question_mark` | -0.1818 [-0.2727, -2.21e-16], q=0.4761 | -0.5455 [-1.1818, 0], q=0.2988 | -0.4545 [-1.0909, 0.0909], q=0.5574 | -0.0909 [-0.1818, -5.55e-17], q=0.814 | 0.3636 [-0.1818, 1], q=0.5815 | generation consistent; phishing consistent; small/uncertain |
| `syntactic_semicolon` | -0.0909 [-0.2727, 0], q=0.7284 | 6.79e-17 [0, 2.04e-16], q=1 | 0.0909 [0, 0.2727], q=0.5867 | -4.16e-17 [-1.11e-16, 0], q=1 | -0.0909 [-0.2727, 0], q=0.5748 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `syntactic_slash` | -0.1818 [-0.7295, 0.1818], q=0.8261 | -1.7273 [-3.4545, -8.53e-18], q=0.2529 | -1.4545 [-3.3636, 0.2727], q=0.5574 | 0.0909 [-8.88e-16, 0.2727], q=0.9366 | 1.5455 [-0.1841, 3.4568], q=0.485 | generation consistent; phishing opposing/unclear; small/uncertain |
| `vocabulary_average_sentence_length_characters` | 36.7798 [26.2928, 45.6213], q=4.22e-05 | -34.8089 [-63.1351, -13.4499], q=0.1096 | -43.3731 [-71.0628, -21.6779], q=0.0547 | 28.2156 [19.5412, 36.6525], q=0.0021 | 71.5887 [48.9108, 101.4829], q=0.0027 | generation opposing/unclear; phishing opposing/unclear; evidence of interaction |
| `vocabulary_average_sentence_length_words` | 5.4446 [3.897, 6.9157], q=0.000234 | -6.6005 [-10.9727, -2.5182], q=0.0654 | -8.1299 [-12.3884, -4.2885], q=0.0291 | 3.9153 [2.4129, 5.2251], q=0.0147 | 12.0452 [7.5389, 16.4587], q=0.0027 | generation opposing/unclear; phishing opposing/unclear; evidence of interaction |
| `vocabulary_average_word_length` | -0.000581 [-0.2903, 0.2819], q=1 | 0.4245 [0.1572, 0.661], q=0.0469 | 0.5398 [0.2215, 0.8433], q=0.0617 | 0.1147 [-0.1023, 0.3441], q=0.6965 | -0.4251 [-0.8146, -0.0094], q=0.2719 | generation opposing/unclear; phishing consistent; small/uncertain |
| `vocabulary_brunet_w` | -0.1834 [-0.4623, 0.1319], q=0.8065 | -0.7936 [-1.0688, -0.4988], q=0.0055 | -0.4058 [-0.7681, -0.0454], q=0.5343 | 0.2044 [0.0024, 0.4246], q=0.3608 | 0.6102 [0.2044, 1.0281], q=0.2466 | generation consistent; phishing opposing/unclear; small/uncertain |
| `vocabulary_hapax_legomena` | 0.9091 [-5.4545, 6.7273], q=0.9989 | 8.8182 [1.5455, 15.7273], q=0.1935 | 2.49e-14 [-8.7273, 8.1818], q=1 | -7.9091 [-13.275, -3.0886], q=0.1102 | -7.9091 [-17.55, 1.6386], q=0.5115 | generation consistent; phishing opposing/unclear; small/uncertain |
| `vocabulary_honore_r` | -27.9753 [-594.95, 507.0468], q=1 | 1.77e+03 [826.0056, 2.91e+03], q=0.0591 | 640.0527 [-88.4181, 1.3e+03], q=0.5574 | -1.15e+03 [-2.19e+03, -290.6638], q=0.2333 | -1.79e+03 [-3e+03, -644.3248], q=0.2265 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `vocabulary_ratio_short_words` | -3.9179 [-7.0763, -0.5358], q=0.311 | -3.7078 [-7.1403, 0.0033], q=0.2179 | -6.8591 [-9.6946, -3.9446], q=0.0102 | -7.0693 [-10.9453, -3.4343], q=0.04 | -0.2101 [-5.0535, 4.5284], q=0.9585 | generation consistent; phishing consistent; small/uncertain |
| `vocabulary_sichel_s` | 0.0206 [-0.0084, 0.0523], q=0.7284 | -0.0596 [-0.0948, -0.0218], q=0.0591 | -0.0513 [-0.0908, -0.0118], q=0.1854 | 0.0289 [-0.001, 0.0574], q=0.3412 | 0.0802 [0.0322, 0.1284], q=0.1331 | generation opposing/unclear; phishing opposing/unclear; small/uncertain |
| `vocabulary_simpson_d` | -0.00027 [-0.0021, 0.0014], q=0.9989 | -0.0049 [-0.0065, -0.0033], q=0.000628 | -0.000868 [-0.0028, 0.0011], q=0.7292 | 0.0037 [0.0023, 0.0052], q=0.0021 | 0.0046 [0.0023, 0.0071], q=0.0604 | generation consistent; phishing opposing/unclear; small/uncertain |
| `vocabulary_total_unique_words` | -6.75e-14 [-7.9114, 8.1886], q=1 | 0.3636 [-6.8182, 7.275], q=1 | -5.4545 [-15, 3], q=0.6474 | -5.8182 [-12.9091, 0.9091], q=0.4779 | -0.3636 [-10.9136, 11.1841], q=0.964 | generation opposing/unclear; phishing consistent; small/uncertain |
| `vocabulary_total_words` | -5.6364 [-18.3682, 7.4545], q=0.8131 | -17.4545 [-27.0023, -6.0909], q=0.1891 | -13 [-27.0932, 1.1818], q=0.5867 | -1.1818 [-11.7386, 8.9114], q=0.9942 | 11.8182 [-6.9114, 28.4568], q=0.5838 | generation consistent; phishing consistent; small/uncertain |
| `vocabulary_yule_k` | 342.0675 [-153.6467, 785.842], q=0.8065 | 1.98e+03 [1.22e+03, 2.68e+03], q=0.002 | 669.5898 [-11.2134, 1.33e+03], q=0.5574 | -967.0267 [-1.59e+03, -475.9214], q=0.0645 | -1.64e+03 [-2.47e+03, -807.7695], q=0.1484 | generation consistent; phishing opposing/unclear; small/uncertain |

Skipped non-scalar metrics: `pos_symbols`, `surface_tab_count`, `surface_tab_ratio`, `syntactic_ellipsis`.

### Candidate transferable features

| Type | Feature | Minimum q | Evidence across both cells |
|---|---|---:|---|
| MGT | `surface_special_character_ratio` | 1.11e-05 | both q<0.05 |
| MGT | `surface_uppercase_ratio` | 9.16e-05 | both q<0.05 |
| MGT | `syntactic_brackets` | 0.000264 | both q<0.05 |
| MGT | `pos_possessive_pronouns` | 0.000628 | one q<0.05 |
| MGT | `surface_letter_ratio` | 0.000628 | both q<0.05 |
| MGT | `vocabulary_simpson_d` | 0.000628 | one q<0.05 |
| MGT | `vocabulary_yule_k` | 0.002 | one q<0.05 |
| MGT | `surface_uppercase_count` | 0.0034 | both q<0.05 |
| MGT | `surface_whitespace_ratio` | 0.0055 | one q<0.05 |
| MGT | `vocabulary_brunet_w` | 0.0055 | one q<0.05 |
| MGT | `lda_assignment_topic_4` | 0.0118 | one q<0.05 |
| MGT | `pos_adverbs` | 0.0299 | one q<0.05 |
| MGT | `surface_comma_percentage` | 0.0302 | both q<0.05 |
| MGT | `lda_topic_4` | 0.0452 | one q<0.05 |
| MGT | `surface_space_count` | 0.1244 | direction only |
| MGT | `pos_density_1` | 0.1566 | direction only |
| MGT | `syntactic_exclamation` | 0.1821 | direction only |
| MGT | `vocabulary_total_words` | 0.1891 | direction only |
| MGT | `character_2gram_unique` | 0.1935 | direction only |
| MGT | `pos_density_3` | 0.1935 | direction only |
| MGT | `pos_determiners` | 0.1935 | direction only |
| MGT | `vocabulary_hapax_legomena` | 0.1935 | direction only |
| MGT | `lda_assignment_topic_0` | 0.2037 | direction only |
| MGT | `pos_verbs` | 0.2179 | direction only |
| MGT | `vocabulary_ratio_short_words` | 0.2179 | direction only |
| MGT | `pos_prepositions` | 0.2414 | direction only |
| MGT | `surface_question_sentence_percentage` | 0.2414 | direction only |
| MGT | `syntactic_comma` | 0.2414 | direction only |
| MGT | `syntactic_slash` | 0.2529 | direction only |
| MGT | `pos_nouns` | 0.2866 | direction only |
| MGT | `syntactic_question_mark` | 0.2988 | direction only |
| MGT | `pos_conjunctions` | 0.3478 | direction only |
| MGT | `character_2gram_count` | 0.369 | direction only |
| MGT | `character_3gram_count` | 0.369 | direction only |
| MGT | `character_4gram_count` | 0.369 | direction only |
| MGT | `surface_character_count` | 0.369 | direction only |
| MGT | `lda_active_topic_count` | 0.443 | direction only |
| MGT | `lda_dominant_topic_mass` | 0.443 | direction only |
| MGT | `lda_topic_0` | 0.443 | direction only |
| MGT | `lda_topic_entropy` | 0.443 | direction only |
| MGT | `surface_character_count_without_spaces` | 0.4488 | direction only |
| MGT | `lda_assignment_topic_3` | 0.4766 | direction only |
| MGT | `pos_adjectives` | 0.7912 | direction only |
| MGT | `character_3gram_unique` | 0.9989 | direction only |
| MGT | `character_4gram_unique` | 0.9989 | direction only |
| phishing | `lda_assignment_topic_4` | 1.97e-09 | both q<0.05 |
| phishing | `lda_topic_4` | 8.18e-08 | one q<0.05 |
| phishing | `pos_possessive_pronouns` | 0.0022 | both q<0.05 |
| phishing | `surface_letter_ratio` | 0.007 | one q<0.05 |
| phishing | `surface_special_character_ratio` | 0.007 | one q<0.05 |
| phishing | `pos_determiners` | 0.0102 | one q<0.05 |
| phishing | `vocabulary_ratio_short_words` | 0.0102 | both q<0.05 |
| phishing | `syntactic_apostrophe` | 0.019 | one q<0.05 |
| phishing | `lda_assignment_topic_1` | 0.0249 | one q<0.05 |
| phishing | `lda_topic_1` | 0.0559 | direction only |
| phishing | `surface_whitespace_ratio` | 0.0617 | direction only |
| phishing | `vocabulary_average_word_length` | 0.0617 | direction only |
| phishing | `lda_assignment_topic_0` | 0.0981 | direction only |
| phishing | `pos_particles` | 0.1318 | direction only |
| phishing | `pos_interrogatives` | 0.1564 | direction only |
| phishing | `surface_comma_percentage` | 0.202 | direction only |
| phishing | `lda_topic_0` | 0.2387 | direction only |
| phishing | `character_2gram_unique` | 0.2591 | direction only |
| phishing | `syntactic_comma` | 0.3412 | direction only |
| phishing | `lda_assignment_topic_2` | 0.4369 | direction only |
| phishing | `vocabulary_total_unique_words` | 0.4779 | direction only |
| phishing | `pos_prepositions` | 0.512 | direction only |
| phishing | `pos_verbs` | 0.512 | direction only |
| phishing | `surface_uppercase_ratio` | 0.512 | direction only |
| phishing | `lda_dominant_topic_mass` | 0.5196 | direction only |
| phishing | `lda_topic_entropy` | 0.5574 | direction only |
| phishing | `surface_space_count` | 0.5574 | direction only |
| phishing | `syntactic_question_mark` | 0.5574 | direction only |
| phishing | `lda_topic_2` | 0.5856 | direction only |
| phishing | `lda_assignment_topic_3` | 0.5867 | direction only |
| phishing | `surface_question_sentence_percentage` | 0.5867 | direction only |
| phishing | `surface_uppercase_count` | 0.5867 | direction only |
| phishing | `vocabulary_total_words` | 0.5867 | direction only |
| phishing | `character_3gram_unique` | 0.6929 | direction only |
| phishing | `character_4gram_unique` | 0.8119 | direction only |
| phishing | `pos_conjunctions` | 0.814 | direction only |

