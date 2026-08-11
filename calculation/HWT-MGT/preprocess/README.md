# HWT/MGT preprocessing adapters

These scripts add the source-repository preparation stages that were omitted
from `calculation/HWT-MGT`. They can download/load models at runtime; the
models are not vendored into `e-phishGen`.

The adapters deliberately stop at prepared model inputs, logits/labels,
perturbed text, token surprisals, or contextual embeddings. The metric
formulas remain in the parent directory.

| Adapter | Original repository and purpose |
|---|---|
| `common.py` | Shared file readers and Hugging Face causal-model helpers |
| `mgtbench.py` | [MGTBench](https://github.com/xinleihe/MGTBench): `gpt2-medium`, PAD=EOS, entropy 512 and likelihood/rank 1024 limits |
| `gltr.py` | [detecting-fake-text](https://github.com/HendrikStrobelt/detecting-fake-text): GPT-2 BOS prepend and GLTR next-token alignment |
| `detectgpt.py` | [detect-gpt](https://github.com/eric-mitchell/detect-gpt): span masking and T5 fill generation |
| `detectllm.py` | [DetectLLM](https://github.com/mbzuai-nlp/DetectLLM): `gpt2-medium` + `t5-small` defaults and source perturbation settings |
| `dna_gpt.py` | [DNA-GPT](https://github.com/Xianjun-Yang/DNA-GPT): JSONL reading, 350-word cap, 50% character prefix, and n-gram normalization |
| `fast_dna_gpt.py` | [fast-detect-gpt](https://github.com/baoguangsheng/fast-detect-gpt): GPT-2 local model, 50% word prefix, and 10 regenerated continuations |
| `fast_detectgpt.py` | [fast-detect-gpt](https://github.com/baoguangsheng/fast-detect-gpt): model aliases, cache lookup, padding, and reference/scoring alignment |
| `gpt_who.py` | [GPT-Who](https://github.com/saranya-venkatraman/gpt-who): CSV input, GPT-2 XL, EOS prepend, and token surprisal vectors |
| `gptid.py` | [GPTID](https://github.com/ArGintum/GPTID): RoBERTa-base, whitespace normalization, 512-token truncation, and special-token removal |
| `perplexity.py` | [Hugging Face perplexity reference](https://huggingface.co/docs/transformers/en/perplexity): strided windows and `-100` context-label masking |

## Usage

Because `HWT-MGT` contains a hyphen, add both directories to `PYTHONPATH`
when importing adapters:

```powershell
$env:PYTHONPATH = "calculation\HWT-MGT;calculation\HWT-MGT\preprocess"
python -c "from mgtbench import load_model; model, tokenizer = load_model()"
```

Most adapters use lazy imports, so importing the modules does not require
PyTorch or Transformers. Running them requires the dependencies and the
source model weights. `dna_gpt.py` prepares OpenAI-compatible prompts but
does not make API requests.

For an HWT/MGT run, record the actual model, cache path, device, tokenizer,
context limit, truncation/window policy, and input file format in the output
metadata. The source defaults are preserved for provenance, but should not
be assumed to be optimal for every experiment.
