# Stylometric descriptive comparison

This report summarizes recoverable Stylometric features for `matched_pool_44.json`; individual sample rows are intentionally omitted.

## Dataset and settings

- Total samples: **44**
- `HW-P`: **11**; `MG-P`: **11**
- `HW-B`: **11**; `MG-B`: **11**
- English NLTK tokenization, sentence splitting, and POS tagging were used.
- Character n-grams use a deterministic character-ID mapping and report counts/uniques, not a recovered neural model score.
- LDA uses a newly fitted 5-topic scikit-learn model on this 44-document dataset; it is not an original recovered LDA-C model.
- Difference is left mean minus right mean; Cohen d is descriptive, not a significance test.

## HWT versus MGT

| Metric | HW mean | MG mean | Difference (HW - MG) | Cohen d |
|---|---:|---:|---:|---:|
| Character 2gram count | 672.1364 | 615.0000 | 57.1364 | 0.4021 |
| Character 2gram unique | 253.5909 | 234.2273 | 19.3636 | 0.6392 |
| Character 3gram count | 671.1364 | 614.0000 | 57.1364 | 0.4021 |
| Character 3gram unique | 436.0455 | 430.3182 | 5.7273 | 0.0833 |
| Character 4gram count | 670.1364 | 613.0000 | 57.1364 | 0.4021 |
| Character 4gram unique | 513.2273 | 506.5909 | 6.6364 | 0.0746 |
| Lda active topic count | 1.3182 | 1.0909 | 0.2273 | 0.4526 |
| Lda assignment topic 0 | 0.2561 | 0.1310 | 0.1251 | 0.6441 |
| Lda assignment topic 1 | 0.1729 | 0.1614 | 0.0115 | 0.0578 |
| Lda assignment topic 2 | 0.0605 | 0.0590 | 0.0014 | 0.0130 |
| Lda assignment topic 3 | 0.0176 | 0.0000 | 0.0176 | 0.3015 |
| Lda assignment topic 4 | 0.4929 | 0.6485 | -0.1556 | -0.6550 |
| Lda dominant topic mass | 0.8962 | 0.9638 | -0.0676 | -0.4682 |
| Lda per token likelihood bound | -30.3046 | -32.0418 | 1.7372 | 0.2933 |
| Lda topic 0 | 0.3297 | 0.1276 | 0.2021 | 0.5202 |
| Lda topic 1 | 0.2269 | 0.2365 | -0.0096 | -0.0227 |
| Lda topic 2 | 0.0962 | 0.1101 | -0.0139 | -0.0520 |
| Lda topic 3 | 0.0263 | 0.0022 | 0.0242 | 0.2996 |
| Lda topic 4 | 0.3209 | 0.5236 | -0.2027 | -0.4404 |
| Lda topic entropy | 0.2288 | 0.1145 | 0.1143 | 0.4372 |
| Pos adjectives | 6.0455 | 6.3636 | -0.3182 | -0.1309 |
| Pos adverbs | 3.5909 | 2.0000 | 1.5909 | 0.8382 |
| Pos cardinal numbers | 0.3182 | 1.0000 | -0.6818 | -0.6327 |
| Pos conjunctions | 2.5909 | 1.8636 | 0.7273 | 0.5027 |
| Pos density 1 | 18.2733 | 20.4510 | -2.1777 | -0.5461 |
| Pos density 2 | 57.2728 | 59.6611 | -2.3883 | -0.3902 |
| Pos density 3 | 80.9541 | 83.9831 | -3.0290 | -0.4896 |
| Pos determiners | 7.1818 | 6.0455 | 1.1364 | 0.3747 |
| Pos foreign words | 0.0000 | 0.0455 | -0.0455 | -0.3015 |
| Pos interrogatives | 0.7727 | 0.5455 | 0.2273 | 0.2056 |
| Pos nouns | 43.0455 | 39.2273 | 3.8182 | 0.4148 |
| Pos particles | 0.4091 | 0.5000 | -0.0909 | -0.1183 |
| Pos possessive pronouns | 2.9545 | 4.9545 | -2.0000 | -0.7136 |
| Pos prepositions | 12.9545 | 11.5455 | 1.4091 | 0.3810 |
| Pos symbols | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Pos verbs | 16.9545 | 14.0455 | 2.9091 | 0.5711 |
| Sentence mean sentence length | 103.9468 | 104.9323 | -0.9855 | -0.0310 |
| Sentence variance of sentence length | 5057.8466 | 3018.2637 | 2039.5829 | 0.5417 |
| Surface character count | 673.1364 | 616.0000 | 57.1364 | 0.4021 |
| Surface character count without spaces | 569.0909 | 524.4091 | 44.6818 | 0.3646 |
| Surface comma percentage | 0.4070 | 0.6751 | -0.2681 | -1.3592 |
| Surface digit count | 0.7727 | 1.9545 | -1.1818 | -0.5178 |
| Surface digit ratio | 0.1075 | 0.3277 | -0.2202 | -0.5898 |
| Surface letter ratio | 79.2215 | 81.9921 | -2.7706 | -1.6313 |
| Surface punctuation percentage | 1.7376 | 1.8296 | -0.0920 | -0.2286 |
| Surface question sentence percentage | 5.2020 | 0.7576 | 4.4444 | 0.6443 |
| Surface semicolon percentage | 0.0087 | 0.0000 | 0.0087 | 0.3015 |
| Surface space count | 104.0455 | 91.5909 | 12.4545 | 0.6035 |
| Surface special character ratio | 20.5642 | 17.6802 | 2.8840 | 1.9629 |
| Surface tab count | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Surface tab ratio | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Surface uppercase count | 92.9545 | 26.2727 | 66.6818 | 1.7380 |
| Surface uppercase ratio | 13.3878 | 4.2868 | 9.1010 | 2.0759 |
| Surface whitespace ratio | 15.5806 | 14.8660 | 0.7146 | 0.7156 |
| Syntactic apostrophe | 1.0455 | 0.8182 | 0.2273 | 0.1930 |
| Syntactic brackets | 17.0000 | 2.9091 | 14.0909 | 1.7841 |
| Syntactic colon | 1.5909 | 1.8182 | -0.2273 | -0.1353 |
| Syntactic comma | 2.8636 | 4.1364 | -1.2727 | -0.8120 |
| Syntactic dash | 1.8182 | 1.2273 | 0.5909 | 0.2945 |
| Syntactic ellipsis | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Syntactic exclamation | 0.5909 | 0.0455 | 0.5455 | 0.8270 |
| Syntactic full stop | 5.8636 | 5.1818 | 0.6818 | 0.3126 |
| Syntactic question mark | 0.4091 | 0.0455 | 0.3636 | 0.5513 |
| Syntactic semicolon | 0.0455 | 0.0000 | 0.0455 | 0.3015 |
| Syntactic slash | 1.0000 | 0.0455 | 0.9545 | 0.5035 |
| Vocabulary average sentence length characters | 103.9468 | 104.9323 | -0.9855 | -0.0310 |
| Vocabulary average sentence length words | 16.5452 | 15.9673 | 0.5780 | 0.1079 |
| Vocabulary average word length | 6.4245 | 6.6364 | -0.2120 | -0.5153 |
| Vocabulary brunet w | 9.5963 | 9.1078 | 0.4885 | 0.9558 |
| Vocabulary hapax legomena | 60.5455 | 65.4091 | -4.8636 | -0.4552 |
| Vocabulary honore r | 2673.2553 | 3542.6872 | -869.4319 | -0.6415 |
| Vocabulary ratio short words | 33.9066 | 30.0937 | 3.8129 | 0.6307 |
| Vocabulary sichel s | 0.1243 | 0.1048 | 0.0195 | 0.3837 |
| Vocabulary simpson d | 0.0087 | 0.0062 | 0.0026 | 0.8950 |
| Vocabulary total unique words | 76.3636 | 76.5455 | -0.1818 | -0.0143 |
| Vocabulary total words | 104.5909 | 93.0455 | 11.5455 | 0.5518 |
| Vocabulary yule k | 4228.6177 | 5388.9934 | -1160.3757 | -1.0484 |

