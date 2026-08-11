"""detecting-fake-text/GLTR input preparation.

Adapted from ``detecting-fake-text/backend/api.py``. The source prepends the
GPT-2 BOS token and uses the resulting token IDs to align next-token labels.
"""


DEFAULT_MODEL = "gpt2"


def load_model(model_name: str = DEFAULT_MODEL, device: str | None = None):
    import torch
    from transformers import GPT2LMHeadModel, GPT2Tokenizer

    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name).to(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    model.eval()
    return model, tokenizer


def prepare_text(text: str, tokenizer):
    import torch

    token_ids = tokenizer(text, return_tensors="pt").input_ids[0]
    start_token = tokenizer(tokenizer.bos_token, return_tensors="pt").input_ids[0]
    return torch.cat([start_token, token_ids]).unsqueeze(0)


def model_inputs(text: str, model, tokenizer, device: str | None = None):
    """Return GLTR-aligned model logits and observed next-token labels."""
    token_ids = prepare_text(text, tokenizer).to(device or next(model.parameters()).device)
    with __import__("torch").no_grad():
        logits = model(token_ids).logits[:, :-1]
    return logits, token_ids[:, 1:]


__all__ = ["DEFAULT_MODEL", "load_model", "model_inputs", "prepare_text"]
