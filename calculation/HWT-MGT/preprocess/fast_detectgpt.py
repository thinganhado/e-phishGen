"""Fast-DetectGPT model loading and two-model input alignment.

The model aliases, cache lookup, tokenizer padding, and float16 choices are
adapted from ``fast-detect-gpt/scripts/model.py``. The shifted logits/labels
are prepared exactly as in ``scripts/fast_detect_gpt.py``; the criterion
itself remains in ``../fast_detectgpt_criterion.py``.
"""

MODEL_FULLNAMES = {
    "gpt2": "gpt2", "gpt2-xl": "gpt2-xl", "opt-2.7b": "facebook/opt-2.7b",
    "gpt-neo-2.7B": "EleutherAI/gpt-neo-2.7B", "gpt-j-6B": "EleutherAI/gpt-j-6B",
    "gpt-neox-20b": "EleutherAI/gpt-neox-20b", "mgpt": "sberbank-ai/mGPT",
    "pubmedgpt": "stanford-crfm/pubmedgpt", "mt5-xl": "google/mt5-xl",
    "llama-13b": "huggyllama/llama-13b", "llama2-13b": "TheBloke/Llama-2-13B-fp16",
    "bloom-7b1": "bigscience/bloom-7b1", "opt-13b": "facebook/opt-13b",
    "falcon-7b": "tiiuae/falcon-7b", "falcon-7b-instruct": "tiiuae/falcon-7b-instruct",
}
FLOAT16_MODELS = {"gpt-neo-2.7B", "gpt-j-6B", "gpt-neox-20b", "llama-13b", "llama2-13b",
                  "bloom-7b1", "opt-13b", "falcon-7b", "falcon-7b-instruct"}


def full_name(model_name: str) -> str:
    return MODEL_FULLNAMES.get(model_name, model_name)


def load_tokenizer(model_name: str, cache_dir: str | None = None):
    from transformers import AutoTokenizer
    from_pretrained = _cached_from_pretrained(AutoTokenizer, full_name(model_name), cache_dir)
    kwargs = {"padding_side": "right"}
    if full_name(model_name).startswith("facebook/opt-"):
        kwargs["fast"] = False
    tokenizer = from_pretrained(**kwargs)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
        if "13b" in full_name(model_name):
            tokenizer.pad_token_id = 0
    return tokenizer


def load_model(model_name: str, device: str = "cuda", cache_dir: str | None = None):
    import torch
    from transformers import AutoModelForCausalLM
    kwargs = {}
    if model_name in FLOAT16_MODELS:
        kwargs["torch_dtype"] = torch.float16
    if "gpt-j" in model_name:
        kwargs["revision"] = "float16"
    model = _cached_from_pretrained(AutoModelForCausalLM, full_name(model_name), cache_dir)(**kwargs)
    model.to(device)
    model.eval()
    return model


def _cached_from_pretrained(cls, model_name: str, cache_dir: str | None):
    from pathlib import Path
    if cache_dir:
        local_path = Path(cache_dir) / ("local." + model_name.replace("/", "_"))
        if local_path.exists():
            return lambda **kwargs: cls.from_pretrained(str(local_path), **kwargs)
    return lambda **kwargs: cls.from_pretrained(model_name, cache_dir=cache_dir, **kwargs)


def model_inputs(text: str, tokenizer, model, device: str = "cuda"):
    import torch
    encoded = tokenizer(text, truncation=True, return_tensors="pt", padding=True,
                        return_token_type_ids=False).to(device)
    labels = encoded.input_ids[:, 1:]
    with torch.no_grad():
        logits_score = model(**encoded).logits[:, :-1]
    return encoded, logits_score, labels


def aligned_two_model_inputs(text: str, sampling_tokenizer, sampling_model,
                             scoring_tokenizer, scoring_model, device: str = "cuda"):
    _, logits_score, labels = model_inputs(text, scoring_tokenizer, scoring_model, device)
    encoded_ref = sampling_tokenizer(text, truncation=True, return_tensors="pt", padding=True,
                                     return_token_type_ids=False).to(device)
    if not __import__("torch").equal(encoded_ref.input_ids[:, 1:], labels):
        raise ValueError("sampling and scoring tokenizers produced different next-token labels")
    with __import__("torch").no_grad():
        logits_ref = sampling_model(**encoded_ref).logits[:, :-1]
    return logits_ref, logits_score, labels


__all__ = ["aligned_two_model_inputs", "full_name", "load_model", "load_tokenizer", "model_inputs"]
