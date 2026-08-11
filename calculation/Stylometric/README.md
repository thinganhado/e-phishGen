# Stylometric calculation scripts

These scripts implement the calculations documented in [`METRICS.md`](METRICS.md).
They operate on already-preprocessed representations. They do not read raw
corpora, tokenize text, lowercase text, sentence-split, POS-tag, build
vocabularies, run eSpeak/CoreNLP, train topic models, or load neural models.

| Script | Calculation input | Main outputs |
|---|---|---|
| `character_ngram_features.py` | Encoded character IDs and an optional fitted n-gram vocabulary | Character n-gram sequences/presence |
| `gender_prediction_features.py` | Selected text, POS tags, tokens, sentence tokens | GenderPrediction-JAVA syntactic, POS, character, lexical, and vocabulary values |
| `sentence_complexity_features.py` | Sentence lengths, relative-clause lengths, sentence flags | Mean/variance and relative-clause metrics |
| `rst_relation_proportions.py` | Parsed fine-grained RST relation labels | 32 normalized coarse-relation proportions |
| `entity_grid_transitions.py` | Coreference entity grid with `s/o/x/-` cells | 16 normalized adjacent-sentence transitions |
| `author_topic_features.py` | Author-topic and topic-word Gibbs counts | Author-topic `theta`, topic-word `phi`, topic-author rankings |
| `lda_topic_features.py` | LDA-C `gamma`, assignments, likelihood bound | Topic proportions, assignment proportions, entropy, dominant mass, active topics |
| `rhyme_features.py` | IPA component pairs, learned probabilities, final n-grams | IPA/ngram rhyme scores and detection decision |
| `character_embedding_features.py` | Integer character IDs and a supplied embedding matrix | Character embedding vectors |

## Recovery checklist

The following items are missing from the checked-out Stylometric folder or are
required to reproduce the original preprocessing pipelines. The calculation
modules above are not complete raw-text pipelines, so recovering the items
below is necessary before applying every metric directly to
`matched_pool_44.json`.

### Missing shared input preparation

- [ ] A raw JSON adapter that treats each object in `samples` as one document.
- [ ] Consistent English tokenization and sentence splitting.
- [ ] POS tagging and sentence-token structures for
      `gender_prediction_features.py` and sentence-complexity features.
- [ ] A documented normalization policy for `[URL]`, `[ORGANIZATION]`, email
      addresses, punctuation, case, and whitespace.
- [ ] A per-sample output schema that preserves `sample_id`, `group`, and
      `match_stratum` alongside every feature vector.

### Python 2 legacy environment

Required by `preprocess/continuous_n_gram_AA` and the discourse vectorizers:

- [ ] Python 2.7 runtime.
- [ ] `scikit_learn==0.18`.
- [ ] `keras==1.1.1`.
- [ ] A compatible Theano backend and its configuration.
- [ ] `nltk==3.0.4` and compatible NLTK data.
- [ ] A Pandas version compatible with Python 2.7 and the old APIs used by the
      discourse scripts.
- [ ] The original continuous-n-gram training vocabulary and character-ID
      mapping; these must be fitted on training data, not on the 44 evaluation
      samples.
- [ ] The original continuous-n-gram neural weights/checkpoint if inference
      rather than retraining is intended.

Python 2 is not installed locally. The discourse scripts also contain legacy
Python syntax and inconsistent indentation that must be preserved or repaired
before execution.

### Python 3 legacy environment

Required by `Authorship_Attribution_Short_Texts`, ancient Greek extraction,
and RhymeTagger:

- [ ] A Python version compatible with Keras 1.1.1, normally Python 3.6 or
      earlier.
- [ ] `keras==1.1.1` plus a compatible TensorFlow or Theano backend.
- [ ] `scikit-learn<0.20` for the removed `sklearn.cross_validation` import.
- [ ] A repair for `preprocess/Authorship_Attribution_Short_Texts/predict_def.py`
      (currently fails compilation with an indentation error near line 115).
- [ ] The original `dataset.csv` and its author/class labels for the short-text
      repository.
- [ ] Any original trained short-text classifier or embedding checkpoint.
- [ ] The missing ancient-Greek support modules referenced by the scripts:
      `download_corpus.py`, `corpus_categories.py`, and `greek_features.py`.
