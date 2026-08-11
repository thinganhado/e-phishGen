# Dependency inventory and environment split

The `original/` directory contains copies of every dependency declaration
found in the source repositories:

| Source repository | Copied declaration |
|---|---|
| [detecting-fake-text](https://github.com/HendrikStrobelt/detecting-fake-text) | `original/detecting-fake-text-requirements.txt` |
| [MGTBench](https://github.com/xinleihe/MGTBench) | `original/MGTBench-environment.yml` |
| [detect-gpt](https://github.com/eric-mitchell/detect-gpt) | `original/detect-gpt-requirements.txt` |
| [DNA-GPT](https://github.com/Xianjun-Yang/DNA-GPT) | `original/DNA-GPT-requirements.txt` |
| [DetectLLM](https://github.com/mbzuai-nlp/DetectLLM) | `original/DetectLLM-requirements.txt` |
| [fast-detect-gpt](https://github.com/baoguangsheng/fast-detect-gpt) | `original/fast-detect-gpt-requirements.txt` |
| [GPT-Who](https://github.com/saranya-venkatraman/gpt-who) | `original/gpt-who-requirements.txt` |
| [GPTID](https://github.com/ArGintum/GPTID) | No requirements file; inferred from `README.md` and `example.ipynb` |

The original MGTBench and DetectLLM files are full historical environments,
including benchmark/UI packages that are not required for the metric
calculation adapters. The consolidated files in this directory are therefore
deliberately separate from the copied originals.

The copied MGTBench environment is a Linux/CUDA export with an absolute Linux
prefix, and the copied DetectLLM requirements include Linux CUDA wheels and
DeepSpeed. Treat both as provenance records rather than Windows installation
files.

## Minimum practical environment count

For `e-phishGen` metric work, the minimum practical count is **two Python
environments**:

| Environment | Use for | Reason |
|---|---|---|
| `metric-core-py38.txt` | MGTBench, detecting-fake-text metric code, DetectGPT, DNA-GPT, DetectLLM, Fast-DetectGPT, and the Hugging Face perplexity preparation | Shares the PyTorch 1.13-era stack and a common Transformers 4.28.1 interface. MGTBench's older 4.24 pin is relaxed here because the documented metric APIs are compatible. |
| `gptwho-gptid-py38.txt` | GPT-Who and GPTID | Preserves GPT-Who's PyTorch 2.0.1/Transformers 4.30.0 pins and adds GPTID's SciPy/scikit-dimension dependencies. |

The detecting-fake-text web server can use the first environment after
installing `detecting-fake-text-server-optional.txt`. Its JavaScript client
has a separate `npm install` workflow and is not a Python dependency.

`huggingface-perplexity-reference.txt` records the standalone dependencies
for the Hugging Face reference; those packages are already covered by the
core environment.

## Why not one environment?

A single modern environment may work if exact source-version reproduction is
not required. It is not the recommended baseline here because GPT-Who pins
PyTorch 2.0.1/Transformers 4.30.0, while MGTBench and DetectLLM were released
against PyTorch 1.13.1 and older/different Transformers versions. Keeping two
environments makes the source differences explicit and avoids silently
changing tokenization or model-loading behavior.

For strict reproduction of every repository's historical lockfile, use the
copied files under `original/` directly. That requires more than two isolated
environments because MGTBench's `environment.yml` and DetectLLM's fully pinned
requirements intentionally contain incompatible historical pins.

## Installation examples

```powershell
python -m venv .venv-metric-core
.\.venv-metric-core\Scripts\python.exe -m pip install -r calculation\HWT-MGT\requirements\metric-core-py38.txt

python -m venv .venv-gptwho-gptid
.\.venv-gptwho-gptid\Scripts\python.exe -m pip install -r calculation\HWT-MGT\requirements\gptwho-gptid-py38.txt
```

The original DNA-GPT utilities also load the spaCy model `en_core_web_sm`;
install it separately when running those original utilities:

```powershell
python -m spacy download en_core_web_sm
```

Model weights are downloaded by the preprocessing adapters at runtime and
are not included in these requirement files.
