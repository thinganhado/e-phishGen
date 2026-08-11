# Stylometric preprocessing scripts

This directory contains source-adapted preprocessing entry points copied from
the original repositories documented in `../METRICS.md`. The calculation
scripts in the parent directory consume their outputs.

These files are intentionally kept close to the original implementations so
their settings remain auditable. They are not guaranteed to run in the base
repository until the original dependencies, external models, and language
runtimes are installed.

| Directory | Adopted source | Purpose | External requirement |
|---|---|---|---|
| `continuous_n_gram_AA` | [`continuous-n-gram-AA`](https://github.com/yunitata/continuous-n-gram-AA) | Character cleaning, alphabet mapping, character IDs, and n-gram input construction | Historical Python 2/Keras stack; use the training vocabulary for validation/test data |
| `GenderPrediction_JAVA` | [`GenderPrediction-JAVA`](https://github.com/shaina-ashraf/GenderPrediction-JAVA) | Java text handling, Stanford POS tagging, and source-compatible feature preparation | Java, Stanford POS tagger JAR/model, and the original classpath |
| `Authorship_Attribution_Short_Texts` | [`Authorship-Attribution-of-Short-Texts`](https://github.com/ironfist2/Authorship-Attribution-of-Short-Texts) | Character vocabulary and integer encoding, including the source's embedding path | Keras/TensorFlow model code; the checked-in embedding path has the caveats recorded in `../METRICS.md` |
| `ancient_greek_genre_classification` | [`ancient_greek_genre_classification`](https://github.com/QuantitativeCriticismLab/ancient_greek_genre_classification) | Tesserae parsing and qcrit feature-extraction entry points | Python 3.6-era qcrit/NLTK and the Tesserae corpus |
| `authorship_attribution_discourse` | [`authorship-attribution-discourse`](https://github.com/elisaF/authorship-attribution-discourse) | Stanford CoreNLP entity/RST grids and grid-to-vector preparation | Java, Stanford CoreNLP models, and the RST parser data/tooling |
| `lda_c` | [`lda-c`](https://github.com/blei-lab/lda-c) | Original sparse document-word input reader and format reference | C compiler; vocabulary and sparse bag-of-words generation must match the fitted model |
| `TopicModel4J` | [`TopicModel4J`](https://github.com/soberqian/TopicModel4J) | Original tokenization/file preparation and AuthorTM input handling | Java/Maven and the repository's encoding/tokenization assumptions |
| `rhymetagger` | [`rhymetagger`](https://github.com/versotym/rhymetagger) | Line-final word extraction and IPA/rhyme preprocessing integrated with the tagger | Python package dependencies, eSpeak NG, and a language model JSON |

## Important usage rules

- Do not fit vocabularies, topic models, or learned n-gram maps on the test
  split. Fit them on the training split and reuse them.
- The pretrained model files themselves are not copied into this directory.
  Supply them through the original repository's documented model paths.
- The copied scripts may use old Python 2, Java, Keras, pandas, or CoreNLP
  APIs. Keep their original environment separate from the calculation-only
  scripts if exact reproduction is required.
- Preprocessing is not a HW-P/MG-P metric. It produces the representation;
  the parent scripts calculate the documented values, and a separate analysis
  step compares the resulting HW-P and MG-P distributions.

## Provenance

The copied files are retained with their original source comments and names.
The source repository links above are the provenance references; local copies
should be updated deliberately when an upstream implementation changes.
