# Preprocessing

These scripts are copied from the `cross-model-phishing` pipeline:

- `01_unify_datasets.py`: unify the human phishing corpora
- `03_sample_corpus.py`: sample the corpus
- `04_merge_llm_corpus.py`: merge LLM-generated emails
- `05_extract_features.py`: run spaCy preprocessing and create the 17-feature table

The copied scripts import the original `config.py` and therefore retain the
upstream path assumptions. Copy `config.example.py` to `config.py` and set the
paths before running them; the upstream config contained an embedded Azure
credential and was not copied. `05_extract_features.py` requires spaCy and
`en_core_web_sm`.

The parent calculation modules are the separated, calculation-only interfaces;
this directory is the only part that performs file reading and NLP
preprocessing.
