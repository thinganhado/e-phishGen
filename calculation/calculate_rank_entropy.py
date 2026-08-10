"""Calculate per-sample average token rank and top-k entropy.

The implementation matches the GLTR repository:
- rank is the position of the observed next token in descending model probability
- entropy is normalized entropy over the top-k predictions, with k=10 by default
"""

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_records(path):
    raw = Path(path).read_text(encoding="utf-8-sig").strip()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        payload = []
        position = 0
        while position < len(raw):
            while position < len(raw) and raw[position].isspace():
                position += 1
            value, position = decoder.raw_decode(raw, position)
            payload.extend(value if isinstance(value, list) else [value])

    if isinstance(payload, dict):
        payload = payload.get("samples", [payload])

    records = []
    for index, item in enumerate(payload):
        if isinstance(item, str):
            text, metadata = item.strip(), {}
        else:
            metadata = dict(item)
            text = metadata.get("text") or metadata.get("email") or metadata.get("content")
            if not text and (metadata.get("Subject") or metadata.get("Body")):
                text = f"{metadata.get('Subject', '')}\n\n{metadata.get('Body', '')}"
            text = (text or "").strip()
        if text:
            records.append({
                **metadata,
                "text": text,
                "sample_id": metadata.get("sample_id", f"sample_{index:04d}"),
            })
    return records


def calculate_metrics(text, model, tokenizer, device, top_k, max_length):
    encoded = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length).to(device)
    with torch.no_grad():
        logits = model(**encoded).logits[:, :-1, :]

    labels = encoded.input_ids[:, 1:]
    if labels.shape[1] == 0:
        return {"n_tokens": 0, "average_rank_zero_based": None, "average_rank_one_based": None, "average_entropy_topk": None}

    target_logits = logits.gather(-1, labels.unsqueeze(-1)).squeeze(-1)
    # Count logits strictly greater than the observed token's logit.
    # This is equivalent to its zero-based descending rank in normal cases.
    ranks_zero_based = (logits > target_logits.unsqueeze(-1)).sum(dim=-1).float()
    k = min(top_k, logits.shape[-1])
    top_logits = torch.topk(logits, k=k, dim=-1).values
    top_probabilities = torch.softmax(top_logits, dim=-1)
    entropy = -(top_probabilities * torch.log(top_probabilities.clamp_min(1e-12))).sum(dim=-1)

    return {
        "n_tokens": int(labels.shape[1]),
        "average_rank_zero_based": float(ranks_zero_based.mean().item()),
        "average_rank_one_based": float((ranks_zero_based + 1).mean().item()),
        "average_entropy_topk": float(entropy.mean().item()),
        "top_k": k,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--max-length", type=int, default=1024)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")

    print(f"Loading model: {args.model}")
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(args.model, local_files_only=True).to(device).eval()
    records = load_records(args.dataset)
    print(f"Loaded {len(records)} samples")

    results = []
    for number, record in enumerate(records, 1):
        metrics = calculate_metrics(record["text"], model, tokenizer, device, args.top_k, args.max_length)
        result = {"sample_id": record["sample_id"], **metrics}
        for key in ("origin", "phishing_label", "language", "source"):
            if key in record:
                result[key] = record[key]
        results.append(result)
        print(
            f"[{number}/{len(records)}] {record['sample_id']}: "
            f"rank={metrics['average_rank_one_based']:.3f}, "
            f"entropy={metrics['average_entropy_topk']:.3f}"
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(results)} results to {output.resolve()}")


if __name__ == "__main__":
    main()
