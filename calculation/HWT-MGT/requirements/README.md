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

## Final CUDA environments

The four final environments use Python 3.13 and the tested CUDA stack
`torch==2.11.0+cu128` with CUDA 12.8. This is the supported setup for the
RTX 5090 in this workspace:

| Environment | Use for | Reason |
|---|---|---|
| `metric-core-py38.txt` | MGTBench, detecting-fake-text metric code, DetectGPT, DNA-GPT, DetectLLM, Fast-DetectGPT, and intrinsic-dimension metrics | Consolidated CUDA environment; the filename is retained for compatibility with existing references. |
| `gptwho-gptid-py38.txt` | GPT-Who and GPTID | Uses the same tested CUDA stack and includes `scikit-dimension`. |
| `detecting-fake-text-server-optional.txt` | GLTR plus the optional detecting-fake-text server | Includes Transformers because GLTR loads GPT-2 through Transformers. |
| `huggingface-perplexity-reference.txt` | Hugging Face perplexity reference | Minimal CUDA-enabled reference environment. |

The detecting-fake-text web server can use the first environment after
installing `detecting-fake-text-server-optional.txt`. Its JavaScript client
has a separate `npm install` workflow and is not a Python dependency.

All four environments were tested with local model paths under
`E:\AI\models`. Each passed `pip check`, CUDA initialization, and a model
forward pass on the RTX 5090. The direct dependencies are pinned in the four
requirement files.

## Why retain four environments?

A single modern environment may work, but the four files preserve the
original calculation groupings while sharing a known-good CUDA baseline.
They are execution environments rather than strict historical reproductions;
the old Python 3.8/PyTorch pins were incompatible with the repository's
Python 3.10-style type annotations and the RTX 5090.

For strict reproduction of every repository's historical lockfile, use the
copied files under `original/` directly. That requires more than two isolated
environments because MGTBench's `environment.yml` and DetectLLM's fully pinned
requirements intentionally contain incompatible historical pins.

## Installation examples

```powershell
mamba create -n hwt_metric_core python=3.13 pip -y
mamba run -n hwt_metric_core python -m pip install -r calculation\HWT-MGT\requirements\metric-core-py38.txt

mamba create -n hwt_gptwho_gptid python=3.13 pip -y
mamba run -n hwt_gptwho_gptid python -m pip install -r calculation\HWT-MGT\requirements\gptwho-gptid-py38.txt
```

The original DNA-GPT utilities also load the spaCy model `en_core_web_sm`;
install it separately when running those original utilities:

```powershell
python -m spacy download en_core_web_sm
```

Model weights are downloaded by the preprocessing adapters at runtime and
are not included in these requirement files.
