"""Calculate DetectGPT scores for every record in a JSON dataset.

DetectGPT raw discrepancy (d) is:
    log_likelihood(original) - mean(log_likelihood(perturbations))

The z-score is the usual DetectGPT score:
    d / standard_deviation(log_likelihood(perturbations))
"""

import argparse
import json
import math
import random
import re
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer


MASK_RE = re.compile(r"<extra_id_\d+>")


def load_records(path):
    path = Path(path)
    raw = path.read_text(encoding="utf-8-sig").strip()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        payload = []
        position = 0
        while position < len(raw):
            while position < len(raw) and raw[position].isspace():
                position += 1
            if position >= len(raw):
                break
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
            records.append({**metadata, "text": text, "sample_id": metadata.get("sample_id", f"sample_{index:04d}")})
    return records


def make_masked_text(text, span_length, pct, buffer_size):
    words = text.split()
    if len(words) <= span_length + 2:
        return None
    n_spans = max(1, int(pct * len(words) / (span_length + 2 * buffer_size)))
    selected = []
    attempts = 0
    while len(selected) < n_spans and attempts < 500:
        attempts += 1
        start = random.randrange(0, len(words) - span_length)
        end = start + span_length
        if any(start < old_end + buffer_size and end + buffer_size > old_start for old_start, old_end in selected):
            continue
        selected.append((start, end))
    if not selected:
        return None
    selected.sort(reverse=True)
    masked = words[:]
    for mask_number, (start, end) in enumerate(selected):
        masked[start:end] = [f"<extra_id_{len(selected) - mask_number - 1}>"]
    return " ".join(masked), len(selected)


def perturb(text, tokenizer, model, device, span_length, pct, buffer_size, top_p):
    masked = make_masked_text(text, span_length, pct, buffer_size)
    if masked is None:
        return text
    masked_text, n_masks = masked
    inputs = tokenizer(masked_text, return_tensors="pt", truncation=True, max_length=512).to(device)
    stop_id = tokenizer.encode(f"<extra_id_{n_masks}>")[0]
    with torch.no_grad():
        output = model.generate(**inputs, max_length=256, do_sample=True, top_p=top_p, eos_token_id=stop_id)
    generated = tokenizer.decode(output[0], skip_special_tokens=False)
    generated = generated.replace("<pad>", "").replace("</s>", "").strip()
    fills = MASK_RE.split(generated)[1:-1]
    if len(fills) < n_masks:
        return text
    result = masked_text
    for i, fill in enumerate(fills[:n_masks]):
        result = result.replace(f"<extra_id_{i}>", fill.strip(), 1)
    return result


def log_likelihood(text, model, tokenizer, device):
    tokens = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024).to(device)
    with torch.no_grad():
        # This matches DetectGPT's run.py: negative causal-LM loss.
        return -model(**tokens, labels=tokens.input_ids).loss.item()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--mask-model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--n-perturbations", type=int, default=10)
    parser.add_argument("--pct-words-masked", type=float, default=0.30)
    parser.add_argument("--span-length", type=int, default=2)
    parser.add_argument("--buffer-size", type=int, default=1)
    parser.add_argument("--mask-top-p", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")

    print(f"Loading scoring model: {args.base_model}")
    base_tokenizer = AutoTokenizer.from_pretrained(args.base_model, local_files_only=True)
    if base_tokenizer.pad_token is None:
        base_tokenizer.pad_token = base_tokenizer.eos_token
    base_model = AutoModelForCausalLM.from_pretrained(args.base_model, local_files_only=True).to(device).eval()

    print(f"Loading mask model: {args.mask_model}")
    mask_tokenizer = AutoTokenizer.from_pretrained(args.mask_model, local_files_only=True)
    mask_model = AutoModelForSeq2SeqLM.from_pretrained(args.mask_model, local_files_only=True).to(device).eval()

    records = load_records(args.dataset)
    print(f"Loaded {len(records)} records")
    results = []
    for number, record in enumerate(records, 1):
        original_ll = log_likelihood(record["text"], base_model, base_tokenizer, device)
        perturbed_texts = [
            perturb(record["text"], mask_tokenizer, mask_model, device, args.span_length,
                    args.pct_words_masked, args.buffer_size, args.mask_top_p)
            for _ in range(args.n_perturbations)
        ]
        perturbed_lls = [log_likelihood(x, base_model, base_tokenizer, device) for x in perturbed_texts]
        mean_ll = float(np.mean(perturbed_lls))
        std_ll = float(np.std(perturbed_lls)) if len(perturbed_lls) > 1 else 1.0
        if std_ll == 0:
            std_ll = 1.0
        discrepancy = original_ll - mean_ll
        result = {
            "sample_id": record["sample_id"],
            "detectgpt_score": discrepancy / std_ll,
            "raw_discrepancy_d": discrepancy,
            "original_log_likelihood": original_ll,
            "mean_perturbed_log_likelihood": mean_ll,
            "perturbed_log_likelihood_std": std_ll,
            "n_perturbations": args.n_perturbations,
            "perturbed_log_likelihoods": perturbed_lls,
        }
        for key in ("origin", "phishing_label", "language", "source"):
            if key in record:
                result[key] = record[key]
        results.append(result)
        print(f"[{number}/{len(records)}] {record['sample_id']}: score={result['detectgpt_score']:.6f}")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(results)} results to {output.resolve()}")


if __name__ == "__main__":
    main()