### Outstanding observations

- The largest HWT/MGT effects are surface and punctuation features: uppercase ratio (d = 2.0759), special-character ratio (d = 1.9629), bracket count (d = 1.7841), uppercase count (d = 1.7380), and letter ratio (d = -1.6313).
- HW has substantially more uppercase characters, brackets, special characters, and total characters. These differences may reflect formatting and template conventions rather than authorship alone.
- Vocabulary Yule K (d = -1.0484) and Brunet W (d = 0.9558) also show relatively strong authorship differences, while total unique-word count is effectively identical (d = -0.0143).
- POS features show higher HW adverb counts (d = 0.8382) and higher MG possessive-pronoun counts (d = -0.7136), but sentence mean length is almost identical (d = -0.0310).
- Character 2-gram uniqueness has moderate separation (d = 0.6392), whereas 3- and 4-gram uniqueness are nearly unchanged.


## Phishing versus benign

| Metric | P mean | B mean | Difference (P - B) | Cohen d |
|---|---:|---:|---:|---:|
| Character 2gram count | 640.0909 | 647.0455 | -6.9545 | -0.0480 |
| Character 2gram unique | 235.8636 | 251.9545 | -16.0909 | -0.5226 |
| Character 3gram count | 639.0909 | 646.0455 | -6.9545 | -0.0480 |
| Character 3gram unique | 424.1818 | 442.1818 | -18.0000 | -0.2640 |
| Character 4gram count | 638.0909 | 645.0455 | -6.9545 | -0.0480 |
| Character 4gram unique | 501.0455 | 518.7727 | -17.7273 | -0.2002 |
| Lda active topic count | 1.2727 | 1.1364 | 0.1364 | 0.2670 |
| Lda assignment topic 0 | 0.1232 | 0.2640 | -0.1408 | -0.7362 |
| Lda assignment topic 1 | 0.0864 | 0.2480 | -0.1616 | -0.8910 |
| Lda assignment topic 2 | 0.0363 | 0.0832 | -0.0469 | -0.4368 |
| Lda assignment topic 3 | 0.0000 | 0.0176 | -0.0176 | -0.3015 |
| Lda assignment topic 4 | 0.7542 | 0.3872 | 0.3670 | 2.2122 |
| Lda dominant topic mass | 0.8982 | 0.9618 | -0.0636 | -0.4392 |
| Lda per token likelihood bound | -32.1667 | -30.1797 | -1.9870 | -0.3366 |
| Lda topic 0 | 0.0941 | 0.3632 | -0.2691 | -0.7124 |
| Lda topic 1 | 0.0919 | 0.3715 | -0.2795 | -0.7022 |
| Lda topic 2 | 0.0593 | 0.1471 | -0.0878 | -0.3319 |
| Lda topic 3 | 0.0022 | 0.0263 | -0.0241 | -0.2994 |
| Lda topic 4 | 0.7525 | 0.0919 | 0.6606 | 2.0063 |
| Lda topic entropy | 0.2184 | 0.1249 | 0.0935 | 0.3549 |
| Pos adjectives | 6.2273 | 6.1818 | 0.0455 | 0.0187 |
| Pos adverbs | 3.1364 | 2.4545 | 0.6818 | 0.3349 |
| Pos cardinal numbers | 0.3636 | 0.9545 | -0.5909 | -0.5413 |
| Pos conjunctions | 2.0455 | 2.4091 | -0.3636 | -0.2453 |
| Pos density 1 | 19.7206 | 19.0037 | 0.7169 | 0.1738 |
| Pos density 2 | 58.0894 | 58.8445 | -0.7551 | -0.1212 |
| Pos density 3 | 81.8020 | 83.1352 | -1.3332 | -0.2102 |
| Pos determiners | 4.9091 | 8.3182 | -3.4091 | -1.3382 |
| Pos foreign words | 0.0455 | 0.0000 | 0.0455 | 0.3015 |
| Pos interrogatives | 0.2727 | 1.0455 | -0.7727 | -0.7439 |
| Pos nouns | 40.8182 | 41.4545 | -0.6364 | -0.0677 |
| Pos particles | 0.1364 | 0.7727 | -0.6364 | -0.9119 |
| Pos possessive pronouns | 5.7273 | 2.1818 | 3.5455 | 1.4968 |
| Pos prepositions | 11.3182 | 13.1818 | -1.8636 | -0.5113 |
| Pos symbols | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Pos verbs | 14.2273 | 16.7727 | -2.5455 | -0.4948 |
| Sentence mean sentence length | 100.6501 | 108.2289 | -7.5788 | -0.2402 |
| Sentence variance of sentence length | 3077.7378 | 4998.3726 | -1920.6348 | -0.5079 |
| Surface character count | 641.0909 | 648.0455 | -6.9545 | -0.0480 |
| Surface character count without spaces | 546.7273 | 546.7727 | -0.0455 | -0.0004 |
| Surface comma percentage | 0.5029 | 0.5792 | -0.0763 | -0.3217 |
| Surface digit count | 0.9545 | 1.7727 | -0.8182 | -0.3521 |
| Surface digit ratio | 0.1450 | 0.2903 | -0.1454 | -0.3797 |
| Surface letter ratio | 81.4583 | 79.7554 | 1.7029 | 0.8374 |
| Surface punctuation percentage | 1.7323 | 1.8349 | -0.1025 | -0.2553 |
| Surface question sentence percentage | 1.6414 | 4.3182 | -2.6768 | -0.3752 |
| Surface semicolon percentage | 0.0087 | 0.0000 | 0.0087 | 0.3015 |
| Surface space count | 94.3636 | 101.2727 | -6.9091 | -0.3242 |
| Surface special character ratio | 18.3968 | 19.8476 | -1.4508 | -0.7456 |
| Surface tab count | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Surface tab ratio | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Surface uppercase count | 53.2273 | 66.0000 | -12.7727 | -0.2508 |
| Surface uppercase ratio | 7.7903 | 9.8844 | -2.0941 | -0.3321 |
| Surface whitespace ratio | 14.8373 | 15.6092 | -0.7719 | -0.7818 |
| Syntactic apostrophe | 0.5455 | 1.3182 | -0.7727 | -0.6930 |
| Syntactic brackets | 8.7273 | 11.1818 | -2.4545 | -0.2311 |
| Syntactic colon | 1.6364 | 1.7727 | -0.1364 | -0.0810 |
| Syntactic comma | 3.2273 | 3.7727 | -0.5455 | -0.3258 |
| Syntactic dash | 1.3182 | 1.7273 | -0.4091 | -0.2027 |
| Syntactic ellipsis | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Syntactic exclamation | 0.3182 | 0.3182 | 0.0000 | 0.0000 |
| Syntactic full stop | 5.8182 | 5.2273 | 0.5909 | 0.2700 |
| Syntactic question mark | 0.0909 | 0.3636 | -0.2727 | -0.4065 |
| Syntactic semicolon | 0.0455 | 0.0000 | 0.0455 | 0.3015 |
| Syntactic slash | 0.1818 | 0.8636 | -0.6818 | -0.3539 |
| Vocabulary average sentence length characters | 100.6501 | 108.2289 | -7.5788 | -0.2402 |
| Vocabulary average sentence length words | 15.2026 | 17.3099 | -2.1073 | -0.4008 |
| Vocabulary average word length | 6.6941 | 6.3668 | 0.3273 | 0.8369 |
| Vocabulary brunet w | 9.3017 | 9.4024 | -0.1007 | -0.1778 |
| Vocabulary hapax legomena | 61.0000 | 64.9545 | -3.9545 | -0.3668 |
| Vocabulary honore r | 2979.2940 | 3236.6485 | -257.3545 | -0.1812 |
| Vocabulary ratio short words | 28.5181 | 35.4822 | -6.9642 | -1.3244 |
| Vocabulary sichel s | 0.1089 | 0.1202 | -0.0112 | -0.2185 |
| Vocabulary simpson d | 0.0082 | 0.0067 | 0.0014 | 0.4673 |
| Vocabulary total unique words | 73.6364 | 79.2727 | -5.6364 | -0.4544 |
| Vocabulary total words | 95.2727 | 102.3636 | -7.0909 | -0.3308 |
| Vocabulary yule k | 4734.4464 | 4883.1648 | -148.7184 | -0.1186 |

