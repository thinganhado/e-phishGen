# Stylometric descriptive comparison

This report summarizes recoverable Stylometric features for `matched_pool_44.json`; individual sample rows are intentionally omitted.

## Dataset and settings

- Total samples: **8980**
- `HW-P`: **2245**; `MG-P`: **2245**
- `HW-B`: **2245**; `MG-B`: **2245**
- English NLTK tokenization, sentence splitting, and POS tagging were used.
- Character n-grams use a deterministic character-ID mapping and report counts/uniques, not a recovered neural model score.
- LDA uses a newly fitted 5-topic scikit-learn model on this 44-document dataset; it is not an original recovered LDA-C model.
- Difference is left mean minus right mean; Cohen d is descriptive, not a significance test.

## HWT versus MGT

| Metric | HW mean | MG mean | Difference (HW - MG) | Cohen d |
|---|---:|---:|---:|---:|
| Character 2gram count | 1267.8715 | 643.7766 | 624.0949 | 0.7945 |
| Character 2gram unique | 317.2058 | 243.0624 | 74.1434 | 0.7659 |
| Character 3gram count | 1266.8715 | 642.7766 | 624.0949 | 0.7945 |
| Character 3gram unique | 622.2918 | 451.3477 | 170.9441 | 0.6025 |
| Character 4gram count | 1265.8715 | 641.7766 | 624.0949 | 0.7945 |
| Character 4gram unique | 794.5630 | 537.1269 | 257.4361 | 0.6115 |
| Lda active topic count | 1.9773 | 1.1468 | 0.8305 | 1.2676 |
| Lda assignment topic 0 | 0.4531 | 0.2171 | 0.2360 | 1.8874 |
| Lda assignment topic 1 | 0.1957 | 0.0514 | 0.1444 | 1.3353 |
| Lda assignment topic 2 | 0.2150 | 0.7222 | -0.5072 | -6.7592 |
| Lda assignment topic 3 | 0.0450 | 0.0034 | 0.0416 | 0.4928 |
| Lda assignment topic 4 | 0.0911 | 0.0059 | 0.0852 | 0.8164 |
| Lda dominant topic mass | 0.7893 | 0.9706 | -0.1813 | -1.3227 |
| Lda per token likelihood bound | -1886.7292 | -1904.3661 | 17.6369 | 0.0110 |
| Lda topic 0 | 0.4407 | 0.0128 | 0.4279 | 1.6084 |
| Lda topic 1 | 0.3058 | 0.0083 | 0.2975 | 1.1434 |
| Lda topic 2 | 0.0396 | 0.9706 | -0.9310 | -13.7180 |
| Lda topic 3 | 0.0563 | 0.0030 | 0.0533 | 0.4176 |
| Lda topic 4 | 0.1577 | 0.0052 | 0.1525 | 0.7614 |
| Lda topic entropy | 0.5085 | 0.1279 | 0.3806 | 1.3856 |
| Pos adjectives | 12.4806 | 7.9229 | 4.5577 | 0.4945 |
| Pos adverbs | 6.8336 | 2.5641 | 4.2695 | 0.8119 |
| Pos cardinal numbers | 5.3047 | 0.5492 | 4.7555 | 0.3825 |
| Pos conjunctions | 5.2708 | 2.2606 | 3.0102 | 0.6809 |
| Pos density 1 | 16.5785 | 20.4715 | -3.8930 | -0.4603 |
| Pos density 2 | 49.9895 | 61.1027 | -11.1132 | -0.8313 |
| Pos density 3 | 73.6300 | 84.8809 | -11.2508 | -0.8596 |
| Pos determiners | 14.2980 | 6.9223 | 7.3757 | 0.6568 |
| Pos foreign words | 0.0967 | 0.0091 | 0.0875 | 0.2340 |
| Pos interrogatives | 1.6597 | 0.6009 | 1.0588 | 0.5910 |
| Pos nouns | 76.6307 | 36.9497 | 39.6811 | 0.8267 |
| Pos particles | 0.4837 | 0.3735 | 0.1102 | 0.1357 |
| Pos possessive pronouns | 3.2192 | 4.1962 | -0.9771 | -0.1896 |
| Pos prepositions | 22.9180 | 11.7702 | 11.1479 | 0.6557 |
| Pos symbols | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Pos verbs | 27.8650 | 16.3091 | 11.5559 | 0.6164 |
| Sentence mean sentence length | 149.5626 | 96.2178 | 53.3448 | 0.4418 |
| Sentence variance of sentence length | 26463.2272 | 2454.9793 | 24008.2479 | 0.2550 |
| Surface character count | 1234.1323 | 631.9697 | 602.1626 | 0.7873 |
| Surface character count without spaces | 1055.3004 | 543.7365 | 511.5639 | 0.7709 |
| Surface comma percentage | 0.7405 | 0.6311 | 0.1093 | 0.1778 |
| Surface digit count | 16.2755 | 1.2771 | 14.9984 | 0.2849 |
| Surface digit ratio | 1.0647 | 0.1892 | 0.8754 | 0.3624 |
| Surface letter ratio | 76.7744 | 83.2598 | -6.4854 | -1.5145 |
| Surface punctuation percentage | 2.2279 | 1.7771 | 0.4509 | 0.4903 |
| Surface question sentence percentage | 8.4295 | 3.6880 | 4.7415 | 0.3849 |
| Surface semicolon percentage | 0.0478 | 0.0014 | 0.0464 | 0.3204 |
| Surface space count | 178.8318 | 88.2332 | 90.5987 | 0.7790 |
| Surface special character ratio | 25.1669 | 18.6899 | 6.4770 | 1.7297 |
| Surface tab count | 1.7403 | 0.0002 | 1.7401 | 0.1909 |
| Surface tab ratio | 0.1268 | 0.0000 | 0.1268 | 0.2960 |
| Surface uppercase count | 212.0704 | 24.8537 | 187.2167 | 0.8831 |
| Surface uppercase ratio | 17.5046 | 4.1603 | 13.3442 | 1.4843 |
| Surface whitespace ratio | 14.4857 | 13.9581 | 0.5276 | 0.1865 |
| Syntactic apostrophe | 2.0929 | 1.6102 | 0.4826 | 0.1604 |
| Syntactic brackets | 43.1051 | 1.0548 | 42.0503 | 1.0288 |
| Syntactic colon | 4.0873 | 1.2793 | 2.8080 | 0.5293 |
| Syntactic comma | 10.3167 | 3.8813 | 6.4354 | 0.4322 |
| Syntactic dash | 3.2909 | 0.9969 | 2.2940 | 0.4504 |
| Syntactic ellipsis | 0.0016 | 0.0000 | 0.0016 | 0.0559 |
| Syntactic exclamation | 1.2911 | 0.4339 | 0.8572 | 0.4730 |
| Syntactic full stop | 9.2011 | 5.3343 | 3.8668 | 0.5594 |
| Syntactic question mark | 0.7570 | 0.2218 | 0.5352 | 0.4844 |
| Syntactic semicolon | 0.6588 | 0.0096 | 0.6492 | 0.2626 |
| Syntactic slash | 1.2940 | 0.0100 | 1.2840 | 0.4557 |
| Vocabulary average sentence length characters | 149.5626 | 96.2178 | 53.3448 | 0.4418 |
| Vocabulary average sentence length words | 21.3802 | 14.8091 | 6.5710 | 0.4429 |
| Vocabulary average word length | 6.8314 | 6.5721 | 0.2593 | 0.2630 |
| Vocabulary brunet w | 10.1769 | 9.0789 | 1.0980 | 0.7534 |
| Vocabulary hapax legomena | 84.3824 | 69.1938 | 15.1886 | 0.3568 |
| Vocabulary honore r | 2721.0257 | 3775.8784 | -1054.8527 | -0.5424 |
| Vocabulary ratio short words | 35.8838 | 32.6767 | 3.2071 | 0.4188 |
| Vocabulary sichel s | 0.1245 | 0.0886 | 0.0359 | 0.7333 |
| Vocabulary simpson d | 0.0173 | 0.0055 | 0.0118 | 0.4622 |
| Vocabulary total unique words | 112.1846 | 80.2236 | 31.9610 | 0.5510 |
| Vocabulary total words | 188.9198 | 97.9499 | 90.9699 | 0.7912 |
| Vocabulary yule k | 3774.1140 | 5508.2875 | -1734.1735 | -1.1957 |

