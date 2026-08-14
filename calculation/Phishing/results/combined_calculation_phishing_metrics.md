# Phishing stylometric descriptive comparison

This report summarizes the 16 applicable phishing features for `matched_pool_44.json`; individual sample rows are omitted.

## Dataset and settings

- Samples: **2352**
- `HW-P`: **168**; `MG-P`: **1008**
- `HW-B`: **168**; `MG-B`: **1008**
- Each sample was processed as one input using the source `extract_features()` function.
- spaCy model: `en_core_web_sm`.
- URL metrics are intentionally excluded because this dataset does not contain URL information.
- Difference is left mean minus right mean; Cohen d is descriptive, not a significance test.

## HWT versus MGT

| Metric | HW mean | MG mean | Difference (HW - MG) | Cohen d |
|---|---:|---:|---:|---:|
| Authority density | 0.3437 | 0.3730 | -0.0293 | -0.0335 |
| Clause density | 1.7351 | 1.9043 | -0.1693 | -0.4606 |
| Cta density | 1.1357 | 1.1316 | 0.0041 | 0.0036 |
| First person ratio | 0.0350 | 0.0423 | -0.0073 | -0.2782 |
| Imperative count | 0.4762 | 0.2584 | 0.2178 | 0.3824 |
| Mean parse depth | 2.4900 | 2.5762 | -0.0862 | -0.1996 |
| Mean sentence len tokens | 16.1401 | 16.8057 | -0.6656 | -0.1956 |
| Mean word len | 4.7955 | 5.0538 | -0.2582 | -0.6177 |
| Noun ratio | 0.1725 | 0.1779 | -0.0053 | -0.1774 |
| Politeness density | 2.2837 | 2.0151 | 0.2687 | 0.1924 |
| Second person ratio | 0.0530 | 0.0550 | -0.0021 | -0.0788 |
| Time pressure density | 0.5759 | 0.7594 | -0.1836 | -0.1847 |
| Ttr | 0.7202 | 0.6982 | 0.0220 | 0.3157 |
| Urgency density | 0.6746 | 1.0983 | -0.4236 | -0.3778 |
| Verb ratio | 0.1093 | 0.1230 | -0.0137 | -0.6377 |
| Yules k | 114.5426 | 98.2718 | 16.2708 | 0.5532 |

### Outstanding observations

- Mean word length is the clearest HWT/MGT difference (d = -1.2634): MG samples use longer words on average.
- MG also has higher CTA density (d = -0.6926), politeness density (d = -0.7199), time-pressure density (d = -0.5959), TTR (d = -0.5962), and urgency density (d = -0.4027).
- HWT has higher Yule's K (d = 0.4334), indicating more word-frequency concentration under this corpus and tokenizer.
- Mean parse depth is essentially identical between HW and MG (d = 0.0049), while clause density and imperative count are also weak separators.


## Phishing versus benign

| Metric | P mean | B mean | Difference (P - B) | Cohen d |
|---|---:|---:|---:|---:|
| Authority density | 0.3992 | 0.3385 | 0.0606 | 0.0693 |
| Clause density | 1.8921 | 1.8682 | 0.0240 | 0.0644 |
| Cta density | 1.1902 | 1.0741 | 0.1162 | 0.1014 |
| First person ratio | 0.0382 | 0.0443 | -0.0061 | -0.2317 |
| Imperative count | 0.3044 | 0.2747 | 0.0298 | 0.0518 |
| Mean parse depth | 2.6153 | 2.5125 | 0.1028 | 0.2392 |
| Mean sentence len tokens | 17.0926 | 16.3287 | 0.7639 | 0.2254 |
| Mean word len | 5.0432 | 4.9906 | 0.0526 | 0.1232 |
| Noun ratio | 0.1788 | 0.1754 | 0.0034 | 0.1128 |
| Politeness density | 1.7458 | 2.3611 | -0.6152 | -0.4507 |
| Second person ratio | 0.0489 | 0.0606 | -0.0117 | -0.4561 |
| Time pressure density | 0.7804 | 0.6861 | 0.0943 | 0.0948 |
| Ttr | 0.7086 | 0.6940 | 0.0146 | 0.2085 |
| Urgency density | 1.1624 | 0.9131 | 0.2494 | 0.2218 |
| Verb ratio | 0.1193 | 0.1229 | -0.0036 | -0.1620 |
| Yules k | 93.5549 | 107.6376 | -14.0827 | -0.4837 |

### Outstanding observations

- Second-person ratio is the strongest Phishing/Benign difference (d = 1.9366): phishing samples address the reader much more directly.
- CTA density is also substantially higher for phishing (d = 1.1614), followed by mean word length (d = 0.8909), urgency density (d = 0.6930), politeness density (d = 0.6458), and time-pressure density (d = 0.3853).
- Phishing samples have lower mean parse depth (d = -0.6220) and shorter mean sentences (d = -0.3389) than benign samples.
- Authority density (d = 0.0044), TTR (d = -0.0695), verb ratio (d = 0.0942), and first-person ratio (d = 0.0441) show little or no separation.
- URL metrics are excluded from this analysis because the dataset contains no URL information.

## Reproducibility

The complete per-sample values remain available in `matched_pool_44_phishing_metrics.json`.