### Outstanding observations

- The strongest phishing/benign differences come from the newly fitted LDA model: assignment topic 4 (d = 2.2122) and topic 4 proportion (d = 2.0063). These are dataset-specific topic coordinates, not universal linguistic meanings.
- POS possessive-pronoun count (d = 1.4968) is higher for phishing, while determiners (d = -1.3382), particles (d = -0.9119), and interrogatives (d = -0.7439) are higher for benign text.
- Benign samples have higher character 2-gram uniqueness (d = -0.5226), longer mean sentences (d = -0.2402), more short words (d = -1.3244), and more total words (d = -0.3308).
- Phishing samples have a higher letter ratio (d = 0.8374) and average word length (d = 0.8369), while total character count is almost identical (d = -0.0480).
- Several basic features show little phishing/benign separation, including character count without spaces (d = -0.0004), POS adjectives (d = 0.0187), POS nouns (d = -0.0677), and sentence length variance only has a moderate effect (d = -0.5079).


## Interpretation

- Positive `HW - MG` means the metric is higher for human-written text; negative means it is higher for machine-generated text.
- Positive `P - B` means the metric is higher for phishing text; negative means it is higher for benign text.
- Topic coordinates are model-specific and should not be interpreted semantically without inspecting the fitted vocabulary.
- This output does not include unavailable RST, entity-grid, author-topic, character-embedding, or trained neural n-gram metrics.
- The complete per-sample values are available in the JSON file.
