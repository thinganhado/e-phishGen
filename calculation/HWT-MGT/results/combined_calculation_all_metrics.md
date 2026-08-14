# Combined calculation descriptive comparison

This report consolidates the three completed analyses for the combined dataset.
Individual sample values are omitted here; complete values remain in each group's JSON output.

## Dataset and notation

- Total samples: **2352**
- `HW-P`: **168**; `MG-P`: **1008**
- `HW-B`: **168**; `MG-B`: **1008**
- Difference is calculated as left mean minus right mean.
- Cohen d is a descriptive standardized effect size, not a significance test.

# 1. HWT/MGT calculation

This section uses the completed HWT/MGT model-based metrics.

## HWT versus MGT

This pools phishing and benign samples: `HW = HW-P + HW-B` and `MG = MG-P + MG-B`.

| Metric | HW mean | MG mean | Difference (HW - MG) | Cohen d |
|---|---:|---:|---:|---:|
| Average log probability | -3.2478 | -2.9599 | -0.2878 | -0.7544 |
| Detectgpt discrepancy | 0.0232 | 0.0290 | -0.0057 | -0.0938 |
| Detectgpt normalized discrepancy | 0.2178 | 0.3826 | -0.1648 | -0.2094 |
| Dna gpt regeneration log probability difference | -0.5989 | -0.4919 | -0.1069 | -0.2387 |
| Fast detectgpt analytic | -0.4553 | 0.1074 | -0.5628 | -0.3943 |
| Fast detectgpt sampling | 2.1062 | 2.2529 | -0.1467 | -0.5547 |
| Lrr | 2.0052 | 2.0704 | -0.0652 | -0.6549 |
| Mean log rank | 1.6289 | 1.4391 | 0.1898 | 0.7936 |
| Mean token rank | 171.7345 | 149.4112 | 22.3233 | 0.2130 |
| Mle intrinsic dimension | 11.5101 | 12.0218 | -0.5117 | -0.7093 |
| Negative mean log rank | -1.6289 | -1.4391 | -0.1898 | -0.7936 |
| Negative mean token rank | -171.7345 | -149.4112 | -22.3233 | -0.2130 |
| Ngram overlap ratio | 0.3215 | 0.3045 | 0.0170 | 0.3340 |
| Npr | 1.0126 | 1.0194 | -0.0068 | -0.2471 |
| Perplexity from causal log probs | 27.7747 | 20.8027 | 6.9720 | 0.7651 |
| Perplexity gpt2 large | 24.5678 | 18.3829 | 6.1850 | 0.7759 |
| Phd intrinsic dimension | 9.1860 | 9.7374 | -0.5514 | -0.3164 |
| Predictive entropy | 3.1322 | 2.9516 | 0.1806 | 0.7270 |
| Probability fraction | 0.5260 | 0.5594 | -0.0334 | -0.6761 |
| Rank 100 1000 ratio | 0.0723 | 0.0578 | 0.0145 | 0.5885 |
| Rank 10 100 ratio | 0.1677 | 0.1603 | 0.0075 | 0.2031 |
| Rank gt1000 ratio | 0.0314 | 0.0220 | 0.0094 | 0.7025 |
| Top10 entropy | 1.4397 | 1.4155 | 0.0241 | 0.3239 |
| Top10 rank ratio | 0.7285 | 0.7599 | -0.0313 | -0.6051 |
| Total surprisal | 353.4074 | 477.9356 | -124.5282 | -0.8616 |
| Uid diff | 3.0309 | 2.9286 | 0.1023 | 0.2575 |
| Uid diff2 | 17.4380 | 17.6442 | -0.2063 | -0.0410 |
| Uid max span | 3.4422 | 3.2299 | 0.2124 | 0.4218 |
| Uid mean | 3.0789 | 2.8070 | 0.2719 | 0.6986 |
| Uid min span | 2.8737 | 2.4393 | 0.4343 | 0.7950 |
| Uid variance | 9.7584 | 9.2291 | 0.5293 | 0.2271 |
| Weighted ngram score | 0.0018 | 0.0016 | 0.0002 | 0.0555 |

