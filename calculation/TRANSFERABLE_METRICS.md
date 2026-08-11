# Transferable metric classification

This classification is based on [`FACTORIAL_TESTS.md`](FACTORIAL_TESTS.md),
using the four cells HW-P, MG-P, HW-B, and MG-B.

## Classification rule

- **Generation**: the metric changes in the same direction for HW-P -> MG-P
  and HW-B -> MG-B, while the generation x phishing interaction is not
  statistically supported after correction.
- **Intent**: the metric differs in the same direction for HW-P vs HW-B and
  MG-P vs MG-B, while the interaction is not statistically supported after
  correction.

The classification is not exclusive. A metric can appear in both types if it
has evidence for both a machine-generation effect and a phishing-intent
effect. “Strong” means both relevant cell effects have q < 0.05. “Provisional”
means only one cell effect has q < 0.05, but the direction is consistent. The
full direction-only candidate lists remain in `FACTORIAL_TESTS.md`.

## Strong transferable metrics

| Type | Feature group | Metric | Interpretation |
|---|---|---|---|
| Generation | HWT-MGT | `total_surprisal` | Consistent generation-related shift in phishing and benign text |
| Generation | Stylometric | `surface_special_character_ratio` | Consistent generation-related surface-style shift |
| Generation | Stylometric | `surface_uppercase_ratio` | Consistent generation-related capitalization shift |
| Generation | Stylometric | `syntactic_brackets` | Consistent generation-related punctuation/structure shift |
| Generation | Stylometric | `surface_letter_ratio` | Consistent generation-related character-composition shift |
| Generation | Stylometric | `surface_uppercase_count` | Consistent generation-related capitalization-count shift |
| Generation | Stylometric | `surface_comma_percentage` | Consistent generation-related punctuation shift |
| Intent | Phishing | `second_person_ratio` | Consistent phishing-related reader-address shift in HW and MG text |
| Intent | Stylometric | `lda_assignment_topic_4` | Consistent topic-assignment difference associated with phishing |
| Intent | Stylometric | `pos_possessive_pronouns` | Consistent possessive-pronoun difference associated with phishing |
| Intent | Stylometric | `vocabulary_ratio_short_words` | Consistent short-word-ratio difference associated with phishing |

## Provisional transferable metrics

These have consistent cross-cell direction and no detected interaction, but
only one of the two relevant cell effects passed the q < 0.05 threshold.

### Generation-related

| Feature group | Metrics |
|---|---|
| HWT-MGT | `weighted_ngram_score`, `ngram_overlap_ratio`, `lrr`, `mean_log_rank`, `negative_mean_log_rank`, `phd_intrinsic_dimension`, `rank_100_1000_ratio`, `average_log_probability`, `rank_gt1000_ratio`, `mle_intrinsic_dimension`, `dna_gpt_regeneration_log_probability_difference` |
| Phishing | `mean_word_len`, `politeness_density` |
| Stylometric | `pos_possessive_pronouns`, `vocabulary_simpson_d`, `vocabulary_yule_k`, `surface_whitespace_ratio`, `vocabulary_brunet_w`, `lda_assignment_topic_4`, `pos_adverbs`, `lda_topic_4` |

### Intent-related

| Feature group | Metrics |
|---|---|
| HWT-MGT | `probability_fraction`, `average_log_probability` |
| Phishing | `mean_word_len`, `politeness_density`, `cta_density` |
| Stylometric | `lda_topic_4`, `surface_letter_ratio`, `surface_special_character_ratio`, `pos_determiners`, `syntactic_apostrophe`, `lda_assignment_topic_1` |

## Features with evidence of interaction

These should not be treated as universally transferable without further
validation because their behavior changes between human and machine text:

- Phishing `mean_sentence_len_tokens`
- Stylometric `sentence_mean_sentence_length`
- Stylometric `vocabulary_average_sentence_length_characters`
- Stylometric `vocabulary_average_sentence_length_words`
- Stylometric `syntactic_full_stop`

## Recommended use

For a transferable detector, start with the strong metrics and validate the
provisional metrics on held-out LLMs, phishing topics, and datasets. Keep
generation and intent features separate when evaluating transfer: generation
features should remain stable across phishing/benign domain changes, while
intent features should remain stable across human/machine authorship changes.

These are exploratory results from 11 observations per cell. They identify
shortlist candidates, not universal causal markers or fixed classification
thresholds.
