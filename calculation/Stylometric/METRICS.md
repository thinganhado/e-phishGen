# Stylometric Metrics

This document records stylometric text features planned for `e-phishGen`.
The features can be used for authorship attribution, text classification, or
other comparative text-analysis tasks. New metrics will be added here as they
are reviewed.

## Reading the metrics for HW-P versus MG-P

The goal of this inventory is to identify how **HW-P** and **MG-P** differ.
Unless a section explicitly says otherwise, these metrics are descriptive
features, not universal detectors: “higher” means more of the measured
property, not automatically “HW-P” or “MG-P.” Read them by comparing the
feature distributions for labeled HW-P and MG-P samples under the same
preprocessing and model settings.

| Metric output type | How to read it for HW-P versus MG-P |
|---|---|
| Scalar feature or normalized proportion | Compare group means/medians and spread. A consistently higher HW-P value suggests the property is more characteristic of HW-P; a consistently higher MG-P value suggests the reverse. |
| Vector feature, such as topic, RST, entity-grid, or character features | Do not interpret one coordinate in isolation. Keep feature order and settings fixed, then compare the full vectors with a classifier or distance/effect-size analysis. |
| Probability or model score | Higher means greater confidence in the class or event named by that score. It is HW-P/MG-P evidence only after calibration on labeled samples. |
| Categorical or structured output, such as rhyme words or rhyme schemes | Convert to predeclared counts/proportions if a scalar comparison is needed; the raw label itself has no higher/lower direction. |

For every metric, record the original repository, formula, preprocessing,
settings, and whether the value is direct or derived. Thresholds shown in this
file are source thresholds for detecting an event (for example, a rhyme), not
HW-P/MG-P decision thresholds. A HW-P/MG-P threshold must be learned from a
training split and evaluated on held-out data; do not assume that `0.5`, a
source probability cutoff, or a larger value universally identifies either
class. For a new metric, the next useful record is the observed HW-P and MG-P
summary (mean, median, variance, and effect direction) under identical input
length and preprocessing controls.

## Character n-grams

