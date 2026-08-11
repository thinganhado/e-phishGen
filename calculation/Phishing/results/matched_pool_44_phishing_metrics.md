# Phishing stylometric descriptive comparison

This report summarizes the 16 applicable phishing features for `matched_pool_44.json`; individual sample rows are omitted.

## Dataset and settings

- Samples: **44**
- `HW-P`: **11**; `MG-P`: **11**
- `HW-B`: **11**; `MG-B`: **11**
- Each sample was processed as one input using the source `extract_features()` function.
- spaCy model: `en_core_web_sm`.
- URL metrics are intentionally excluded because this dataset does not contain URL information.
- Difference is left mean minus right mean; Cohen d is descriptive, not a significance test.

## HWT versus MGT

| Metric | HW mean | MG mean | Difference (HW - MG) | Cohen d |
|---|---:|---:|---:|---:|
| Authority density | 0.2802 | 0.4614 | -0.1812 | -0.3153 |
| Clause density | 1.8445 | 1.8043 | 0.0402 | 0.0719 |
| Cta density | 2.1825 | 3.7626 | -1.5801 | -0.6926 |
| First person ratio | 0.0306 | 0.0334 | -0.0028 | -0.1600 |
| Imperative count | 0.2727 | 0.1818 | 0.0909 | 0.1898 |
| Mean parse depth | 2.3937 | 2.3913 | 0.0024 | 0.0049 |
| Mean sentence len tokens | 16.1877 | 16.7368 | -0.5491 | -0.1326 |
| Mean word len | 5.0098 | 5.4648 | -0.4550 | -1.2634 |
| Noun ratio | 0.1859 | 0.1972 | -0.0112 | -0.2729 |
| Politeness density | 2.0411 | 3.1358 | -1.0947 | -0.7199 |
| Second person ratio | 0.0400 | 0.0540 | -0.0140 | -0.4401 |
| Time pressure density | 0.2943 | 0.8438 | -0.5495 | -0.5959 |
| Ttr | 0.7035 | 0.7490 | -0.0455 | -0.5962 |
| Urgency density | 0.6540 | 1.1327 | -0.4787 | -0.4027 |
| Verb ratio | 0.1045 | 0.1145 | -0.0099 | -0.4548 |
| Yules k | 106.9199 | 91.6197 | 15.3002 | 0.4334 |

### Outstanding observations

- Mean word length is the clearest HWT/MGT difference (d = -1.2634): MG samples use longer words on average.
- MG also has higher CTA density (d = -0.6926), politeness density (d = -0.7199), time-pressure density (d = -0.5959), TTR (d = -0.5962), and urgency density (d = -0.4027).
- HWT has higher Yule's K (d = 0.4334), indicating more word-frequency concentration under this corpus and tokenizer.
- Mean parse depth is essentially identical between HW and MG (d = 0.0049), while clause density and imperative count are also weak separators.


## Phishing versus benign

| Metric | P mean | B mean | Difference (P - B) | Cohen d |
|---|---:|---:|---:|---:|
| Authority density | 0.3720 | 0.3695 | 0.0025 | 0.0044 |
| Clause density | 1.7707 | 1.8781 | -0.1074 | -0.1928 |
| Cta density | 4.1808 | 1.7644 | 2.4164 | 1.1614 |
| First person ratio | 0.0324 | 0.0316 | 0.0008 | 0.0441 |
| Imperative count | 0.1818 | 0.2727 | -0.0909 | -0.1898 |
| Mean parse depth | 2.2488 | 2.5362 | -0.2874 | -0.6220 |
| Mean sentence len tokens | 15.7694 | 17.1550 | -1.3856 | -0.3389 |
| Mean word len | 5.4111 | 5.0635 | 0.3476 | 0.8909 |
| Noun ratio | 0.1888 | 0.1944 | -0.0056 | -0.1349 |
| Politeness density | 3.0853 | 2.0916 | 0.9937 | 0.6458 |
| Second person ratio | 0.0695 | 0.0245 | 0.0450 | 1.9366 |
| Time pressure density | 0.7513 | 0.3868 | 0.3645 | 0.3853 |
| Ttr | 0.7235 | 0.7290 | -0.0055 | -0.0695 |
| Urgency density | 1.2897 | 0.4970 | 0.7927 | 0.6930 |
| Verb ratio | 0.1106 | 0.1084 | 0.0021 | 0.0942 |
| Yules k | 108.0322 | 90.5074 | 17.5249 | 0.5003 |

### Outstanding observations

- Second-person ratio is the strongest Phishing/Benign difference (d = 1.9366): phishing samples address the reader much more directly.
- CTA density is also substantially higher for phishing (d = 1.1614), followed by mean word length (d = 0.8909), urgency density (d = 0.6930), politeness density (d = 0.6458), and time-pressure density (d = 0.3853).
- Phishing samples have lower mean parse depth (d = -0.6220) and shorter mean sentences (d = -0.3389) than benign samples.
- Authority density (d = 0.0044), TTR (d = -0.0695), verb ratio (d = 0.0942), and first-person ratio (d = 0.0441) show little or no separation.

## Reproducibility

The complete per-sample values remain available in `matched_pool_44_phishing_metrics.json`.