- [ ] The Tesserae corpus and its expected directory layout for `qcrit`.
- [ ] The original ancient-Greek feature configuration and language resources;
      this pipeline is not directly applicable to the English phishing data.

The following RhymeTagger resources have already been recovered locally:
`ujson`, NLTK data, eSpeak NG, and `preprocess/rhymetagger/models/en.json`.

### Java, Stanford NLP, and Weka

Required by GenderPrediction-JAVA, TopicModel4J, and discourse-grid builders:

- [ ] The original GenderPrediction-JAVA `libs/` directory, especially the
      exact Weka, Stanford POS tagger, and SLF4J versions used by the project.
- [ ] GenderPrediction-JAVA data files:
      `data/gendercombined.model`, `data/Gender_LadTree.model`,
      `data/Age_RandomForest.model`, `data/age.model`, ARFF files, truth data,
      and the original corpus directory.
- [ ] `TopicModel4J/com/topic/utils/FuncUtils.java`, imported by
      `AuthorTM.java` but absent from this checkout.
- [ ] TopicModel4J input corpus files, stopword file, vocabulary, and the
      original author-topic settings/checkpoints if exact reproduction is
      required.
- [ ] `authorship_attribution_discourse/entityGrid/NounPhrase.java`, imported
      by `BuildRSTGrid.java` but absent from this checkout.
- [ ] The complete RST parser source, parser models, fine-grained relation
      label CSVs, and parser configuration.
- [ ] Coreference/parser model resources and the exact Stanford CoreNLP
      runtime classpath used by the original discourse repository.
- [ ] Java wrapper scripts/classpaths that connect preprocessing outputs to the
      Python vector calculators.

Java 8, Stanford CoreNLP 3.6.0, CoreNLP models, Stanford POS tagger resources,
Commons Math, SLF4J, and Weka have been downloaded under the local
`external/` directory, but the project-specific source/data items above are
still missing.

### LDA-C and topic features

The checked-in `preprocess/lda_c` directory is incomplete. The following
original LDA-C sources are missing:

- [ ] `lda-estimate.c`
- [ ] `lda-model.c`
- [ ] `lda-inference.c`
- [ ] `utils.c`
- [ ] `cokus.c`
- [ ] `lda-alpha.c`
- [ ] The complete LDA-C Makefile in the build directory.
- [ ] A fitted LDA vocabulary and sparse document-word representation.
- [ ] Fitted `.beta`, `.gamma`, likelihood, and word-assignment outputs using
      one fixed topic count and vocabulary.

Without those artifacts, `lda_topic_features.py` cannot produce meaningful
document-topic features for the 44 samples.

### Learned stylometric artifacts

- [ ] Fitted character n-gram vocabulary and n-gram ID map.
- [ ] Character embedding matrix and its character-ID vocabulary.
- [ ] Author-topic Gibbs counts (`n_ak`, `n_kw`, assignments, author map) and
      fixed hyperparameters.
- [ ] RST relation vectors or the complete parser pipeline that creates them.
- [ ] Entity grids or the CoreNLP/coreference pipeline that creates them.
- [ ] Any original classifier calibration, thresholds, or checkpoints used to
      turn feature vectors into author/phishing predictions.

### Known source defects to recover or repair

- [ ] Fix the indentation error in `Authorship_Attribution_Short_Texts/predict_def.py`.
- [ ] Fix inconsistent tabs/spaces in the Python discourse vectorizers.
- [ ] Restore missing Java source files listed above.
- [ ] Restore missing LDA-C source files listed above.
- [ ] Replace hard-coded historical paths and input filenames with paths under
      this project.
- [ ] Add tests for empty documents, one-sentence documents, short texts, and
      documents with no detected RST/entity/rhyme relations.

Import functions directly, for example:

```python
from lda_topic_features import document_topic_proportions

theta = document_topic_proportions(gamma)
```

The scripts are deliberately calculation APIs rather than preprocessing
pipelines. Any HW-P/MG-P comparison, normalization across documents, class
threshold, and model calibration should be performed by a separate evaluation
script using identically prepared inputs.