| Metric | Original repository | Representation | Original setting |
|---|---|---|---|
| Continuous character n-grams | [`continuous-n-gram-AA`](https://github.com/yunitata/continuous-n-gram-AA) | Character IDs plus learned contiguous 2-, 3-, and 4-gram IDs | `char` mode uses `ngram_range_char = 4`; n-grams are learned from the training split and sequences are padded before the neural classifier |

### Calculation direction

This repository does not produce one standalone scalar “character n-gram
score.” It creates a sequence representation that is passed to a neural
authorship-attribution classifier. The directly comparable output is the
classifier probability or accuracy after training on the task's labels:

```text
character sequence
  -> character IDs
  -> learned 2-, 3-, and 4-gram IDs
  -> padded sequence
  -> embedding + neural classifier
  -> target-class probability
```

For a classification task, a higher probability for a target class means the
classifier considers the text more likely to belong to that class. A higher
raw n-gram ID or a higher number of active n-gram features has no intrinsic
class meaning. The original repository is an authorship-attribution study,
so its output should be calibrated for any new task.

### Original preprocessing

The source [`text_preprocess.py`](https://github.com/yunitata/continuous-n-gram-AA/blob/master/text_preprocess.py)
does the following before character encoding:

1. Separates common English contractions and selected punctuation with spaces.
2. Collapses repeated whitespace, strips surrounding whitespace, and lowercases.
3. Keeps a fixed alphabet of lowercase letters, digits, punctuation, newline,
   and space.
4. Replaces every character outside that alphabet with the character `a`.

The source [`util.py`](https://github.com/yunitata/continuous-n-gram-AA/blob/master/util.py)
then converts characters to IDs, learns all 2-, 3-, and 4-grams appearing in
the training sequences, appends recognized n-gram IDs, and pads each sequence
with Keras `pad_sequences`.

N-gram vocabulary construction must be fit on the training split only. The
validation and test splits are transformed using the training vocabulary.

### Original model and experiment settings

The source [`training_testing.py`](https://github.com/yunitata/continuous-n-gram-AA/blob/master/training_testing.py)
uses a Keras neural model with an embedding size, dropout, average pooling,
and a dense softmax classifier. The character-mode settings are:

| Dataset | Classes | Batch size | Epochs | Embedding size | Padded character length | Learning rate | Evaluation |
|---|---:|---:|---:|---:|---:|---:|---|
| CCAT10 | 10 | 5 | 150 | 100 | 9,000 | 0.001 | Held-out test split; 10% of training data for validation |
| CCAT50 | 50 | 5 | 150 | 100 | 9,000 | 0.001 | Held-out test split; 10% of training data for validation |
| Judgment | 3 | 5 | 150 | 100 | 30,000 | 0.001 | 10-fold stratified cross-validation; 10% train/validation split inside each fold |
| IMDb62 | 62 | 32 | 20 | 50 | 4,000 | 0.01 | 10-fold stratified cross-validation; 10% train/validation split inside each fold |

These settings describe the original authorship experiments. For another
classification task, record the label mapping, sequence length, split, random
seed, and classifier calibration. The source does not define a fixed
classification threshold.

### Input formats

- CCAT-style CSV: `article` text column and `class` author-label column.
- IMDb62: tab-separated lines containing author label followed by document
  text.
- Judgment: tab-separated rows; the source selects specific author groups
  and extracts the text from column 3.
- The source `data_prep.py` merges per-author document files into CCAT-style
  CSV files.

### Dependencies and provenance

The original [`requirements.txt`](https://github.com/yunitata/continuous-n-gram-AA/blob/master/requirements.txt)
declares `scikit_learn==0.18`, `keras==1.1.1`, `pandas`, and `nltk==3.0.4`.
The README additionally specifies Python 2.7 and Keras with a Theano backend.
These are historical dependencies; modern Keras/TensorFlow may require an
adapter rather than reproducing the original code unchanged.

## Relative character-frequency features

| Feature | Original repository | Formula | Source behavior |
|---|---|---|---|
| Digit ratio (`ratioOfDigits`) | [`GenderPrediction-JAVA`](https://github.com/shaina-ashraf/GenderPrediction-JAVA) | `100 * count(digits) / N` | Counts numeric characters and divides by the character count |
| Letter ratio (`ratioOfLetters`) | [`GenderPrediction-JAVA`](https://github.com/shaina-ashraf/GenderPrediction-JAVA) | `100 * count([A-Z] or [a-z]) / N` | Counts ASCII uppercase and lowercase letters |
| Uppercase-letter ratio (`ratioOfUpperCaseLetters`) | [`GenderPrediction-JAVA`](https://github.com/shaina-ashraf/GenderPrediction-JAVA) | `100 * count([A-Z]) / N` | Counts ASCII uppercase letters |
| Space ratio (`ratioOfWhiteSpacesToN`) | [`GenderPrediction-JAVA`](https://github.com/shaina-ashraf/GenderPrediction-JAVA) | `100 * count(' ') / N` | Counts literal ASCII space characters only |

Here `N` is the source's `characterCount(text)`: the number of characters
after removing carriage returns (`\r`) and newlines (`\n`). Other characters,
including tabs and punctuation, remain part of `N`. The source does not define
a standalone lowercase ratio. If needed, derive it as:

```text
lowercase_ratio = letter_ratio - uppercase_ratio
```

This derivation is valid for the source's ASCII letter definitions. It should
not be treated as a Unicode lowercase-character count.

### Source settings and output

The implementations are in
[`src/StylometricTechniques.java`](https://github.com/shaina-ashraf/GenderPrediction-JAVA/blob/main/src/StylometricTechniques.java),
and the feature ordering is registered in
[`src/CreateARFF.java`](https://github.com/shaina-ashraf/GenderPrediction-JAVA/blob/main/src/CreateARFF.java).
The four features occur in the ARFF vector as lexical attributes 29--32
(zero-based indices in the full feature array). Values are percentages in the
range 0--100 in ordinary inputs, and the ARFF writer rounds all feature values
to two decimal places.

The original project combines these features with punctuation, POS, lexical,
and vocabulary features, then trains Weka gender/age classifiers. These four
frequencies are therefore feature inputs rather than a standalone classifier
score. A higher value means a greater relative frequency of that character
category; it does not intrinsically indicate any class. The repository does
not define a per-feature threshold.

### Input handling and provenance

The repository's main pipeline reads its truth data from
[`data/truth.csv`](https://github.com/shaina-ashraf/GenderPrediction-JAVA/blob/main/data/truth.csv)
and generates ARFF files for Weka. It bundles Weka and Stanford POS-tagger JAR
files under `libs/`. The character-frequency methods themselves only require
the input text and do not require tokenization or POS tagging.

### Complete `GenderPrediction-JAVA` feature inventory

The complete source feature vector contains 55 values before the gender and
age class attributes. It is assembled by
[`src/MainClass.java`](https://github.com/shaina-ashraf/GenderPrediction-JAVA/blob/main/src/MainClass.java),
written to ARFF by
[`src/CreateARFF.java`](https://github.com/shaina-ashraf/GenderPrediction-JAVA/blob/main/src/CreateARFF.java),
and combines the following groups.

#### Syntactic character counts

Implemented in
[`src/SyntacticFeatures.java`](https://github.com/shaina-ashraf/GenderPrediction-JAVA/blob/main/src/SyntacticFeatures.java).
Each feature is a raw count in the input text.

| Feature | Counted characters |
|---|---|
| Apostrophe | ASCII apostrophe and the source's curly-apostrophe representation |
| Brackets | `[ ]`, `( )`, `{ }`, `< >` |
| Colon | `:` |
| Comma | `,` plus two additional comma-like Unicode characters in the source |
| Dash | The source's dash character |
| Ellipsis | The source's ellipsis character; additionally increments once if the text contains `...` |
| Exclamation | `!` |
| Full stop | `.` |
| Question mark | `?` |
| Semicolon | `;` |
| Slash | `/` and `\\` |

#### Part-of-speech features

Implemented in
[`src/POSTagger.java`](https://github.com/shaina-ashraf/GenderPrediction-JAVA/blob/main/src/POSTagger.java)
using Stanford's `english-left3words-distsim.tagger`. The first 13 values are
raw tag counts:

| Feature | Stanford POS tags counted |
|---|---|
| Nouns | `NN`, `NNS`, `NNP`, `NNPS` |
| Adjectives | `JJ`, `JJR` (the source repeats `JJR` instead of listing `JJS`) |
| Adverbs | `RB`, `RBS`, `RBR` |
| Verbs | `VB`, `VBD`, `VBG`, `VBN`, `VBP`, `VBZ` |
| Cardinal numbers | `CD` |
| Prepositions | `IN`, `TO` |
| Particles | `RP` |
| Symbols | `SYM` |
| Conjunctions | `CC` |
| Determiners | `DT` |
| Interrogatives | `WDT`, `WP`, `WRB` |
| Foreign words | `FW` |
| Possessive pronouns | `PRP$` |

The remaining three POS features are density percentages:

| Feature | Formula |
|---|---|
| POS unigram density | `100 * number_of_unique_POS_tags / number_of_POS_tags` |
| POS bigram density | `100 * number_of_unique_adjacent_POS_bigrams / number_of_POS_bigrams` |
| POS trigram density | `100 * number_of_unique_adjacent_POS_trigrams / number_of_POS_trigrams` |

The bigram and trigram implementations use whitespace-tokenized POS-tag
strings and do not bridge line boundaries. Empty or too-short tag sequences can
make these ratios undefined.

#### Character and lexical features

The following 16 character-level and surface features are implemented in
[`src/StylometricTechniques.java`](https://github.com/shaina-ashraf/GenderPrediction-JAVA/blob/main/src/StylometricTechniques.java):

| Feature | Source formula/definition |
|---|---|
| Character count | Number of characters after removing `\\r` and `\\n` |
| Character count without spaces | Character count after also removing literal spaces |
| Digit ratio | `100 * digit_count / character_count` |
| Letter ratio | `100 * ASCII_letter_count / character_count` |
| Uppercase-letter ratio | `100 * ASCII_uppercase_count / character_count` |
| Whitespace ratio | `100 * literal_ASCII_space_count / character_count` |
| Tab ratio | `100 * tab_count / character_count` |
| Special-character ratio | `100 * count(chars matching the source special-character regex) / character_count` |
| Uppercase character count | Count of `[A-Z]` |
| Digit count | Count of characters accepted by Java `Double.parseDouble` when converted individually; ordinarily `0`--`9` |
| Space count | Count of literal ASCII spaces |
| Tab count | Number of tab-delimited segments minus one |
| Question-sentence percentage | `100 * tokens containing '?' / detected sentence count` |
| Punctuation percentage | `100 * count(['\\\";:!.,]) / character_count` |
| Semicolon percentage | `100 * semicolon_count / character_count` |
| Comma percentage | `100 * comma_count / character_count` |

The source's `characterCount` denominator removes carriage returns and
newlines, but the numerator functions otherwise inspect the original text.
The source special-character regex contains some encoding-dependent and
unexpected literal characters; preserve that regex if exact reproduction is
required.

#### Vocabulary-richness and length features

The remaining 12 values are also implemented in
`src/StylometricTechniques.java`. Words are obtained with Java `Scanner`, so
whitespace separates tokens and punctuation remains attached to a token.

| Feature | Source formula/definition |
|---|---|
| Average word length | `character_count / total_word_count` (the source includes the full character count, not only letters in words) |
| Yule K measure | `10000 * (S2 - N) / N²`, where `S2 = sum(m² * V_m)`, `m` is a word frequency and `V_m` is the number of types with frequency `m` |
| Hapax legomena | Number of word types occurring exactly once (`V1`) |
| Total words | Number of tokens returned by Java `Scanner` |
| Average sentence length in characters | `character_count / detected_sentence_count` |
| Ratio of short words | `100 * count(words with length <= 3) / total_words`; the source method is named `ratioOfWordsWithLength3` |
| Average sentence length in words | `total_words / detected_sentence_count` |
| Total unique words | Number of distinct `Scanner` tokens |
| Simpson D measure | `sum(V_m * (m/N) * ((m-1)/(N-1)))` |
| Sichel S measure | `V2 / V`, where `V2` is the number of types occurring twice and `V` is vocabulary size |
| Brunet W measure | `N^(V^(-0.1654))` |
| Honoré R measure | `100 * log(N) / (1 - V1/V)` |

Sentence detection is source-specific: a sentence is counted when a
whitespace-delimited token contains `.`, `?`, or `!`. The source does not
define smoothing or explicit handling for empty texts, zero sentences, or
single-token vocabularies, so those cases may produce undefined values.

#### Feature order and interpretation

The ARFF order is: syntactic counts `0--10`, POS counts and densities
`11--26`, then the 28 character/lexical/vocabulary values `27--54`. The
gender class is attribute 55 and age is attribute 56. The ARFF writer rounds
the 55 feature values to two decimal places before writing them.

These are feature values, not independent gender or age scores. Higher values
mean more of the corresponding measured property; they do not universally
indicate a particular class. The original repository trains Weka classifiers
on the combined vector and defines no per-feature thresholds.

## Sentence complexity and length

The ancient Greek repository extracts these features through
[`qcrit`](https://pypi.org/project/qcrit/) from the
[Tesserae corpus](https://github.com/QuantitativeCriticismLab/ancient_greek_genre_classification).
They are intended for genre classification and are not limited to authorship or
gender tasks.

| Metric | Formula/definition | Original settings | Overlap decision |
|---|---|---|---|
| Mean sentence length (`mean_sentence_length`) | `mean(len(sentence))`, where length is the number of characters in each tokenized sentence | NLTK Greek Punkt sentence tokenizer; terminal punctuation `.`, `;`, and Greek question mark `;`; sentence strings are measured in characters | Added as a variant: GenderPrediction-JAVA has a similar average-character-length concept, but uses Java sentence detection based on tokens containing `.`, `?`, or `!` |
| Variance of sentence length (`variance_of_sentence_length`) | Population variance `mean((len(sentence) - mean_length)^2)` | Same Greek Punkt tokenization and character-length definition as mean sentence length | New metric; no matching variance feature in the current stylometric document |
| Mean relative-clause length (`mean_length_relative_clause`) | Mean number of characters between each relative pronoun and the next punctuation mark | Relative clauses are identified from inflected Greek relative pronouns; punctuation terminates the measured span | New metric; no matching clause-length feature |
| Fraction of sentences with a relative clause (`freq_sentence_with_relative_clause`) | `count(sentences containing >=1 relative pronoun) / number_of_sentences` | Sentence-normalized; relative-pronoun detection uses the repository's ancient Greek feature rules | New metric; no matching sentence-relative-clause fraction |

The source treats most lexical marker features as per-character frequencies, but
features described as “sentences with...” are normalized by sentence count.
Mean and variance of sentence length are measured directly from tokenized
sentence character counts. The source paper describes the same 23-feature
ancient Greek set, including relative-clause length, mean sentence length, and
sentence-length variance. [The paper](https://aclanthology.org/W19-25.pdf)

### Preprocessing and interpretation

The repository calls
[`run_feature_extraction.py`](https://github.com/QuantitativeCriticismLab/ancient_greek_genre_classification/blob/master/run_feature_extraction.py)
with:

- Python 3.6.5 and NLTK 3.3 in the original experiment
- Tesserae `.tess` parsing
- NLTK's Greek Punkt sentence tokenizer
- `setup_tokenizers(terminal_punctuation=('.', ';', ';'))`
- exclusion of composite corpus files

Higher mean sentence length indicates longer sentences. Higher sentence-length
variance indicates more uneven sentence sizes. Higher mean relative-clause
length indicates longer relative-clause spans, and a higher relative-clause
fraction indicates that relative clauses occur in more sentences. None of these
features has a standalone classification threshold; the original project uses
them as inputs to genre classifiers.

## Discourse, grammatical-relation, and coreference features

Source: [`authorship-attribution-discourse`](https://github.com/elisaF/authorship-attribution-discourse).
These features were added because the existing stylometric inventory has no
RST-relation representation and no coreference-linked grammatical entity grid.
They are therefore not exact overlaps with the current metrics: the formulas,
linguistic definitions, and preprocessing settings are different.

### RST discourse-relation proportions

The source flattens the RST relation cells, maps fine relations to the
following 32 coarse nucleus/satellite categories, and normalizes each count by
the total number of extracted relations:

```text
rst_relation_proportion(r) = count(coarse RST relation r) / total RST relations
```

| Metric family | Categories | Original settings | Interpretation / threshold |
|---|---|---|---|
| Coarse RST relation proportions | `Attribution.N/S`, `Background.N/S`, `Cause.N/S`, `Comparison.N/S`, `Condition.N/S`, `Contrast.N/S`, `Elaboration.N/S`, `Enablement.N/S`, `Evaluation.N/S`, `Explanation.N/S`, `Joint.N`, `Manner-Means.N/S`, `Topic-Comment.N/S`, `Summary.N/S`, `Temporal.N/S`, `Same-unit.N`, `Textual-organization.N`, and `None` | [`create_RST_discourse_vectors.py`](https://github.com/elisaF/authorship-attribution-discourse/blob/master/create_RST_discourse_vectors.py); fine relation sets are read from CSV, mapped with the repository's hard-coded coarse mapper, and normalized per document; empty inputs become all zero | Higher value means that relation category makes up a larger share of the document's RST relations. No fixed threshold; the original work uses the vector as input to authorship classifiers. |

The source maps related fine labels together, for example `cause/result`,
`elaboration/example/definition`, and `temporal/sequence`, while retaining
the `.N` versus `.S` distinction. `None` represents an empty RST relation
cell and is included in the denominator.

### Coreference-aware grammatical entity-grid transitions

The Java preprocessing builds one entity column per Stanford CoreNLP
coreference chain and one row per sentence. Each cell is reduced to a
grammatical role:

| Cell symbol | Definition in the original repository |
|---|---|
| `s` | `nsubj` (nominal subject) |
| `o` | `dobj`, `iobj`, or `nsubjpass`; passive subjects are treated as objects |
| `x` | Any other dependency relation attached to the noun-phrase head |
| `-` | The coreference-chain entity is not mentioned in that sentence |

For every entity column and every pair of adjacent sentences, the source
counts one of the 16 transitions `ss`, `so`, `sx`, `s-`, `os`, `oo`, `ox`,
`o-`, `xs`, `xo`, `xx`, `x-`, `-s`, `-o`, `-x`, `--`, then normalizes them:

```text
entity_grid_transition(a,b) = count(a followed by b) / total adjacent-sentence transitions
```

| Metric family | Original settings | Interpretation / threshold |
|---|---|---|
| Coreference-aware grammatical relation transition proportions | [`BuildEntityGrid.java`](https://github.com/elisaF/authorship-attribution-discourse/blob/master/entityGrid/src/entityGrid/BuildEntityGrid.java) constructs the grid; [`create_discourse_vectors.py`](https://github.com/elisaF/authorship-attribution-discourse/blob/master/create_discourse_vectors.py) calculates the 16 normalized values. Stanford CoreNLP annotators: `tokenize, ssplit, pos, lemma, ner, parse, mention, coref`; `coref.algorithm=neural`; noun-phrase heads are matched to dependency relations; entities with fewer than two mentions are removed. | Higher value means that the corresponding grammatical-role transition is more frequent among tracked entities across adjacent sentences. No fixed threshold; use the complete vector with the downstream classifier. |

This is one combined metric family rather than separate grammatical and
coreference scores: grammatical roles define the cell values, while
coreference chains define which mentions share an entity column. The RST
variant [`BuildRSTGrid.java`](https://github.com/elisaF/authorship-attribution-discourse/blob/master/rstParser/src/rstParser/BuildRSTGrid.java)
uses the same neural-coreference and two-mention filtering settings but
retains mention spans per entity; it is the input format for the RST relation
vectorizer above, not an additional standalone scalar.

### Reproduction caveats

The repository's vectorizers use Python 2-era pandas APIs (`DataFrame.ix` in
the transition script) and expect already-generated grid CSV/TSV files. RST
parsing and CoreNLP annotation are preprocessing steps, not part of the
numeric formulas. The original repository defines no per-feature threshold;
any HWT/MGT decision threshold must be calibrated on the target dataset.

## Author-topic model features

Source: [`TopicModel4J`](https://github.com/soberqian/TopicModel4J), specifically
[`AuthorTM.java`](https://github.com/soberqian/TopicModel4J/blob/master/src/main/java/com/topic/model/AuthorTM.java).
The existing LDA section models a document as a topic mixture. AuthorTM instead
models each observed author as a topic mixture and allows each document to have
multiple authors. It is therefore not an exact overlap: the formula family is
similar, but the distribution being estimated, latent assignments, and
collapsed-Gibbs settings differ.

### Author-topic distributions

After collapsed Gibbs sampling, AuthorTM estimates the author-topic vector:

```text
author_topic[a,k] = (n_ak + alpha) / (n_a + K * alpha)
```

where `n_ak` is the number of tokens assigned to topic `k` for author `a`,
`n_a` is the total assigned tokens for that author, and `K` is the topic count.
The vector sums to 1 for each author.

| Feature | Formula / definition | Original settings | Interpretation / threshold |
|---|---|---|---|
| Author-topic proportions (`theta[a,k]`) | `(n_ak + alpha) / (n_a + K * alpha)` from author and topic assignments | [`estimateTheta`](https://github.com/soberqian/TopicModel4J/blob/master/src/main/java/com/topic/model/AuthorTM.java); collapsed Gibbs sampling; documents may list multiple authors; `alpha` is a symmetric author-topic prior | Higher value means topic `k` is more associated with author `a`. Topic IDs are model-specific. No HWT/MGT threshold |
| Topic-word probabilities (`phi[k,w]`) | `(n_kw + beta) / (n_k + V * beta)` where `n_kw` is the topic-word count and `n_k` is the topic token total | [`estimatePhi`](https://github.com/soberqian/TopicModel4J/blob/master/src/main/java/com/topic/model/AuthorTM.java); `beta` is a symmetric topic-word prior; output is written with the top `inTopWords` words per topic | Higher value means word `w` is more probable under topic `k`; it is a topic interpretation/style feature, not an HWT/MGT score |
| Ranked topic-author association | For each topic, rank authors by `theta[a,k]` and retain the top `inTopWords` authors | [`writeTopicAuthor`](https://github.com/soberqian/TopicModel4J/blob/master/src/main/java/com/topic/model/AuthorTM.java); this is a ranked view of `theta`, not a new probability formula | Higher rank/association means stronger topic-author affinity. No fixed threshold |

The author-topic vector is distinct from the existing LDA document-topic
vector: it requires author metadata during model fitting and produces one
distribution per author, not per document. Consequently, applying it to
HWT/MGT text requires a defined author set or author labels; it is not a
drop-in unsupervised feature for anonymous generated text.

### AuthorTM settings and input format

The source reads each line as a tab-separated record:

```text
author1<separator>author2<tab>lowercased document text
```

The author field is split using the constructor's `separator` argument (the
example uses a comma), and the text is tokenized and lowercased by
`FileUtil.tokenizeAndLowerCase`. The main example uses:

| Setting | Example value |
|---|---:|
| Topics `K` | 30 in [`ATMTest.java`](https://github.com/soberqian/TopicModel4J/blob/master/src/main/java/example/ATMTest.java) |
| Author-topic prior `alpha` | 0.1 |
| Topic-word prior `beta` | 0.01 |
| Gibbs iterations | 800 |
| Top words/authors written | 20 |
| Sampling | Random initialization followed by collapsed Gibbs sampling |

The class's built-in `main` uses a different example configuration (`K=25`,
`alpha=0.1`, `beta=0.01`, 500 iterations, and 50 top items), so the actual
constructor arguments must be recorded. The implementation uses
`Math.random()` for initialization and does not expose a random seed; exact
reproduction therefore requires controlling or recording the runtime setup.
No feature-level classification threshold is defined by the repository.

## LDA topic distributions

Source: [`lda-c`](https://github.com/blei-lab/lda-c). The current stylometric
inventory contains lexical counts, character features, embeddings, and
linguistic structures, but no latent topic representation. LDA topic
distributions are therefore new under the formula, definition, and settings
comparison.

### Document-topic distribution

For each document, LDA-C estimates a variational posterior Dirichlet parameter
vector `gamma` with `K` entries. The topic-proportion feature used for
comparison is the normalized vector:

```text
topic_proportion[k] = gamma[k] / sum(j=1..K, gamma[j])
```

The raw `.gamma` output stores the unnormalized variational Dirichlet
parameters. Normalize it before using it as a document-level topic
distribution; the resulting `K` values sum to 1.

| Metric family | Formula / definition | Original settings | Interpretation / threshold |
|---|---|---|---|
| Document-topic proportions (`theta_1 ... theta_K`) | Normalized variational posterior parameters `gamma_k / sum_j gamma_j`, estimated from sparse document word counts and learned topic-word probabilities `beta` | [`lda-inference.c`](https://github.com/blei-lab/lda-c/blob/master/lda-inference.c); variational inference; symmetric Dirichlet prior `theta ~ Dirichlet(alpha,...,alpha)`; input is a sparse bag-of-words vector | Higher value means the document is more associated with that latent topic. Topic indices have no universal semantic meaning and must be tied to the fitted model. No fixed HWT/MGT threshold; use the full vector or calibrate a downstream classifier |

### Original LDA-C settings

| Setting | Repository default |
|---|---:|
| Topic count `K` | Supplied on the command line; no universal default (`lda est [initial alpha] [k] ...`) |
| Initial alpha | Supplied on the command line; symmetric across topics |
| Variational maximum iterations | 20 in [`settings.txt`](https://github.com/blei-lab/lda-c/blob/master/settings.txt); `-1` in [`inf-settings.txt`](https://github.com/blei-lab/lda-c/blob/master/inf-settings.txt) for inference until convergence |
| Variational convergence | `1e-6` |
| EM maximum iterations | 100 |
| EM convergence | `1e-4` |
| Alpha handling | `estimate` |
| Input representation | One line per document: sparse term-count vector `[M] term_id:count ...` |
| Output | `.gamma` document-topic parameters; `.beta` log topic-word probabilities; likelihood bound separately |

The model must be fit on the training corpus and reused for held-out HWT/MGT
documents. Because topic labels can be permuted between independently fitted
models, compare documents only within the same fitted model and vocabulary.
This is a feature vector, not a standalone score: higher values do not
intrinsically mean HWT or MGT.

### Additional LDA-C topic-model features for stylometry

The following features are available directly or are deterministic summaries
of LDA-C's saved `gamma`, likelihood, and word-assignment outputs. They do not
overlap with the existing lexical, character, sentence, discourse, or rhyme
features.

| Feature | Formula / definition | Source output and settings | Interpretation / threshold |
|---|---|---|---|
| Document variational log-likelihood bound | `L_d = compute_likelihood(document_d, model, phi, gamma)`; the implementation includes the Dirichlet, topic-word, assignment, and entropy terms | [`compute_likelihood`](https://github.com/blei-lab/lda-c/blob/master/lda-inference.c); inference writes one likelihood value per document | Higher generally indicates better model fit, but it is strongly affected by document length; normalize by token count for cross-document comparison. No fixed threshold |
| Topic-assignment proportions | `assignment_proportion[k] = count(words assigned to topic k) / total token count`, where each word receives `argmax_k(phi[word,k])` | [`write_word_assignment`](https://github.com/blei-lab/lda-c/blob/master/lda-estimate.c) writes the highest-`phi` topic for each word; assignments are produced with the same fitted `K`, vocabulary, and inference settings | Higher value means more observed tokens were assigned to that topic. This is a hard-assignment feature and differs from the soft `gamma`-normalized topic proportions; no threshold |
| Topic entropy | `H(theta) = -sum_k(theta_k * log(theta_k))`, with `theta_k = gamma_k / sum_j gamma_j` | Derived from LDA-C's `final.gamma`; topic count `K` and inference settings must be fixed | Higher value means the document's topic mixture is more diffuse; lower means more concentrated. No original repository threshold |
| Dominant-topic mass | `max_k(theta_k)` | Derived from normalized `final.gamma` | Higher value means one topic accounts for a larger posterior share. No original repository threshold |
| Number of active topics | `count(k: theta_k >= epsilon)` | Derived from normalized `final.gamma`; `epsilon` must be recorded because LDA-C does not define one | Higher value means the document uses more topics under the selected cutoff. No original repository threshold |

The first two rows are tied to LDA-C's native inference outputs. The last
three are recommended deterministic summaries for stylometry, not separately
named metrics in the original C program; record `K`, `epsilon`, the fitted
model, vocabulary, and normalization whenever they are used.

## Rhyme detection and versification features

Source: [`rhymetagger`](https://github.com/versotym/rhymetagger). No current
stylometric metric uses phonetic rhyme, line-final sound structure, syllable
peaks, stress, or rhyme schemes, so the features below do not overlap with the
existing inventory under the required formula, definition, and settings test.

`RhymeTagger` is primarily a structured annotator rather than a single-score
metric. Its outputs can be retained per line or aggregated later for a
stylometric classifier.

| Feature | Formula / definition | Original settings | Interpretation / threshold |
|---|---|---|---|
| Line-final rhyme word | Lowercased final word after tokenization and punctuation removal; possessive endings such as `John's` are merged with the preceding token | [`_get_rhyme_word`](https://github.com/versotym/rhymetagger/blob/master/tagger.py); NLTK word tokenization; line-final punctuation is excluded | Categorical support feature; no higher/lower direction and no threshold |
| IPA rhyme components | The reversed sequence of syllable peaks and intervening consonant clusters from the line's IPA transcription, retaining only the final stressed portion | eSpeak NG transcription unless IPA is supplied; `stress=True`, `vowel_length=True`, `syll_max=2` in the model constructor | Encodes the phonetic material used for rhyme comparison; not a scalar score |
| Reduplicant/syllable length | Number of detected syllable-peak components in the rhyme portion before truncation | Syllable peaks are detected from the eSpeak IPA regex; maximum relevant syllables is `syll_max=2` | Higher value means more syllabic material is considered in the rhyme; no standalone threshold |
| Final character n-gram | `last_ngram(word, n) = word[-n:]` (or the complete word when shorter) | `ngram_length=3`; used after IPA scoring from iteration `ngram=3` in the English pretrained model | Categorical orthographic support feature; no higher/lower direction |
| IPA rhyme score | If component-pair probabilities exist, `P = product(p_i)` and `Q = product(1-p_i)`; otherwise identical components use `0.99`, different unknown components use `0.0001`; score is `length_coef * P/(P+Q)` | Pair probabilities learned from collocations; `length_coef = 1 - length_penalty` only when reduplicant lengths have different parity; default `length_penalty=0`; rhyme accepted when score `> prob_ipa_min` | Higher score indicates stronger phonetic rhyme evidence. Default acceptance threshold is `0.95` in `new_model`; pretrained models can override it |
| Character n-gram rhyme score | Lookup of the learned final-n-gram pair probability; identical unknown n-grams receive `0.99`, other unknown pairs `0.0001`, multiplied by the same length coefficient | `ngram_length=3`; used when enabled and IPA did not establish a rhyme; accepted when score `> prob_ngram_min`, default `0.95` | Higher score indicates stronger learned orthographic rhyme evidence; threshold is model-dependent, normally `0.95` |
| Rhyme relation / rhyme chains | Lines are connected when they pass the rhyme score test; output can be per-line rhyme partners, rhyme chains, or an ABBA-style integer scheme | `window=5`; same-word rhymes and cross-stanza rhymes are controlled by model settings; English model: `same_words=false`, `stanza_limit=true` | A detected relation means the pair is classified as rhyming. The source does not define a HWT/MGT threshold; its pair thresholds are the detection thresholds |

### Original model settings

For the checked-in English model [`models/en.json`](https://github.com/versotym/rhymetagger/blob/master/models/en.json), the relevant settings are:

| Setting | English pretrained value |
|---|---:|
| Language / transcription | `en` with eSpeak NG; `transcribed=False` by default |
| Forward comparison window | 5 lines |
| Maximum rhyme syllables | 2 |
| Stress and vowel length | Enabled |
| N-gram fallback iteration | 3 |
| Final n-gram length | 3 characters |
| Same-word rhymes | Disabled |
| Stanza restriction | Enabled |
| IPA / n-gram acceptance probability | 0.95 / 0.95 |
| Length penalty | 0 |
| Refrain (`radif`) filtering | 2; disabled because filtering is only activated for values `<=1` |

The other language models contain language-specific learned probabilities and
settings, so the model file and language must be recorded for reproducibility.
The repository requires eSpeak NG for untranscribed text. These features are
not sentence-length features: they operate on poetic lines and their final
words/sounds, so they do not overlap with the existing sentence complexity
metrics.

## Character embeddings

| Feature/model | Original repository | Representation | Intended setting |
|---|---|---|---|
| Learned character embedding sequence | [`Authorship-Attribution-of-Short-Texts`](https://github.com/ironfist2/Authorship-Attribution-of-Short-Texts) | Lowercased character IDs are mapped through a trainable embedding layer before convolution | Use `model2` and `encode_data2` instead of the repository's default one-hot `model` and `encode_data` |

### Representation and preprocessing

The source [`predict_def.py`](https://github.com/ironfist2/Authorship-Attribution-of-Short-Texts/blob/master/predict_def.py)
defines a vocabulary from lowercase ASCII letters, digits, punctuation,
newline, and space. The intended embedding path is:

```text
text -> lowercase -> remove spaces -> character sequence
     -> integer IDs -> trainable embedding vectors
     -> 1D convolutions -> dense classifier
```

The intended embedding dimension is 300. The configured maximum sequence
length is 140 characters; longer sequences are truncated and shorter ones are
zero-padded. The default one-hot path instead creates an input tensor of shape
`(batch, 140, vocabulary_size)` and is not the embedding representation.

### Intended model settings

From [`main.py`](https://github.com/ironfist2/Authorship-Attribution-of-Short-Texts/blob/master/main.py)
and `model2` in `predict_def.py`:

| Setting | Value |
|---|---:|
| Maximum character length | 140 |
| Embedding dimension | 300 |
| Convolution filter widths | 3, 4, 5 |
| Filters per convolution | 500 |
| Dense layer width | 256 |
| Dropout | 0.5 |
| Output classes | 22 authors |
| Batch size | 32 |
| Epochs | 20 |
| Optimizer | SGD, learning rate 0.001, momentum 0.9 |
| Random seed | NumPy seed 0 |
| Split | `train_test_split(random_state=1)`, with no explicit stratification |

The input file is `dataset.csv`; the source drops missing rows, removes rows
whose `time_stamp` equals `created_at`, uses `raw_text` as the input, and
encodes `username` as the class label.

### Source caveats

The repository does not run the embedding mode by default. Its default
`main.py` path uses one-hot `model` plus `encode_data`. To activate the
embedding path, the README instructs the user to switch to `model2` and
`encode_data2`.

The embedding path also requires source fixes before it can reproduce the
intended representation:

- `Embedding` is referenced in `model2` but is not imported in `predict_def.py`.
- `create_vocab_set` builds single-character vocabulary entries, while
  `encode_data2` removes spaces and constructs adjacent two-character strings.
  Those bigrams therefore do not match the vocabulary and are left as zeros.

These issues mean that a repaired implementation must record its vocabulary
unit (characters or character bigrams) and cannot be described as an exact
run of the checked-in code without that qualification.

Character embeddings are learned internal features, not a standalone scalar
score. A higher classifier probability means greater confidence in the
corresponding author/class; the source defines no per-feature threshold.

The README lists NumPy, Pandas, Keras, and scikit-learn as dependencies. The
repository does not provide a pinned requirements file.