### Outstanding observations

- The largest HWT/MGT effects are surface and punctuation features: uppercase ratio (d = 2.0759), special-character ratio (d = 1.9629), bracket count (d = 1.7841), uppercase count (d = 1.7380), and letter ratio (d = -1.6313).
- HW has substantially more uppercase characters, brackets, special characters, and total characters. These differences may reflect formatting and template conventions rather than authorship alone.
- Vocabulary Yule K (d = -1.0484) and Brunet W (d = 0.9558) also show relatively strong authorship differences, while total unique-word count is effectively identical (d = -0.0143).
- POS features show higher HW adverb counts (d = 0.8382) and higher MG possessive-pronoun counts (d = -0.7136), but sentence mean length is almost identical (d = -0.0310).
- Character 2-gram uniqueness has moderate separation (d = 0.6392), whereas 3- and 4-gram uniqueness are nearly unchanged.


## Phishing versus benign

| Metric | P mean | B mean | Difference (P - B) | Cohen d |
|---|---:|---:|---:|---:|
| Character 2gram count | 887.4350 | 1024.2131 | -136.7782 | -0.1624 |
| Character 2gram unique | 268.5252 | 291.7430 | -23.2178 | -0.2254 |
| Character 3gram count | 886.4350 | 1023.2131 | -136.7782 | -0.1624 |
| Character 3gram unique | 505.6111 | 568.0283 | -62.4171 | -0.2118 |
| Character 4gram count | 885.4350 | 1022.2131 | -136.7782 | -0.1624 |
| Character 4gram unique | 623.0285 | 708.6615 | -85.6330 | -0.1954 |
| Lda active topic count | 1.6071 | 1.5169 | 0.0902 | 0.1165 |
| Lda assignment topic 0 | 0.3338 | 0.3364 | -0.0026 | -0.0150 |
| Lda assignment topic 1 | 0.0990 | 0.1481 | -0.0491 | -0.3844 |
| Lda assignment topic 2 | 0.4709 | 0.4664 | 0.0045 | 0.0171 |
| Lda assignment topic 3 | 0.0172 | 0.0312 | -0.0141 | -0.1624 |
| Lda assignment topic 4 | 0.0791 | 0.0179 | 0.0612 | 0.5638 |
| Lda dominant topic mass | 0.8652 | 0.8947 | -0.0295 | -0.1806 |
| Lda per token likelihood bound | -2089.9342 | -1701.1611 | -388.7731 | -0.2443 |
| Lda topic 0 | 0.2497 | 0.2038 | 0.0459 | 0.1346 |
| Lda topic 1 | 0.0808 | 0.2333 | -0.1525 | -0.5261 |
| Lda topic 2 | 0.5021 | 0.5081 | -0.0061 | -0.0129 |
| Lda topic 3 | 0.0187 | 0.0406 | -0.0218 | -0.1681 |
| Lda topic 4 | 0.1487 | 0.0142 | 0.1345 | 0.6611 |
| Lda topic entropy | 0.3445 | 0.2918 | 0.0527 | 0.1581 |
| Pos adjectives | 9.3786 | 11.0249 | -1.6463 | -0.1741 |
| Pos adverbs | 4.3225 | 5.0753 | -0.7528 | -0.1329 |
| Pos cardinal numbers | 3.2160 | 2.6379 | 0.5782 | 0.0457 |
| Pos conjunctions | 3.4171 | 4.1143 | -0.6971 | -0.1497 |
| Pos density 1 | 20.1488 | 16.9012 | 3.2476 | 0.3809 |
| Pos density 2 | 57.0221 | 54.0701 | 2.9521 | 0.2050 |
| Pos density 3 | 79.4559 | 79.0549 | 0.4010 | 0.0282 |
| Pos determiners | 9.2114 | 12.0089 | -2.7976 | -0.2383 |
| Pos foreign words | 0.0559 | 0.0499 | 0.0060 | 0.0160 |
| Pos interrogatives | 0.9007 | 1.3599 | -0.4592 | -0.2477 |
| Pos nouns | 53.5301 | 60.0503 | -6.5203 | -0.1258 |
| Pos particles | 0.3726 | 0.4846 | -0.1120 | -0.1379 |
| Pos possessive pronouns | 4.1098 | 3.3056 | 0.8042 | 0.1558 |
| Pos prepositions | 15.5410 | 19.1472 | -3.6062 | -0.2026 |
| Pos symbols | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Pos verbs | 19.2379 | 24.9363 | -5.6984 | -0.2936 |
| Sentence mean sentence length | 119.6749 | 126.1055 | -6.4306 | -0.0520 |
| Sentence variance of sentence length | 13247.0515 | 15671.1550 | -2424.1035 | -0.0255 |
| Surface character count | 865.3448 | 1000.7572 | -135.4125 | -0.1653 |
| Surface character count without spaces | 745.9042 | 853.1327 | -107.2285 | -0.1512 |
| Surface comma percentage | 0.7313 | 0.6403 | 0.0910 | 0.1478 |
| Surface digit count | 10.8107 | 6.7419 | 4.0688 | 0.0766 |
| Surface digit ratio | 0.7367 | 0.5172 | 0.2195 | 0.0895 |
| Surface letter ratio | 80.5721 | 79.4622 | 1.1099 | 0.2077 |
| Surface punctuation percentage | 2.0214 | 1.9836 | 0.0378 | 0.0399 |
| Surface question sentence percentage | 4.6502 | 7.4674 | -2.8172 | -0.2260 |
| Surface semicolon percentage | 0.0102 | 0.0390 | -0.0288 | -0.1969 |
| Surface space count | 119.4405 | 147.6245 | -28.1840 | -0.2273 |
| Surface special character ratio | 21.3973 | 22.4595 | -1.0622 | -0.2158 |
| Surface tab count | 0.1100 | 1.6305 | -1.5205 | -0.1666 |
| Surface tab ratio | 0.0097 | 0.1172 | -0.1075 | -0.2503 |
| Surface uppercase count | 122.4463 | 114.4777 | 7.9686 | 0.0344 |
| Surface uppercase ratio | 11.3334 | 10.3315 | 1.0019 | 0.0896 |
| Surface whitespace ratio | 13.8379 | 14.6059 | -0.7680 | -0.2728 |
| Syntactic apostrophe | 1.2570 | 2.4461 | -1.1891 | -0.4018 |
| Syntactic brackets | 19.7866 | 24.3733 | -4.5866 | -0.0999 |
| Syntactic colon | 2.1519 | 3.2147 | -1.0628 | -0.1946 |
| Syntactic comma | 7.4786 | 6.7194 | 0.7592 | 0.0499 |
| Syntactic dash | 1.5800 | 2.7078 | -1.1278 | -0.2173 |
| Syntactic ellipsis | 0.0016 | 0.0000 | 0.0016 | 0.0559 |
| Syntactic exclamation | 1.2227 | 0.5022 | 0.7205 | 0.3943 |
| Syntactic full stop | 6.4584 | 8.0771 | -1.6187 | -0.2270 |
| Syntactic question mark | 0.3439 | 0.6350 | -0.2911 | -0.2582 |
| Syntactic semicolon | 0.1285 | 0.5399 | -0.4114 | -0.1656 |
| Syntactic slash | 0.3889 | 0.9151 | -0.5263 | -0.1829 |
| Vocabulary average sentence length characters | 119.6749 | 126.1055 | -6.4306 | -0.0520 |
| Vocabulary average sentence length words | 17.5875 | 18.6018 | -1.0144 | -0.0668 |
| Vocabulary average word length | 6.7531 | 6.6503 | 0.1028 | 0.1036 |
| Vocabulary brunet w | 9.3884 | 9.8675 | -0.4791 | -0.3113 |
| Vocabulary hapax legomena | 74.4503 | 79.1258 | -4.6755 | -0.1083 |
| Vocabulary honore r | 3625.3809 | 2871.5233 | 753.8576 | 0.3808 |
| Vocabulary ratio short words | 32.6819 | 35.8786 | -3.1968 | -0.4174 |
| Vocabulary sichel s | 0.0953 | 0.1178 | -0.0225 | -0.4409 |
| Vocabulary simpson d | 0.0132 | 0.0097 | 0.0035 | 0.1352 |
| Vocabulary total unique words | 90.9935 | 101.4147 | -10.4212 | -0.1739 |
| Vocabulary total words | 131.8383 | 155.0314 | -23.1931 | -0.1884 |
| Vocabulary yule k | 4990.7625 | 4291.6390 | 699.1235 | 0.4229 |

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
