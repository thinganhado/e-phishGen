# Phishing metric dependencies

Original declaration copied to
[`original/cross-model-phishing-requirements.txt`](original/cross-model-phishing-requirements.txt).

The source declares `pandas`, `tqdm`, and `openai`. Feature extraction also
requires spaCy and the English model `en_core_web_sm`; the evaluation and
figure scripts additionally use scikit-learn, XGBoost, SHAP, matplotlib, and
seaborn.

The separated calculation scripts in the parent directory use only the Python
standard library. The preprocessing environment is therefore needed only when
running the copied corpus/NLP pipeline.