### Strongest descriptive separations

The five largest absolute Cohen d values are: `total_surprisal` (d = -0.8616), `uid_min_span` (d = 0.7950), `negative_mean_log_rank` (d = -0.7936), `mean_log_rank` (d = 0.7936), `perplexity_gpt2_large` (d = 0.7759).

## Phishing versus benign

This pools authorship sources: `P = HW-P + MG-P` and `B = HW-B + MG-B`.

| Metric | P mean | B mean | Difference (P - B) | Cohen d |
|---|---:|---:|---:|---:|
| Average log probability | -3.1347 | -2.8675 | -0.2672 | -0.7197 |
| Detectgpt discrepancy | 0.0267 | 0.0296 | -0.0028 | -0.0462 |
| Detectgpt normalized discrepancy | 0.3262 | 0.3918 | -0.0656 | -0.0832 |
| Dna gpt regeneration log probability difference | -0.6477 | -0.3666 | -0.2811 | -0.6582 |
| Fast detectgpt analytic | -0.0693 | 0.1233 | -0.1926 | -0.1340 |
| Fast detectgpt sampling | 2.1959 | 2.2680 | -0.0721 | -0.2699 |
| Lrr | 2.0210 | 2.1012 | -0.0803 | -0.8547 |
| Mean log rank | 1.5599 | 1.3725 | 0.1874 | 0.8151 |
| Mean token rank | 165.0552 | 140.1454 | 24.9098 | 0.2387 |
| Mle intrinsic dimension | 12.1375 | 11.7599 | 0.3777 | 0.5254 |
| Negative mean log rank | -1.5599 | -1.3725 | -0.1874 | -0.8151 |
| Negative mean token rank | -165.0552 | -140.1454 | -24.9098 | -0.2387 |
| Ngram overlap ratio | 0.2958 | 0.3180 | -0.0223 | -0.4449 |
| Npr | 1.0156 | 1.0212 | -0.0056 | -0.2027 |
| Perplexity from causal log probs | 24.7719 | 18.8254 | 5.9465 | 0.6642 |
| Perplexity gpt2 large | 21.9721 | 16.5607 | 5.4114 | 0.6934 |
| Phd intrinsic dimension | 9.8596 | 9.4576 | 0.4019 | 0.2307 |
| Predictive entropy | 3.0925 | 2.8623 | 0.2301 | 1.0047 |
| Probability fraction | 0.5357 | 0.5736 | -0.0379 | -0.8053 |
| Rank 100 1000 ratio | 0.0673 | 0.0525 | 0.0148 | 0.6153 |
| Rank 10 100 ratio | 0.1717 | 0.1510 | 0.0208 | 0.5870 |
| Rank gt1000 ratio | 0.0250 | 0.0217 | 0.0033 | 0.2444 |
| Top10 entropy | 1.4505 | 1.3875 | 0.0629 | 0.9238 |
| Top10 rank ratio | 0.7360 | 0.7748 | -0.0389 | -0.7897 |
| Total surprisal | 505.4726 | 414.8192 | 90.6533 | 0.6296 |
| Uid diff | 3.0240 | 2.8624 | 0.1617 | 0.4136 |
| Uid diff2 | 17.9084 | 17.3212 | 0.5872 | 0.1169 |
| Uid max span | 3.4012 | 3.1186 | 0.2826 | 0.5781 |
| Uid mean | 2.9845 | 2.7071 | 0.2774 | 0.7380 |
| Uid min span | 2.5808 | 2.4211 | 0.1597 | 0.2845 |
| Uid variance | 9.5228 | 9.0867 | 0.4361 | 0.1874 |
| Weighted ngram score | 0.0014 | 0.0019 | -0.0005 | -0.1328 |

### Strongest descriptive separations

The five largest absolute Cohen d values are: `predictive_entropy` (d = 1.0047), `top10_entropy` (d = 0.9238), `lrr` (d = -0.8547), `negative_mean_log_rank` (d = -0.8151), `mean_log_rank` (d = 0.8151).

## Annotation-group context

Pooled comparisons can be inspected against the four underlying groups here.

