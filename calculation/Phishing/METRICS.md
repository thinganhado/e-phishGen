# Phishing stylometric metrics

Original repository: `C:\Users\donga\Downloads\cross-model-phishing`

The source implementation is `code/05_extract_features.py` and produces these
17 values:

| Feature | Formula / source definition | Reading direction |
|---|---|---|
| TTR | `unique lowercase alphabetic words / alphabetic word tokens` | Higher means greater lexical diversity |
| Mean word length | Mean character length of alphabetic words | Higher means longer words |
| Mean sentence length | `non-space tokens / sentence count` | Higher means longer/more verbose sentences |
| Yule's K | `10000 * (M2 - N) / N²`, with `M2 = sum(frequency²)` | Higher means more word reuse/concentration |
| Clause density | Count of `ROOT`, `ccomp`, `advcl`, `relcl`, `xcomp` dependencies ÷ sentence count | Higher means more clause-structure markers |
| Noun ratio | `NOUN tokens / non-space tokens` | Higher means more nominal style |
| Verb ratio | `VERB tokens / non-space tokens` | Higher means more verb/action content |
| Mean parse depth | Mean distance of tokens to their sentence root; root depth is 0 | Higher means deeper dependency structure |
| Imperative count | Sentences whose first non-space token has tag `VB` and dependency `ROOT` or `ccomp` | Higher means more source-defined imperative patterns |
| First-person ratio | First-person pronouns ÷ alphabetic words | Higher means more authorial/self-reference |
| Second-person ratio | Second-person pronouns ÷ alphabetic words | Higher means more direct reader address |
| Politeness density | `100 * dictionary matches / alphabetic words` | Higher means more source-defined politeness markers |
| Urgency density | `100 * dictionary matches / alphabetic words` | Higher means more urgency markers |
| URL density | `100 * detected URLs / alphabetic words` | Higher means more explicit URLs |
| CTA density | `100 * CTA dictionary matches / alphabetic words` | Higher means more calls to action |
| Authority density | `100 * authority dictionary matches / alphabetic words` | Higher means more authority appeals |
| Time-pressure density | `100 * time-pressure dictionary matches / alphabetic words` | Higher means more deadline/pressure markers |

Source caveats: URL detection recognizes `http://`, `https://`, and `www.`
patterns only. Imperative detection examines only the first non-space token and
accepts both `ROOT` and `ccomp`. Empty inputs return zeros. The source does not
define an HW-P/MG-P threshold; thresholds must be calibrated on labeled data.
