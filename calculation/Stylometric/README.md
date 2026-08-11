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

Import functions directly, for example:

```python
from lda_topic_features import document_topic_proportions

theta = document_topic_proportions(gamma)
```

The scripts are deliberately calculation APIs rather than preprocessing
pipelines. Any HW-P/MG-P comparison, normalization across documents, class
threshold, and model calibration should be performed by a separate evaluation
script using identically prepared inputs.