| Metric | HW-P | MG-P | HW-B | MG-B |
|---|---:|---:|---:|---:|
| Average log probability | -3.3823 | -3.0934 | -3.1132 | -2.8265 |
| Detectgpt discrepancy | 0.0279 | 0.0265 | 0.0186 | 0.0314 |
| Detectgpt normalized discrepancy | 0.2654 | 0.3364 | 0.1701 | 0.4288 |
| Dna gpt regeneration log probability difference | -0.7710 | -0.6272 | -0.4267 | -0.3566 |
| Fast detectgpt analytic | -0.3683 | -0.0194 | -0.5424 | 0.2343 |
| Fast detectgpt sampling | 2.0699 | 2.2169 | 2.1425 | 2.2889 |
| Lrr | 1.9571 | 2.0316 | 2.0533 | 2.1092 |
| Mean log rank | 1.7354 | 1.5307 | 1.5224 | 1.3475 |
| Mean token rank | 175.0581 | 163.3880 | 168.4110 | 135.4344 |
| Mle intrinsic dimension | 11.8383 | 12.1874 | 11.1819 | 11.8562 |
| Negative mean log rank | -1.7354 | -1.5307 | -1.5224 | -1.3475 |
| Negative mean token rank | -175.0581 | -163.3880 | -168.4110 | -135.4344 |
| Ngram overlap ratio | 0.3031 | 0.2945 | 0.3398 | 0.3144 |
| Npr | 1.0114 | 1.0163 | 1.0137 | 1.0224 |
| Perplexity from causal log probs | 31.5264 | 23.6462 | 24.0230 | 17.9592 |
| Perplexity gpt2 large | 28.1681 | 20.9395 | 20.9676 | 15.8262 |
| Phd intrinsic dimension | 9.5231 | 9.9156 | 8.8489 | 9.5591 |
| Predictive entropy | 3.2827 | 3.0608 | 2.9817 | 2.8424 |
| Probability fraction | 0.5028 | 0.5412 | 0.5492 | 0.5777 |
| Rank 100 1000 ratio | 0.0806 | 0.0651 | 0.0640 | 0.0506 |
| Rank 10 100 ratio | 0.1807 | 0.1702 | 0.1548 | 0.1503 |
| Rank gt1000 ratio | 0.0332 | 0.0237 | 0.0297 | 0.0204 |
| Top10 entropy | 1.4838 | 1.4449 | 1.3956 | 1.3862 |
| Top10 rank ratio | 0.7056 | 0.7410 | 0.7515 | 0.7787 |
| Total surprisal | 401.9024 | 522.7342 | 304.9124 | 433.1370 |
| Uid diff | 3.0744 | 3.0156 | 2.9874 | 2.8415 |
| Uid diff2 | 16.9782 | 18.0634 | 17.8978 | 17.2251 |
| Uid max span | 3.5909 | 3.3695 | 3.2918 | 3.0900 |
| Uid mean | 3.2144 | 2.9462 | 2.9434 | 2.6678 |
| Uid min span | 2.9091 | 2.5261 | 2.8378 | 2.3524 |
| Uid variance | 9.5160 | 9.5239 | 10.0009 | 8.9343 |
| Weighted ngram score | 0.0017 | 0.0014 | 0.0020 | 0.0019 |

# 2. Stylometric calculation

The complete descriptive Stylometric report follows.

## Stylometric results


This report summarizes recoverable Stylometric features for `matched_pool_44.json`; individual sample rows are intentionally omitted.

## Dataset and settings

- Total samples: **2352**
- `HW-P`: **168**; `MG-P`: **1008**
- `HW-B`: **168**; `MG-B`: **1008**
- English NLTK tokenization, sentence splitting, and POS tagging were used.
- Character n-grams use a deterministic character-ID mapping and report counts/uniques, not a recovered neural model score.
- LDA uses a newly fitted 5-topic scikit-learn model on this 44-document dataset; it is not an original recovered LDA-C model.
- Difference is left mean minus right mean; Cohen d is descriptive, not a significance test.

## HWT versus MGT

