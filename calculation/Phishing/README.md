# Phishing stylometric calculations

This directory contains the 17 hand-engineered phishing-email features from
the local source repository `C:\Users\donga\Downloads\cross-model-phishing`, split into one calculation file
per metric. The functions accept prepared values; they do not read corpora,
tokenize text, run spaCy, or load `en_core_web_sm`.

| Group | Scripts |
|---|---|
| Lexical | `ttr.py`, `mean_word_length.py`, `mean_sentence_length.py`, `yules_k.py` |
| Syntactic | `clause_density.py`, `noun_ratio.py`, `verb_ratio.py`, `mean_parse_depth.py` |
| Stylistic | `imperative_count.py`, `first_person_ratio.py`, `second_person_ratio.py`, `politeness_density.py`, `urgency_density.py` |
| Phishing-specific | `url_density.py`, `cta_density.py`, `authority_density.py`, `time_pressure_density.py` |

The source-compatible preprocessing pipeline is under [`preprocess/`](preprocess/README.md).
Dependency declarations and environment guidance are under
[`requirements/`](requirements/README.md).

Example:

```python
from ttr import ttr
from yules_k import yules_k

words = ["verify", "your", "account", "verify"]
print(ttr(words))
print(yules_k({"verify": 2, "your": 1, "account": 1}))
```

The source uses dictionary densities per 100 alphabetic words. For HW-P/MG-P
analysis, compare the resulting feature distributions under identical spaCy
model and dictionary settings; no universal class threshold is defined.
