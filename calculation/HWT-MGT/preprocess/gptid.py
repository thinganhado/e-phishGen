"""GPTID contextual-embedding preparation."""


DEFAULT_MODEL = "roberta-base-cased"


def load_model(model_name: str = DEFAULT_MODEL, cache_dir: str | None = None, device: str | None = None):
    import torch
    from transformers import RobertaModel, RobertaTokenizer
    kwargs = {} if cache_dir is None else {"cache_dir": cache_dir}
    tokenizer = RobertaTokenizer.from_pretrained(model_name, **kwargs)
    model = RobertaModel.from_pretrained(model_name, **kwargs)
    if device is not None:
        model.to(device)
    model.eval()
    return model, tokenizer


def normalize_text(text: str) -> str:
    return text.replace("\n", " ").replace("  ", " ")


def contextual_embeddings(text: str, model, tokenizer, device: str | None = None):
    """Return the point cloud after GPTID's 512-token/special-token handling."""
    import torch
    text = normalize_text(text)
    encoded = tokenizer(text, truncation=True, max_length=512, return_tensors="pt")
    if device is not None:
        encoded = {key: value.to(device) for key, value in encoded.items()}
    with torch.no_grad():
        hidden = model(**encoded).last_hidden_state[0]
    if hidden.shape[0] <= 2:
        raise ValueError("GPTID requires at least one non-special token")
    return hidden[1:-1].cpu()


__all__ = ["DEFAULT_MODEL", "contextual_embeddings", "load_model", "normalize_text"]
