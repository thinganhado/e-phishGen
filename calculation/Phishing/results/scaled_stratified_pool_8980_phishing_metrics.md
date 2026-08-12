# Phishing stylometric descriptive comparison

This report summarizes the 16 applicable phishing features for `matched_pool_44.json`; individual sample rows are omitted.

## Dataset and settings

- Samples: **8980**
- `HW-P`: **2245**; `MG-P`: **2245**
- `HW-B`: **2245**; `MG-B`: **2245**
- Each sample was processed as one input using the source `extract_features()` function.
- spaCy model: `en_core_web_sm`.
- URL metrics are intentionally excluded because this dataset does not contain URL information.
- Difference is left mean minus right mean; Cohen d is descriptive, not a significance test.

## HWT versus MGT

| Metric | HW mean | MG mean | Difference (HW - MG) | Cohen d |
|---|---:|---:|---:|---:|
| Authority density | 0.1676 | 0.7756 | -0.6080 | -0.6502 |
| Clause density | 1.7266 | 1.9224 | -0.1958 | -0.3332 |
| Cta density | 0.9524 | 2.0767 | -1.1242 | -0.5667 |
| First person ratio | 0.0281 | 0.0499 | -0.0218 | -0.9013 |
| Imperative count | 0.4884 | 0.3312 | 0.1572 | 0.1889 |
| Mean parse depth | 2.5883 | 2.6266 | -0.0383 | -0.0488 |
| Mean sentence len tokens | 19.2312 | 16.4935 | 2.7377 | 0.3154 |
| Mean word len | 4.8784 | 5.4124 | -0.5340 | -1.0016 |
| Noun ratio | 0.1711 | 0.1856 | -0.0145 | -0.3218 |
| Politeness density | 1.2139 | 2.8525 | -1.6386 | -1.0368 |
| Second person ratio | 0.0254 | 0.0472 | -0.0218 | -0.8894 |
| Time pressure density | 0.2896 | 0.4354 | -0.1458 | -0.1927 |
| Ttr | 0.6595 | 0.7745 | -0.1150 | -1.0109 |
| Urgency density | 0.5734 | 1.0668 | -0.4934 | -0.3771 |
| Verb ratio | 0.0867 | 0.1235 | -0.0369 | -1.2499 |
| Yules k | 165.9959 | 76.4773 | 89.5186 | 0.4178 |

### Outstanding observations

- Mean word length is the clearest HWT/MGT difference (d = -1.2634): MG samples use longer words on average.
- MG also has higher CTA density (d = -0.6926), politeness density (d = -0.7199), time-pressure density (d = -0.5959), TTR (d = -0.5962), and urgency density (d = -0.4027).
- HWT has higher Yule's K (d = 0.4334), indicating more word-frequency concentration under this corpus and tokenizer.
- Mean parse depth is essentially identical between HW and MG (d = 0.0049), while clause density and imperative count are also weak separators.


## Phishing versus benign

| Metric | P mean | B mean | Difference (P - B) | Cohen d |
|---|---:|---:|---:|---:|
| Authority density | 0.5005 | 0.4428 | 0.0577 | 0.0587 |
| Clause density | 1.7767 | 1.8722 | -0.0956 | -0.1609 |
| Cta density | 2.1522 | 0.8769 | 1.2753 | 0.6504 |
| First person ratio | 0.0340 | 0.0440 | -0.0100 | -0.3817 |
| Imperative count | 0.4724 | 0.3472 | 0.1252 | 0.1501 |
| Mean parse depth | 2.5634 | 2.6515 | -0.0881 | -0.1125 |
| Mean sentence len tokens | 17.1585 | 18.5662 | -1.4078 | -0.1607 |
| Mean word len | 5.1808 | 5.1099 | 0.0709 | 0.1191 |
| Noun ratio | 0.1782 | 0.1785 | -0.0004 | -0.0082 |
| Politeness density | 2.1180 | 1.9484 | 0.1696 | 0.0954 |
| Second person ratio | 0.0453 | 0.0274 | 0.0179 | 0.7077 |
| Time pressure density | 0.4912 | 0.2339 | 0.2572 | 0.3433 |
| Ttr | 0.7406 | 0.6934 | 0.0472 | 0.3768 |
| Urgency density | 1.2205 | 0.4196 | 0.8010 | 0.6308 |
| Verb ratio | 0.1051 | 0.1050 | 0.0001 | 0.0021 |
| Yules k | 130.8468 | 111.6264 | 19.2204 | 0.0879 |

### Outstanding observations

- Second-person ratio is the strongest Phishing/Benign difference (d = 1.9366): phishing samples address the reader much more directly.
- CTA density is also substantially higher for phishing (d = 1.1614), followed by mean word length (d = 0.8909), urgency density (d = 0.6930), politeness density (d = 0.6458), and time-pressure density (d = 0.3853).
- Phishing samples have lower mean parse depth (d = -0.6220) and shorter mean sentences (d = -0.3389) than benign samples.
- Authority density (d = 0.0044), TTR (d = -0.0695), verb ratio (d = 0.0942), and first-person ratio (d = 0.0441) show little or no separation.

## Reproducibility

The complete per-sample values remain available in `matched_pool_44_phishing_metrics.json`.