| Metric | HW mean | MG mean | Difference (HW - MG) | Cohen d |
|---|---:|---:|---:|---:|
| Character 2gram count | 504.9494 | 837.6424 | -332.6930 | -1.0414 |
| Character 2gram unique | 208.9137 | 258.0179 | -49.1042 | -1.2460 |
| Character 3gram count | 503.9494 | 836.6424 | -332.6930 | -1.0414 |
| Character 3gram unique | 355.7411 | 528.7207 | -172.9797 | -1.1997 |
| Character 4gram count | 502.9494 | 835.6424 | -332.6930 | -1.0414 |
| Character 4gram unique | 412.2143 | 661.3666 | -249.1523 | -1.1485 |
| Lda active topic count | 1.5119 | 1.9177 | -0.4058 | -0.5012 |
| Lda assignment topic 0 | 0.0457 | 0.0407 | 0.0050 | 0.0708 |
| Lda assignment topic 1 | 0.5564 | 0.5317 | 0.0246 | 0.1438 |
| Lda assignment topic 2 | 0.0615 | 0.0539 | 0.0075 | 0.0897 |
| Lda assignment topic 3 | 0.0316 | 0.0286 | 0.0030 | 0.0514 |
| Lda assignment topic 4 | 0.3049 | 0.3450 | -0.0401 | -0.2323 |
| Lda dominant topic mass | 0.8639 | 0.8029 | 0.0610 | 0.3371 |
| Lda per token likelihood bound | -416.9578 | -278.4097 | -138.5481 | -1.1901 |
| Lda topic 0 | 0.1340 | 0.1110 | 0.0230 | 0.0890 |
| Lda topic 1 | 0.3498 | 0.3400 | 0.0098 | 0.0252 |
| Lda topic 2 | 0.1390 | 0.1230 | 0.0160 | 0.0627 |
| Lda topic 3 | 0.1023 | 0.0978 | 0.0045 | 0.0184 |
| Lda topic 4 | 0.2749 | 0.3283 | -0.0534 | -0.1436 |
| Lda topic entropy | 0.3261 | 0.4701 | -0.1440 | -0.4132 |
| Pos adjectives | 5.3929 | 10.7178 | -5.3249 | -0.9865 |
| Pos adverbs | 2.3065 | 4.6935 | -2.3869 | -0.7433 |
| Pos cardinal numbers | 1.2589 | 1.2316 | 0.0273 | 0.0185 |
| Pos conjunctions | 1.8423 | 2.8373 | -0.9950 | -0.4298 |
| Pos density 1 | 22.9511 | 16.5479 | 6.4033 | 1.2015 |
| Pos density 2 | 63.7867 | 56.7041 | 7.0826 | 0.8620 |
| Pos density 3 | 86.2019 | 83.4820 | 2.7199 | 0.4800 |
| Pos determiners | 5.9881 | 10.8859 | -4.8978 | -0.8728 |
| Pos foreign words | 0.0357 | 0.0293 | 0.0064 | 0.0273 |
| Pos interrogatives | 0.7708 | 1.0461 | -0.2753 | -0.2254 |
| Pos nouns | 30.1577 | 42.1265 | -11.9688 | -0.8743 |
| Pos particles | 0.4464 | 0.4296 | 0.0169 | 0.0226 |
| Pos possessive pronouns | 2.8839 | 5.5531 | -2.6691 | -0.8011 |
| Pos prepositions | 13.2857 | 19.9058 | -6.6200 | -0.7816 |
| Pos symbols | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Pos verbs | 14.0655 | 24.3373 | -10.2718 | -0.9493 |
| Sentence mean sentence length | 91.2672 | 97.3906 | -6.1234 | -0.2837 |
| Sentence variance of sentence length | 1842.1660 | 1798.5392 | 43.6268 | 0.0317 |
| Surface character count | 498.1369 | 825.8021 | -327.6652 | -1.0332 |
| Surface character count without spaces | 419.8125 | 700.3686 | -280.5561 | -1.0488 |
| Surface comma percentage | 0.8730 | 0.7279 | 0.1452 | 0.4835 |
| Surface digit count | 3.6458 | 3.6220 | 0.0238 | 0.0044 |
| Surface digit ratio | 0.7891 | 0.4967 | 0.2924 | 0.3590 |
| Surface letter ratio | 80.1354 | 81.6587 | -1.5232 | -0.8421 |
| Surface punctuation percentage | 1.9243 | 1.7764 | 0.1479 | 0.3526 |
| Surface question sentence percentage | 2.4744 | 1.5679 | 0.9064 | 0.1455 |
| Surface semicolon percentage | 0.0010 | 0.0023 | -0.0013 | -0.0838 |
| Surface space count | 78.3244 | 125.4335 | -47.1091 | -0.9290 |
| Surface special character ratio | 20.7187 | 19.5323 | 1.1864 | 0.7189 |
| Surface tab count | 0.0060 | 0.0045 | 0.0015 | 0.0134 |
| Surface tab ratio | 0.0009 | 0.0005 | 0.0004 | 0.0268 |
| Surface uppercase count | 28.0685 | 33.0347 | -4.9663 | -0.5651 |
| Surface uppercase ratio | 5.9467 | 4.4125 | 1.5342 | 0.9770 |
| Surface whitespace ratio | 15.7117 | 15.1338 | 0.5779 | 0.4784 |
| Syntactic apostrophe | 0.5685 | 0.4668 | 0.1017 | 0.1021 |
| Syntactic brackets | 5.0476 | 4.9603 | 0.0873 | 0.0416 |
| Syntactic colon | 0.1518 | 0.5208 | -0.3690 | -0.5590 |
| Syntactic comma | 4.2768 | 5.6840 | -1.4072 | -0.5586 |
| Syntactic dash | 0.5179 | 0.7743 | -0.2564 | -0.2264 |
| Syntactic ellipsis | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Syntactic exclamation | 0.7411 | 0.3606 | 0.3805 | 0.4284 |
| Syntactic full stop | 4.1607 | 7.5719 | -3.4112 | -0.9957 |
| Syntactic question mark | 0.1369 | 0.1116 | 0.0253 | 0.0660 |
| Syntactic semicolon | 0.0060 | 0.0243 | -0.0184 | -0.1236 |
| Syntactic slash | 0.1339 | 0.0972 | 0.0367 | 0.0951 |
| Vocabulary average sentence length characters | 91.2672 | 97.3906 | -6.1234 | -0.2837 |
| Vocabulary average sentence length words | 15.4003 | 15.7822 | -0.3820 | -0.1184 |
| Vocabulary average word length | 5.9948 | 6.2449 | -0.2501 | -0.5791 |
| Vocabulary brunet w | 9.1785 | 9.7632 | -0.5846 | -0.8548 |
| Vocabulary hapax legomena | 51.2143 | 78.8745 | -27.6602 | -1.1595 |
| Vocabulary honore r | 2426.8087 | 2773.7905 | -346.9818 | -0.4284 |
| Vocabulary ratio short words | 37.0851 | 35.0998 | 1.9853 | 0.3727 |
| Vocabulary sichel s | 0.1279 | 0.1079 | 0.0199 | 0.5263 |
| Vocabulary simpson d | 0.0089 | 0.0078 | 0.0010 | 0.3934 |
| Vocabulary total unique words | 63.9613 | 97.2922 | -33.3309 | -1.0985 |
| Vocabulary total words | 84.8452 | 134.6925 | -49.8472 | -0.9565 |
| Vocabulary yule k | 4452.4658 | 4182.9636 | 269.5022 | 0.2622 |

