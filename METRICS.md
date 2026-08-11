# Metrics

This document records the metrics planned for `e-phishGen`, including their source implementations and any important differences.

## Entropy

Both source repositories use Shannon entropy with the natural logarithm, but they measure different probability distributions.

| Variant | Source repository | Probability distribution | Aggregation | Implementation direction |
|---|---|---|---|---|
| Top-10 entropy | [`detecting-fake-text`](https://github.com/HendrikStrobelt/detecting-fake-text) | The model's top 10 next-token probabilities, renormalized to sum to 1 | One entropy value per token; suitable for a distribution or visualization | Obtain top-k probabilities, keep the top 10, renormalize, then compute `-sum(p * log(p))` |
| Full-vocabulary entropy | [`MGTBench`](https://github.com/xinleihe/MGTBench) | The complete softmax distribution over the model vocabulary | Mean entropy across all predicted tokens; produces one scalar per text | Compute softmax over the full logits, then compute `-sum(p * log(p))` per position and average |

### Formulas

Top-10 variant:

```text
p' = top10_probabilities / sum(top10_probabilities)
H_top10 = -sum(p' * log(p'))
```

Full-vocabulary variant:

```text
p = softmax(logits)
H_full = mean(-sum(p * log(p)))
```

### Provenance and comparison

- Top-10 entropy follows `detecting-fake-text/client/src/ts/start.ts`.
- Full-vocabulary entropy follows `MGTBench/methods/metric_based.py`, `get_entropy`.
- DetectGPT also computes full-vocabulary entropy, but without MGTBench's explicit `max_length=512` truncation; this settings difference is documented below as a variant.
- The values are not directly comparable: truncating and renormalizing the distribution generally produces a lower, differently scaled entropy than full-vocabulary entropy.
- When adding this metric to `e-phishGen`, record which variant is used alongside the metric name (for example, `entropy_top10` or `entropy_full_vocab`).

### DetectGPT full-vocabulary variant

| Source repository | Implementation | Distribution and aggregation | Sequence handling |
|---|---|---|---|
| [`detect-gpt`](https://github.com/eric-mitchell/detect-gpt) | [`run.py`](https://github.com/eric-mitchell/detect-gpt/run.py) - `get_entropy` | Full-vocabulary softmax entropy, averaged across token positions | No explicit truncation or padding; relies on the model/tokenizer context handling |

## Perplexity

Perplexity is the exponentiated average negative log-likelihood of a tokenized sequence. This metric is defined for causal/autoregressive language models.

| Metric | Source/reference | Calculation direction | Important details |
|---|---|---|---|
| Perplexity | [Hugging Face: Perplexity of fixed-length models](https://huggingface.co/docs/transformers/en/perplexity) | Tokenize the text, evaluate next-token negative log-likelihood, average over valid target tokens, then compute `exp(average_NLL)` | Use a strided sliding window for sequences longer than the model context length; exclude overlapping context tokens from the loss | 

### Formula

```text
PPL(X) = exp(-1 / N * sum(log p(x_i | x_<i)))
```

### Implementation direction

- Use a causal language model and its matching tokenizer.
- For short text, calculate the loss directly with the token IDs as labels.
- For long text, use overlapping windows with a configurable stride, mask context-only labels with `-100`, and accumulate the negative log-likelihood and valid loss-token count across windows.
- Report the model, tokenizer, maximum context length, stride, and token count because tokenization and windowing affect the result.

## Average Log-Probability

Both repositories calculate the same metric: the average next-token log-probability under a causal language model.

| Source repository | Implementation | Formula | Sequence handling |
|---|---|---|---|
| [`MGTBench`](https://github.com/xinleihe/MGTBench) | [`methods/metric_based.py`](https://github.com/xinleihe/MGTBench/methods/metric_based.py) - `get_ll` | `-model(input_ids, labels=input_ids).loss` | Truncates to `max_length=1024`; enables padding |
| [`DetectLLM`](https://github.com/mbzuai-nlp/DetectLLM) | [`baselines/loss.py`](https://github.com/mbzuai-nlp/DetectLLM/baselines/loss.py) - `get_ll` | `-model(input_ids, labels=input_ids).loss` | Does not explicitly truncate or pad |

The causal language model internally shifts the labels, so both implementations evaluate the probability of each next token and average the resulting log-probabilities:

```text
AverageLogP = mean(log p(x_i | x_<i))
```

The returned values are typically negative; higher values indicate that the model assigns greater likelihood to the text. The implementations are mathematically equivalent for the same model, tokenizer, and effective token sequence. Results can differ for long texts because MGTBench truncates inputs at 1024 tokens, while DetectLLM relies on the model's own context handling. DetectLLM also contains a manual equivalent in [`baselines/utils/likelihood.py`](https://github.com/mbzuai-nlp/DetectLLM/baselines/utils/likelihood.py).

### DetectGPT OpenAI API variant

DetectGPT additionally supports an API-based version that obtains token log-probabilities from an OpenAI Completion API request rather than a local causal model. It uses `temperature=0`, `max_tokens=0`, `echo=True`, and removes the first returned token/log-probability before averaging. This is a settings variant of Average Log-Probability, not a new mathematical formula.

| Source repository | Implementation | Calculation direction |
|---|---|---|
| [`detect-gpt`](https://github.com/eric-mitchell/detect-gpt) | [`run.py`](https://github.com/eric-mitchell/detect-gpt/run.py) - `get_ll` | Request echoed token log-probabilities from the API, discard the initial prefix token, and compute `mean(token_logprobs)` |

## Token Rank

This metric is implemented in `detecting-fake-text` and is not currently represented in this document. It measures the rank assigned by the language model to the token that actually occurred in the text.

| Source repository | Implementation | Calculation direction | Output |
|---|---|---|---|
| [`detecting-fake-text`](https://github.com/HendrikStrobelt/detecting-fake-text) | [`backend/api.py`](https://github.com/HendrikStrobelt/detecting-fake-text/backend/api.py) - `LM.check_probabilities` | Sort the vocabulary probabilities for each position in descending order and find the position of the observed token | One zero-indexed rank per token; lower rank means the model considered the observed token more likely |

The repository visualizes rank buckets using thresholds at 10, 100, and 1000. The rank itself is distinct from Average Log-Probability because it retains only the token's ordering, not its probability magnitude.

## GLTR Rank-Bucket Ratios

The GLTR-style rank buckets exposed by `detecting-fake-text` can be converted into normalized text-level ratios. For each observed token, use its rank and count the proportion falling into each interval.

| Metric | Formula |
|---|---|
| `top10_rank_ratio` | `count(rank < 10) / N` |
| `rank_10_100_ratio` | `count(10 <= rank < 100) / N` |
| `rank_100_1000_ratio` | `count(100 <= rank < 1000) / N` |
| `rank_gt1000_ratio` | `count(rank >= 1000) / N` |

Implementation basis: [`backend/api.py`](https://github.com/HendrikStrobelt/detecting-fake-text/backend/api.py) and [`client/src/ts/vis/GLTR_Text_Box.ts`](https://github.com/HendrikStrobelt/detecting-fake-text/client/src/ts/vis/GLTR_Text_Box.ts), which use rank thresholds at 10, 100, and 1000. The four ratios sum to 1 when all scored tokens are included.

## Log-Rank Ratio (LRR)

LRR is a composite metric implemented by `DetectLLM`. It combines the average log-probability and average log-rank of the same text.

| Source repository | Formula | Calculation direction |
|---|---|---|
| [`DetectLLM`](https://github.com/mbzuai-nlp/DetectLLM) | `LRR = -AverageLogP / AverageLogRank` | Compute Average Log-Probability and Average Log-Rank for the text, then divide the negated log-probability by the log-rank |

Implementation: [`baselines/all_baselines.py`](https://github.com/mbzuai-nlp/DetectLLM/baselines/all_baselines.py) - `baseline == 'LRR'`. This is distinct from its component metrics because it measures their ratio.

## Normalized Log-Rank Perturbation (NPR)

NPR measures how much a text's average log-rank changes after perturbation.

| Source repository | Formula | Calculation direction |
|---|---|---|
| [`DetectLLM`](https://github.com/mbzuai-nlp/DetectLLM) | `NPR = AverageLogRank(perturbed text) / AverageLogRank(original text)` | Compute Average Log-Rank for the original text and each perturbed text, average the perturbed values, then divide by the original value |

Implementation: [`baselines/all_baselines.py`](https://github.com/mbzuai-nlp/DetectLLM/baselines/all_baselines.py) - `baseline == 'NPR'`.

The default DetectLLM settings are five perturbations, `span_length=2`, `pct_words_masked=0.3`, one perturbation round, T5-Small as the mask-filling model, `mask_top_p=1.0`, and `max_length=150` for mask generation. NPR is different from normalized likelihood discrepancy because it uses log-rank ratios rather than log-probability differences divided by perturbed-log-probability standard deviation.

## Probability Fraction (Frac(p))

This metric is implemented in `detecting-fake-text` and is not currently represented in this document. It measures how much probability the observed token receives relative to the model's most likely token at the same position.

| Source repository | Implementation | Formula | Output |
|---|---|---|---|
| [`detecting-fake-text`](https://github.com/HendrikStrobelt/detecting-fake-text) | [`client/src/ts/start.ts`](https://github.com/HendrikStrobelt/detecting-fake-text/client/src/ts/start.ts) - `fracs` | `Frac(p) = p(observed token) / p(top-1 token)` | One value per token in the range `[0, 1]`; 1 means the observed token is the top prediction |

This is not the same as Average Log-Probability: it is a relative probability ratio and does not measure the absolute probability assigned by the model.

## Average Rank and Average Log-Rank

`detect-gpt` implements aggregate rank metrics that differ from the existing per-token Token Rank metric. It uses one-indexed ranks and averages across the sequence.

| Metric | Source repository | Formula | Settings |
|---|---|---|---|
| Average Rank | [`detect-gpt`](https://github.com/eric-mitchell/detect-gpt) | `mean(rank(x_i))` | Rank is one-indexed; lower values indicate that observed tokens are ranked closer to the top |
| Average Log-Rank | [`detect-gpt`](https://github.com/eric-mitchell/detect-gpt) | `mean(log(rank(x_i)))` | Applies the natural logarithm to the one-indexed rank before averaging |

Implementation: [`run.py`](https://github.com/eric-mitchell/detect-gpt/run.py) - `get_rank`. These metrics are not duplicates of Token Rank because that entry documents zero-indexed, per-token ranks without sequence averaging or log transformation.

## Perturbation Log-Likelihood Discrepancy

This is the core perturbation-based DetectGPT metric and is not currently represented in this document. It compares a text's average log-probability with the average log-probability of texts generated after masking and filling spans.

| Variant | Formula | Interpretation |
|---|---|---|
| Discrepancy (`d`) | `d = LL(original) - mean(LL(perturbed_texts))` | Measures the drop in average log-probability after perturbation |
| Normalized discrepancy (`z`) | `z = d / std(LL(perturbed_texts))` | Normalizes the discrepancy by the variability among perturbed texts |

Implementation: [`run.py`](https://github.com/eric-mitchell/detect-gpt/run.py) - `get_perturbation_results` and `run_perturbation_experiment`.

Default settings are `span_length=2`, `pct_words_masked=0.3`, `n_perturbations=1` or `10`, `n_perturbation_rounds=1`, and T5-Large as the mask-filling model. The perturbations are generated independently for the original and sampled text, and the metric is evaluated using a separate base/scoring language model. The unnormalized discrepancy is also plotted under the label `log likelihood ratio`.

### DetectLLM normalized discrepancy variant

DetectLLM implements the normalized discrepancy formula above as its `DetectGPT` baseline, but with different perturbation settings: `span_length=2`, `pct_words_masked=0.3`, five perturbations by default, one perturbation round, and T5-Small as the default mask-filling model. Mask fills are sampled with `top_p=1.0` and generated with `max_length=150`. Because the formula is shared but these settings differ from the DetectGPT entry, this is documented as a variant rather than skipped.

## N-Gram Overlap

`DNA-GPT` uses lexical overlap between the latter half of an input text and a model-generated continuation. This is not present in the existing metrics because it compares text sequences directly rather than evaluating next-token probabilities.

| Variant | Source repository | Formula | Settings and output |
|---|---|---|---|
| N-gram overlap ratio | [`DNA-GPT`](https://github.com/Xianjun-Yang/DNA-GPT) | `r_n = sum(min(count_target(g), count_generated(g))) / sum(count_target(g))` | Computes overlap for n-grams with `n=1..24`; the detector uses the overlap score divided by the generated-token count |
| Weighted N-gram score | [`DNA-GPT`](https://github.com/Xianjun-Yang/DNA-GPT) | `score = sum(n * log(n) * r_n) / sum(n for nonzero r_n)` | Ignores n-grams of lengths 1-3 in the weighted score; produces one aggregate score across the n-gram lengths |

Implementation: [`DNA-GPT-dist.py`](https://github.com/Xianjun-Yang/DNA-GPT/DNA-GPT-dist.py) - `get_score_ngrams`, `get_ngram_info`, and `N_gram_detector`.

The implementation lowercases text, replaces non-alphanumeric characters with spaces, and applies Porter stemming to words longer than three characters. The demo truncates input to 350 words, uses the first 50% of the input as the generation prompt, generates up to 300 tokens, samples 30 continuations at temperature 0.7, and averages their weighted N-gram scores. The default decision threshold is `0.00025`.

## Regeneration Log-Probability Difference

DNA-GPT also evaluates whether an input's continuation has a different average token log-probability from continuations regenerated by a language model. This is related to Perturbation Log-Likelihood Discrepancy, but it uses continuation regeneration from a prefix rather than masked span perturbations.

| Source repository | Formula | Calculation direction | Settings |
|---|---|---|---|
| [`DNA-GPT`](https://github.com/Xianjun-Yang/DNA-GPT) | `D_regen = mean(LL(original continuation)) - mean(mean(LL(regenerated continuations)))` | Remove the prompt-prefix log-probabilities from the original response, average the remaining token log-probabilities, then subtract the mean per-token log-probability across regenerated completions | Notebook implementation uses 20 regenerated completions; the original and generated responses are scored using OpenAI token log-probabilities |

Implementation: [`openai_generate/my_detector_whitebox.ipynb`](https://github.com/Xianjun-Yang/DNA-GPT/openai_generate/my_detector_whitebox.ipynb) - `get_ratio_avgk`.

### Fast-DNA-GPT local-model variant

[`fast-detect-gpt`](https://github.com/baoguangsheng/fast-detect-gpt) implements the same regeneration-difference formula with a local sampling model rather than the OpenAI log-probability workflow. It uses a 50% prefix, generates `regen_number=10` continuations by default, and computes length-normalized log-probabilities with padding masked out. The default base model is GPT-2, with generation controlled by temperature 1.0, top-k 40, or top-p 0.96 when enabled.

Implementation: [`scripts/dna_gpt.py`](https://github.com/baoguangsheng/fast-detect-gpt/scripts/dna_gpt.py) - `get_dna_gpt`.

## GPT-Who Information-Density Features

`gpt-who` uses token surprisal to describe the local information density of a text. These features are not duplicates of Average Log-Probability: surprisal is the positive negative-log-probability quantity, and the implementation uses GPT-2 XL with an explicit leading EOS token.

For each scored token, the implementation computes:

```text
s_i = -log p(x_i | x_<i)
mu = mean(s_i)
```

| Feature | Source repository | Formula | Interpretation |
|---|---|---|---|
| Mean surprisal (`mean`) | [`gpt-who`](https://github.com/saranya-venkatraman/gpt-who) | `mean(s_i)` | Average information content per token; equivalent in magnitude to negative Average Log-Probability for this scoring setup |
| Total surprisal (`sum`) | [`gpt-who`](https://github.com/saranya-venkatraman/gpt-who) | `sum(s_i)` | Total negative log-probability; depends on both token surprisal and text length |
| UID variance (`uid_var`) | [`gpt-who`](https://github.com/saranya-venkatraman/gpt-who) | `sum((s_i - mu)^2) / N` | Dispersion of token-level surprisal across the text |
| UID local difference (`uid_diff`) | [`gpt-who`](https://github.com/saranya-venkatraman/gpt-who) | `sum(abs(s_(i+1) - s_i)) / N` | Average magnitude of adjacent surprisal changes |
| UID local squared difference (`uid_diff2`) | [`gpt-who`](https://github.com/saranya-venkatraman/gpt-who) | `sum((s_(i+1) - s_i)^2) / N` | Average squared adjacent surprisal change; emphasizes large transitions |

Implementation: [`get_uid_features.py`](https://github.com/saranya-venkatraman/gpt-who/get_uid_features.py) - `get_line_uid_surp`, `local_diff`, and `local_diff2`.

### UID span features

The downstream script divides the token-surprisal sequence into consecutive spans of 50 tokens, computes the variance within each complete span, and selects the minimum-variance and maximum-variance spans. The selected span values are concatenated with `uid_var`, `uid_diff`, `uid_diff2`, and `mean` as input to logistic regression.

| Feature group | Source repository | Calculation direction | Settings |
|---|---|---|---|
| Minimum/maximum UID spans | [`gpt-who`](https://github.com/saranya-venkatraman/gpt-who) | Compute `var(s_i)` for each complete span, then retain the span with minimum variance and the span with maximum variance | Span size is 50 tokens; texts with fewer than 50 scored tokens are excluded from the classifier stage |

Implementation: [`gpt-who.py`](https://github.com/saranya-venkatraman/gpt-who/gpt-who.py) - `spans`.

The feature extraction defaults to GPT-2 XL, prepends the tokenizer's EOS token before scoring, and does not set an explicit truncation limit. The logistic-regression classifier is a downstream model using these features, not itself a metric.

## Fast-DetectGPT Sampling Discrepancy

Fast-DetectGPT measures conditional probability curvature using a reference/sampling model and a scoring model. It compares the observed text's scoring-model log-likelihood with the scoring likelihood of tokens sampled from the reference distribution.

| Variant | Source repository | Formula | Calculation direction |
|---|---|---|---|
| Sampling discrepancy | [`fast-detect-gpt`](https://github.com/baoguangsheng/fast-detect-gpt) | `D_sample = (LL_score(x) - mean(LL_score(x_tilde))) / std(LL_score(x_tilde))` | Sample 10,000 token sequences from the reference model at each position, score those samples with the scoring model, then standardize the observed score |
| Analytic sampling discrepancy | [`fast-detect-gpt`](https://github.com/baoguangsheng/fast-detect-gpt) | `D_analytic = (sum(log p_score(x_i)) - sum(E_ref[log p_score])) / sqrt(sum(Var_ref[log p_score]))` | Compute the reference-distribution expectation and variance of scoring-model log-probabilities directly, avoiding explicit token sampling |

Implementation: [`scripts/fast_detect_gpt.py`](https://github.com/baoguangsheng/fast-detect-gpt/scripts/fast_detect_gpt.py) - `get_sampling_discrepancy` and `get_sampling_discrepancy_analytic`.

These metrics differ from Perturbation Log-Likelihood Discrepancy because their alternatives are sampled token sequences from a reference distribution, not masked-and-filled text perturbations. They also support separate reference and scoring models, enabling white-box and black-box settings. The sampling variant uses 10,000 samples per position and both variants align logits and labels for next-token scoring.

## Negative Average Rank and Negative Average Log-Rank

The fast repository includes rank baselines whose sign convention differs from the existing Average Rank and Average Log-Rank entries: it negates the sequence averages so that higher scores correspond to better detector direction.

| Metric | Source repository | Formula | Settings |
|---|---|---|---|
| Negative Average Rank | [`fast-detect-gpt`](https://github.com/baoguangsheng/fast-detect-gpt) | `-mean(rank(x_i))` | One-indexed ranks, next-token labels, no explicit truncation |
| Negative Average Log-Rank | [`fast-detect-gpt`](https://github.com/baoguangsheng/fast-detect-gpt) | `-mean(log(rank(x_i)))` | One-indexed ranks, natural log, no explicit truncation |

Implementation: [`scripts/baselines.py`](https://github.com/baoguangsheng/fast-detect-gpt/scripts/baselines.py) - `get_rank` and `get_logrank`.

## Embedding Intrinsic Dimension

`GPTID` estimates the intrinsic dimensionality of the manifold formed by a text's contextual token embeddings. This is a distinct family of metrics from the probability- and surprisal-based measures above.

| Variant | Source repository | Calculation direction | Settings |
|---|---|---|---|
| Persistence Homology Dimension (PHD) | [`GPTID`](https://github.com/ArGintum/GPTID) | Build Euclidean distances between sampled embedding points, compute minimum-spanning-tree lengths over increasing subsample sizes, fit the log-length versus log-size slope, and return `1 / (1 - slope)` | RoBERTa-base-cased `RobertaModel`; tokenize with truncation at 512 tokens; remove first/last special-token embeddings; `alpha=1.0`, Euclidean distance, `n_points=9`, minimum subsample 40, seven intermediate sample sizes |
| Maximum Likelihood Estimator (MLE) intrinsic dimension | [`GPTID`](https://github.com/ArGintum/GPTID) | Apply the scikit-dimension MLE estimator to the contextual embedding point cloud | Same RoBERTa-base-cased embeddings, 512-token truncation, and removal of first/last special-token embeddings; estimator uses the library defaults |

Implementation: [`IntrinsicDim.py`](https://github.com/ArGintum/GPTID/IntrinsicDim.py) for PHD and [`example.ipynb`](https://github.com/ArGintum/GPTID/example.ipynb) for the PHD/MLE pipelines.

The resulting value is one intrinsic-dimension estimate per text. The downstream logistic-regression detector described by GPTID is a classifier using these estimates, not itself a metric.

## Rough-list coverage

The requested rough list is fully covered after adding the GLTR rank-bucket ratios:

| Rough-list metric | Documented entry |
|---|---|
| `predictive_entropy` | Full-vocabulary Entropy; Top-10 Entropy is also documented |
| `perplexity` | Perplexity |
| `avg_log_probability` | Average Log-Probability |
| `mean_token_rank` | Average Rank |
| `mean_log_rank` | Average Log-Rank |
| `top10_rank_ratio`, `rank_10_100_ratio`, `rank_100_1000_ratio`, `rank_gt1000_ratio` | GLTR Rank-Bucket Ratios |
| `detectgpt_curvature` | Perturbation Log-Likelihood Discrepancy, especially normalized discrepancy (`z`) |
| `dna_gpt_score` | Regeneration Log-Probability Difference |
| `fast_detectgpt_criterion` | Fast-DetectGPT Sampling Discrepancy, including analytic form |
| `lrr`, `npr` | Log-Rank Ratio and Normalized Log-Rank Perturbation |
| `uid_mean`, `uid_variance`, `uid_diff`, `uid_diff2`, `uid_min_span`, `uid_max_span` | GPT-Who Information-Density Features and UID span features |
| `phd_intrinsic_dimension` | Persistence Homology Dimension (PHD) |

`METRICS.md` contains additional variants and metrics beyond this list, including MLE intrinsic dimension, total surprisal, probability fraction, n-gram overlap, API/local regeneration variants, and negative rank-sign variants.

## Reading scores for HWT vs. MGT

Here, HWT means human-written text and MGT means machine-generated text. “Higher means MGT” describes the usual direction reported by the source repository; it is not a universal threshold across models, tokenizers, datasets, or text lengths.

| Metric | How to read a higher value | Original-repository threshold |
|---|---|---|
| Predictive entropy | Usually more uncertainty; DetectLLM reports higher entropy for MGT | No universal cutoff; repositories evaluate it with learned threshold/ROC experiments |
| Perplexity | The scoring model finds the text less predictable | No HWT/MGT cutoff in the Hugging Face reference |
| Average Log-Probability | Text is more likely under the scoring model; DetectLLM reports higher values as more MGT-like | No universal cutoff; threshold is learned/evaluated from data |
| Mean Token Rank | Raw higher rank means the observed tokens are lower in the model's ordering; direction is model/data dependent | GLTR uses rank boundaries 10, 100, and 1000, not a single HWT/MGT cutoff |
| Mean Log-Rank | Same interpretation as rank after logarithmic compression | No universal cutoff; source uses evaluation thresholds |
| GLTR rank ratios | Higher `top10_rank_ratio` generally suggests MGT; higher `rank_gt1000_ratio` generally suggests HWT | Rank bucket boundaries are 10, 100, and 1000; no fixed ratio cutoff |
| DetectGPT curvature | The paper describes MGT as having more negative curvature; interpret the raw sign carefully because implementations may negate or standardize the score | No universal numeric cutoff; source evaluates thresholds from ROC/PR experiments |
| DNA-GPT score | Higher score means the original continuation is more likely than regenerated continuations; the source uses this as more MGT-like | Demo default: `0.00025` |
| Fast-DetectGPT criterion | Higher sampling/analytic discrepancy is more MGT-like | No single universal cutoff; the local demo calibrates normal distributions and reports `P(MGT)`; a probability above 0.5 is the natural balanced-prior decision point |
| LRR | Higher ratio is more MGT-like according to DetectLLM | No fixed numeric cutoff; compare LRR and NPR on a validation set |
| NPR | Higher perturbation log-rank ratio is more MGT-like | No fixed numeric cutoff; compare against a validation distribution |
| UID mean / variance / diff / diff2 | Higher means more surprisal or more local variation, but does not by itself imply HWT or MGT | No fixed threshold; GPT-Who trains logistic regression on the feature set |
| UID minimum/maximum spans | Higher values mean more or less variable local surprisal depending on the selected span; interpret through the trained classifier | No fixed threshold; classifier learns the decision boundary |
| PHD / MLE intrinsic dimension | Higher intrinsic dimension is generally more HWT-like; GPTID reports MGT dimensions about 1.5 lower on average for several settings | No universal cutoff; use the estimator distribution and a validation classifier |

### Additional documented metrics

- Higher Top-10 Entropy means a more dispersed top-10 distribution; the source uses it for visualization rather than a fixed HWT/MGT cutoff.
- Higher `Frac(p)` means the observed token is closer to the model's top prediction; this is generally more MGT-like, but the source does not define a classification threshold.
- Higher Total Surprisal means lower overall likelihood and is length-dependent; it should not be thresholded without length normalization.
- Higher N-gram overlap or Weighted N-gram Score means more overlap with a generated continuation; DNA-GPT uses a default score threshold of `0.00025` for its demo.
- Higher Negative Average Rank or Negative Average Log-Rank means better model rank after sign reversal; these are detector-oriented versions of the raw rank metrics.

For comparisons across HWT and MGT, calibrate thresholds using the same scoring model, tokenizer, text-length policy, and dataset split used for evaluation. A source-repository threshold should not be transferred directly to a different model or corpus.

## Original model, tokenizer, and input settings

The calculation modules under `calculation/HWT-MGT` intentionally do not load models, tokenize text, read files, or preprocess inputs. The following settings summarize what the original repositories do before their metric formulas are applied.

| Source / metrics | Model and tokenizer | Input alignment and preprocessing | File/data handling |
|---|---|---|---|
| MGTBench: entropy, average log-probability | `AutoModelForCausalLM` and `AutoTokenizer`; default base model `gpt2-medium`; tokenizer padding ID is set to the EOS ID | Average log-probability truncates to 1024 tokens; entropy truncates to 512; causal-model logits are shifted against next-token labels | Dataset loader supplies train/test text and labels; metric results are written under `update_results/` |
| detecting-fake-text: top-10 entropy, GLTR ranks and ratios | `GPT2LMHeadModel` and `GPT2Tokenizer`; default model `gpt2`; model is put in evaluation mode | Prepends the GPT-2 BOS token; no explicit truncation in the GPT-2 backend; API returns top 20 predictions while the UI uses the top 10; observed-token ranks are zero-based | Flask/Connexion API accepts a JSON text request and returns token-level probabilities/ranks; the UI aggregates and visualizes them |
| DetectGPT: curvature and rank baselines | Configurable local causal model; default base model `gpt2-medium`; default mask model `t5-large` | Baseline scoring uses causal next-token alignment with no explicit truncation; perturbations use span length 2, mask 30% of words, one or more rounds, and T5-generated fills | Dataset loaders produce original/sampled text pairs; experiment outputs are JSON files under timestamped result directories |
| DetectLLM: LRR, NPR and baselines | Configurable `AutoModelForCausalLM`/`AutoTokenizer`; default base model `gpt2-medium`; tokenizer padding ID is set to EOS; default mask model `t5-small` | Base scoring uses shifted next-token labels; perturbations use span length 2, mask 30% of words, five perturbations by default, `mask_top_p=1.0`, and mask-generation `max_length=150` | Data is generated or loaded as original/sampled text pairs; results are saved as JSON under `results/` |
| DNA-GPT: n-gram and regeneration scores | Demo regeneration uses OpenAI `gpt-3.5-turbo-instruct`; notebook log-probability experiments use OpenAI completion log-probabilities | Demo truncates input to 350 words, uses a 50% character prefix, generates up to 300 tokens at temperature 0.7, and samples 30 continuations; text normalization lowercases, removes non-alphanumeric characters, and Porter-stems words longer than three characters | Demo receives text through Gradio; notebooks read JSONL result files containing original and regenerated completions |
| Fast-DNA-GPT variant | Local configurable causal model; default base model `gpt2` with its matching tokenizer | Uses a 50% prefix and 10 regenerated continuations by default; generated samples use a 30-token prompt in the data builder, `max_length=200`, and configurable temperature/top-k/top-p; padding tokens are masked from score averages | Reads prepared dataset files containing original/sampled text pairs and writes metric JSON results |
| Fast-DetectGPT: sampling discrepancy | Separate reference/sampling and scoring causal models; defaults are `falcon-7b` and `falcon-7b-instruct`; matching automatic tokenizers | Uses padded token batches, removes the first input token from labels and the final logit position, and supports separate vocabularies by clipping to the smaller vocabulary; empirical criterion samples 10,000 tokens per position | Reads prepared dataset files; writes separate JSON results for sampling and analytic criteria |
| GPT-Who: UID features | `GPT2LMHeadModel` and `GPT2Tokenizer`; fixed model `gpt2-xl`; tokenizer PAD is set to EOS; CUDA is expected | Prepends the GPT-2 EOS token, scores token surprisals from shifted logits, and does not set an explicit truncation limit | Reads CSV input with `text` and `label` columns; writes UID features to CSV, then the classifier script reads train/test CSV files |
| GPTID: PHD and MLE | Notebook uses `RobertaModel` and `RobertaTokenizer` with `roberta-base-cased`; multilingual mode uses an AutoModel/AutoTokenizer alternative | Replaces newlines/repeated spaces, truncates to 512 tokens, removes first/last special-token embeddings, and applies PHD with Euclidean distances, `alpha=1.0`, minimum subsample 40, seven intermediate points, and nine repeats per point | Notebook loads text from pandas data frames; PHD/MLE values are then passed to a downstream classifier |
| Hugging Face Perplexity reference | `GPT2LMHeadModel` and `GPT2TokenizerFast`; example model `openai-community/gpt2-large` | Encodes concatenated WikiText-2 text; uses the model context length with a strided sliding window, example stride 512, and masks overlapping context labels with `-100` | Loads WikiText-2 through the Hugging Face Datasets library |

These are provenance settings, not defaults for `e-phishGen`. The caller of each calculation module must choose and record the actual model, tokenizer, context length, truncation/window policy, alignment convention, and source file format used for the HWT/MGT experiment.

The corresponding source-specific preparation adapters are in [`calculation/HWT-MGT/preprocess/`](calculation/HWT-MGT/preprocess/README.md). They preserve the original loading, tokenization, file-reading, and input-preparation settings while leaving the metric formulas in `calculation/HWT-MGT`.
