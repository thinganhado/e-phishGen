"""Fast-DNA-GPT local-model preprocessing.

Adapted from ``fast-detect-gpt/scripts/dna_gpt.py``. This prepares the
word-truncated prefix and regenerated continuations; log-probability scoring
is left to the calculation stage.
"""

DEFAULT_MODEL = "gpt2"
DEFAULT_REGEN_NUMBER = 10
DEFAULT_TRUNCATE_RATIO = 0.5


def load_model(model_name: str = DEFAULT_MODEL, cache_dir: str | None = None, device: str = "cuda"):
    from fast_detectgpt import load_model as load_local_model, load_tokenizer
    tokenizer = load_tokenizer(model_name, cache_dir)
    model = load_local_model(model_name, device, cache_dir)
    return model, tokenizer


def prefix_by_words(text: str, truncate_ratio: float = DEFAULT_TRUNCATE_RATIO) -> str:
    words = text.split(" ")
    return " ".join(words[:int(len(words) * truncate_ratio)])


def prepare_prefixes(texts: list[str], truncate_ratio: float = DEFAULT_TRUNCATE_RATIO) -> list[str]:
    return [prefix_by_words(text, truncate_ratio) for text in texts]


def tokenize_prefixes(texts: list[str], tokenizer, device: str = "cuda"):
    return tokenizer(texts, return_tensors="pt", padding=True).to(device)


def generate_continuations(texts: list[str], model, tokenizer, device: str = "cuda",
                           truncate_ratio: float = DEFAULT_TRUNCATE_RATIO,
                           temperature: float = 1.0, top_k: int | None = None,
                           top_p: float | None = None, max_length: int = 200,
                           min_length: int = 150) -> list[str]:
    """Use the source generator settings to prepare local regenerations."""
    import torch

    encoded = tokenize_prefixes(prepare_prefixes(texts, truncate_ratio), tokenizer, device)
    kwargs = {"temperature": temperature}
    if top_p is not None:
        kwargs["top_p"] = top_p
    elif top_k is not None:
        kwargs["top_k"] = top_k
    with torch.no_grad():
        outputs = model.generate(**encoded, min_length=min_length, max_length=max_length,
                                 do_sample=True, **kwargs,
                                 pad_token_id=tokenizer.eos_token_id,
                                 eos_token_id=tokenizer.eos_token_id)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)


def regeneration_inputs(text: str, model, tokenizer, device: str = "cuda",
                         regen_number: int = DEFAULT_REGEN_NUMBER, **generation_kwargs) -> list[str]:
    return generate_continuations([text] * regen_number, model, tokenizer, device, **generation_kwargs)


__all__ = ["generate_continuations", "load_model", "prefix_by_words", "prepare_prefixes",
           "regeneration_inputs", "tokenize_prefixes"]