### Outstanding observations

- The largest HWT/MGT effects are surface and punctuation features: uppercase ratio (d = 2.0759), special-character ratio (d = 1.9629), bracket count (d = 1.7841), uppercase count (d = 1.7380), and letter ratio (d = -1.6313).
- HW has substantially more uppercase characters, brackets, special characters, and total characters. These differences may reflect formatting and template conventions rather than authorship alone.
- Vocabulary Yule K (d = -1.0484) and Brunet W (d = 0.9558) also show relatively strong authorship differences, while total unique-word count is effectively identical (d = -0.0143).
- POS features show higher HW adverb counts (d = 0.8382) and higher MG possessive-pronoun counts (d = -0.7136), but sentence mean length is almost identical (d = -0.0310).
- Character 2-gram uniqueness has moderate separation (d = 0.6392), whereas 3- and 4-gram uniqueness are nearly unchanged.


## Phishing versus benign

| Metric | P mean | B mean | Difference (P - B) | Cohen d |
|---|---:|---:|---:|---:|
| Character 2gram count | 831.9821 | 748.2474 | 83.7347 | 0.2481 |
| Character 2gram unique | 260.5527 | 241.4532 | 19.0995 | 0.4556 |
| Character 3gram count | 830.9821 | 747.2474 | 83.7347 | 0.2481 |
| Character 3gram unique | 530.8095 | 477.2092 | 53.6003 | 0.3479 |
| Character 4gram count | 829.9821 | 746.2474 | 83.7347 | 0.2481 |
| Character 4gram unique | 661.5281 | 590.0187 | 71.5094 | 0.3095 |
| Lda active topic count | 1.8342 | 1.8852 | -0.0510 | -0.0621 |
| Lda assignment topic 0 | 0.0459 | 0.0369 | 0.0090 | 0.1273 |
| Lda assignment topic 1 | 0.5363 | 0.5342 | 0.0021 | 0.0120 |
| Lda assignment topic 2 | 0.0398 | 0.0702 | -0.0303 | -0.3677 |
| Lda assignment topic 3 | 0.0364 | 0.0217 | 0.0146 | 0.2555 |
| Lda assignment topic 4 | 0.3416 | 0.3369 | 0.0047 | 0.0269 |
| Lda dominant topic mass | 0.8147 | 0.8086 | 0.0061 | 0.0337 |
| Lda per token likelihood bound | -279.1526 | -317.2520 | 38.0994 | 0.3056 |
| Lda topic 0 | 0.1280 | 0.1006 | 0.0274 | 0.1061 |
| Lda topic 1 | 0.3495 | 0.3332 | 0.0164 | 0.0419 |
| Lda topic 2 | 0.0745 | 0.1760 | -0.1015 | -0.4053 |
| Lda topic 3 | 0.1212 | 0.0756 | 0.0456 | 0.1859 |
| Lda topic 4 | 0.3267 | 0.3146 | 0.0121 | 0.0325 |
| Lda topic entropy | 0.4357 | 0.4635 | -0.0278 | -0.0790 |
| Pos adjectives | 10.6131 | 9.3010 | 1.3121 | 0.2313 |
| Pos adverbs | 4.7891 | 3.9158 | 0.8733 | 0.2655 |
| Pos cardinal numbers | 1.4184 | 1.0527 | 0.3656 | 0.2499 |
| Pos conjunctions | 2.8036 | 2.5867 | 0.2168 | 0.0927 |
| Pos density 1 | 16.6243 | 18.3010 | -1.6767 | -0.2931 |
| Pos density 2 | 57.0278 | 58.4041 | -1.3764 | -0.1609 |
| Pos density 3 | 83.4463 | 84.2949 | -0.8486 | -0.1481 |
| Pos determiners | 10.8588 | 9.5136 | 1.3452 | 0.2308 |
| Pos foreign words | 0.0391 | 0.0213 | 0.0179 | 0.0757 |
| Pos interrogatives | 1.1199 | 0.8937 | 0.2262 | 0.1854 |
| Pos nouns | 42.9677 | 37.8656 | 5.1020 | 0.3622 |
| Pos particles | 0.5349 | 0.3291 | 0.2058 | 0.2790 |
| Pos possessive pronouns | 4.9702 | 5.3733 | -0.4031 | -0.1167 |
| Pos prepositions | 19.7202 | 18.1998 | 1.5204 | 0.1738 |
| Pos symbols | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Pos verbs | 23.8937 | 21.8461 | 2.0476 | 0.1803 |
| Sentence mean sentence length | 98.5450 | 94.4866 | 4.0585 | 0.1880 |
| Sentence variance of sentence length | 1953.9713 | 1655.5720 | 298.3993 | 0.2178 |
| Surface character count | 820.4677 | 737.5179 | 82.9498 | 0.2478 |
| Surface character count without spaces | 696.1037 | 624.4745 | 71.6293 | 0.2534 |
| Surface comma percentage | 0.6927 | 0.8045 | -0.1118 | -0.3734 |
| Surface digit count | 4.1981 | 3.0527 | 1.1454 | 0.2150 |
| Surface digit ratio | 0.5830 | 0.4940 | 0.0890 | 0.1086 |
| Surface letter ratio | 81.5335 | 81.3486 | 0.1848 | 0.0981 |
| Surface punctuation percentage | 1.7344 | 1.8606 | -0.1262 | -0.3021 |
| Surface question sentence percentage | 2.2269 | 1.1680 | 1.0589 | 0.1704 |
| Surface semicolon percentage | 0.0030 | 0.0013 | 0.0017 | 0.1116 |
| Surface space count | 124.3639 | 113.0434 | 11.3206 | 0.2135 |
| Surface special character ratio | 19.5181 | 19.8854 | -0.3674 | -0.2172 |
| Surface tab count | 0.0000 | 0.0094 | -0.0094 | -0.0844 |
| Surface tab ratio | 0.0000 | 0.0011 | -0.0011 | -0.0845 |
| Surface uppercase count | 35.2628 | 29.3878 | 5.8750 | 0.6942 |
| Surface uppercase ratio | 4.7763 | 4.4870 | 0.2893 | 0.1750 |
| Surface whitespace ratio | 15.1143 | 15.3185 | -0.2042 | -0.1673 |
| Syntactic apostrophe | 0.5374 | 0.4252 | 0.1122 | 0.1128 |
| Syntactic brackets | 5.3980 | 4.5476 | 0.8503 | 0.4139 |
| Syntactic colon | 0.5604 | 0.3759 | 0.1845 | 0.2769 |
| Syntactic comma | 5.5000 | 5.4660 | 0.0340 | 0.0133 |
| Syntactic dash | 0.8053 | 0.6701 | 0.1352 | 0.1192 |
| Syntactic ellipsis | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Syntactic exclamation | 0.2772 | 0.5527 | -0.2755 | -0.3105 |
| Syntactic full stop | 7.5153 | 6.6539 | 0.8614 | 0.2391 |
| Syntactic question mark | 0.1548 | 0.0757 | 0.0791 | 0.2073 |
| Syntactic semicolon | 0.0298 | 0.0136 | 0.0162 | 0.1089 |
| Syntactic slash | 0.1811 | 0.0238 | 0.1573 | 0.4162 |
| Vocabulary average sentence length characters | 98.5450 | 94.4866 | 4.0585 | 0.1880 |
| Vocabulary average sentence length words | 16.0001 | 15.4553 | 0.5448 | 0.1693 |
| Vocabulary average word length | 6.2307 | 6.1876 | 0.0431 | 0.0978 |
| Vocabulary brunet w | 9.7226 | 9.6366 | 0.0860 | 0.1206 |
| Vocabulary hapax legomena | 79.7815 | 70.0646 | 9.7168 | 0.3843 |
| Vocabulary honore r | 2875.2932 | 2573.1502 | 302.1430 | 0.3753 |
| Vocabulary ratio short words | 34.6450 | 36.1219 | -1.4769 | -0.2775 |
| Vocabulary sichel s | 0.1077 | 0.1138 | -0.0061 | -0.1583 |
| Vocabulary simpson d | 0.0075 | 0.0084 | -0.0009 | -0.3304 |
| Vocabulary total unique words | 97.8946 | 87.1667 | 10.7279 | 0.3346 |
| Vocabulary total words | 134.1403 | 121.0026 | 13.1378 | 0.2408 |
| Vocabulary yule k | 4300.2307 | 4142.6971 | 157.5336 | 0.1531 |

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

# 3. Phishing calculation

The complete descriptive Phishing-feature report follows.

## Phishing results


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

## Source files

- HWT/MGT: `HWT-MGT/results/combined_calculation_metrics.json`
- Stylometric: `Stylometric/results/combined_calculation_stylometric_metrics.json`
- Phishing: `Phishing/results/combined_calculation_phishing_metrics.json`
