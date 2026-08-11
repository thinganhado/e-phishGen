# Stylometric dependency environments

This directory records the dependencies of the original repositories used by
the Stylometric metric group. Original declarations copied from upstream are
under [`original/`](original/).

## Minimal environment proposal

The smallest practical split is **four environments/toolchains**:

| Environment | Covers | Why it is separate |
|---|---|---|
| `python2-legacy.txt` | `continuous-n-gram-AA` and the Python discourse vectorizers | The n-gram repository specifies Python 2.7, Keras 1.1.1, and old scikit-learn/NLTK; the discourse scripts use Python-2 print syntax and old pandas APIs. |
| `python3-legacy.txt` | `Authorship-Attribution-of-Short-Texts`, ancient Greek extraction, and RhymeTagger | These are Python 3 workflows. The ancient Greek repository specifies Python 3.6 and qcrit 0.0.21; the short-text repository uses legacy Keras/scikit-learn APIs; RhymeTagger additionally needs ujson, NLTK data, and eSpeak NG. Pin and test this combined environment before relying on exact reproduction. |
| `java-topic-discourse.txt` | `GenderPrediction-JAVA`, `TopicModel4J`, and Java discourse-grid preprocessing | These can share a Java 8 toolchain and Stanford 3.6-era libraries, but the original projects bundle or declare different JARs. Keep the project-local JARs on the classpath. |
| `c-lda-c.txt` | `lda-c` | The original is standalone C; it needs a C compiler, `make`, and the system math library, not a Python environment. |

The calculation-only scripts in the parent directory use Python standard
library code and do not require these legacy environments. The four-way split
is a minimum toolchain count, not a guarantee that every historical package
will install together. If the combined Python 3 environment cannot resolve
Keras 1.1.1 with qcrit/RhymeTagger, split it into two environments, making
five total.

## Original dependency audit

- `continuous-n-gram-AA`: copied `requirements.txt`; README also specifies
  Python 2.7 and a Theano backend.
- `Authorship-Attribution-of-Short-Texts`: README lists NumPy, Pandas, Keras,
  and scikit-learn; no pinned requirements file is provided.
- `GenderPrediction-JAVA`: Java, Weka, Stanford POS Tagger, and SLF4J JARs are
  bundled under `libs/`; no dependency manifest is provided.
- `ancient_greek_genre_classification`: copied `Pipfile` and `Pipfile.lock`;
  the declared runtime is Python 3.6 with sklearn, numpy, scipy, nltk, qcrit
  0.0.21, tqdm, and optional pylint.
- `authorship-attribution-discourse`: no requirements file; Python scripts
  import pandas and the Java grid builders require Stanford CoreNLP and its
  model resources.
- `lda-c`: copied `Makefile`; it builds with GCC and links `libm`.
- `TopicModel4J`: copied `pom.xml`; it declares Stanford CoreNLP 3.6.0,
  CoreNLP models 3.6.0, Commons Math 3.6, and test-only JUnit 3.8.1.
- `rhymetagger`: no requirements file; source imports `ujson` and `nltk`, and
  requires the external eSpeak NG executable plus a language model JSON.

Model files, Stanford tagger/CoreNLP resources, NLTK data, eSpeak NG, and
corpora are runtime assets rather than Python package requirements and are not
installed by these files.
