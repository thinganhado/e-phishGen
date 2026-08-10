r"""Calculate per-email NPR using local causal and mask-filling models.

Example:
python calculate_npr.py `
  --dataset C:\Users\Admin\Documents\GitHub\e-phishGen\dataset `
  --base-model C:\Users\Admin\Documents\LLMs\gpt2-xl `
  --mask-model C:\Users\Admin\Documents\LLMs\t5-large `
  --output C:\Users\Admin\Documents\GitHub\e-phishGen\dataset\npr_results.json
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
    if path.is_dir():
        candidates = sorted(path.glob("*.json"))
        if not candidates:
            raise FileNotFoundError(f"No JSON files found in {path}")
        if len(candidates) > 1:
            preferred = [p for p in candidates if "sample" in p.name.lower()]
            candidates = preferred or candidates
        path = candidates[0]

    raw = path.read_text(encoding="utf-8-sig").strip()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        # Also support JSON Lines and files containing multiple concatenated
        # JSON arrays/objects, which otherwise raise "Extra data".
        decoder = json.JSONDecoder()
        payload = []
        position = 0
        while position < len(raw):
            while position < len(raw) and raw[position].isspace():
                position += 1
            if position >= len(raw):
                break
            value, end = decoder.raw_decode(raw, position)
            if isinstance(value, list):
                payload.extend(value)
            else:
                payload.append(value)
            position = end
    if isinstance(payload, dict) and "samples" in payload:
        payload = payload["samples"]
    if not isinstance(payload, list):
        raise ValueError("Dataset JSON must be a list or an object containing a 'samples' list")

    records = []
    for index, item in enumerate(payload):
        if isinstance(item, str):
            text = item.strip()
            metadata = {}
        else:
            metadata = dict(item)
            text = metadata.get("text")
            if not text and (metadata.get("Subject") or metadata.get("Body")):
                text = f"{metadata.get('Subject', '')}\n\n{metadata.get('Body', '')}"
            text = (text or "").strip()
        if text:
            records.append({**metadata, "sample_id": metadata.get("sample_id", f"sample_{index:04d}"), "text": text})
    return records


def mask_text(text, span_length, pct_words_masked, buffer_size):
    words = text.split()
    if len(words) <= span_length + 2:
        return None
    n_spans = max(1, int(pct_words_masked * len(words) / (span_length + 2 * buffer_size)))
    tokens = words[:]
    mask_positions = []
    attempts = 0
    while len(mask_positions) < n_spans and attempts < 500:
        attempts += 1
        start = random.randint(0, len(words) - span_length - 1)
        end = start + span_length
        search_start = max(0, start - buffer_size)
        search_end = min(len(words), end + buffer_size)
        if any(i < search_end and i + span_length > search_start for i in mask_positions):
            continue
        mask_positions.append(start)
        tokens[start:end] = [f"<extra_id_{len(mask_positions)-1}>"]
        words = words[:start] + [f"<extra_id_{len(mask_positions)-1}>"] + words[end:]
    if not mask_positions:
        return None
    return " ".join(words), len(mask_positions)


def perturb_once(text, mask_tokenizer, mask_model, device, span_length, pct, buffer_size, top_p):
    masked = mask_text(text, span_length, pct, buffer_size)
    if masked is None:
        return text
    masked_text, n_masks = masked
    inputs = mask_tokenizer(masked_text, return_tensors="pt", truncation=True, max_length=512).to(device)
    stop_id = mask_tokenizer.encode(f"<extra_id_{n_masks}>")[0]
    with torch.no_grad():
        output = mask_model.generate(
            **inputs, max_length=256, do_sample=True, top_p=top_p,
            num_return_sequences=1, eos_token_id=stop_id,
        )
    generated = mask_tokenizer.decode(output[0], skip_special_tokens=False)
    generated = generated.replace("<pad>", "").replace("</s>", "").strip()
    fills = MASK_RE.split(generated)[1:-1]
    if len(fills) < n_masks:
        return text
    result = masked_text
    for i in range(n_masks):
        result = result.replace(f"<extra_id_{i}>", fills[i].strip(), 1)
    return result.strip()


def average_log_rank(text, model, tokenizer, device):
    encoded = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024).to(device)
    with torch.no_grad():
        logits = model(**encoded).logits[:, :-1, :]
    labels = encoded.input_ids[:, 1:]
    target_logits = logits.gather(-1, labels.unsqueeze(-1)).squeeze(-1)
    ranks = (logits > target_logits.unsqueeze(-1)).sum(dim=-1).float() + 1.0
    return torch.log(ranks).mean().item()


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
        raise RuntimeError("CUDA was requested but is not available")

    print(f"Loading scoring model: {args.base_model}")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.base_model, local_files_only=True).to(device).eval()

    print(f"Loading mask model: {args.mask_model}")
    mask_tokenizer = AutoTokenizer.from_pretrained(args.mask_model, local_files_only=True)
    mask_model = AutoModelForSeq2SeqLM.from_pretrained(args.mask_model, local_files_only=True).to(device).eval()

    records = load_records(args.dataset)
    output = []
    for index, record in enumerate(records, 1):
        text = record["text"]
        original = average_log_rank(text, model, tokenizer, device)
        perturbed = [
            perturb_once(text, mask_tokenizer, mask_model, device, args.span_length,
                         args.pct_words_masked, args.buffer_size, args.mask_top_p)
            for _ in range(args.n_perturbations)
        ]
        perturbed_scores = [average_log_rank(x, model, tokenizer, device) for x in perturbed]
        mean_perturbed = float(np.mean(perturbed_scores))
        result = {
            "sample_id": record.get("sample_id", f"sample_{index-1:04d}"),
            "npr": mean_perturbed / original if original else math.nan,
            "original_logrank": original,
            "mean_perturbed_logrank": mean_perturbed,
            "n_perturbations": args.n_perturbations,
            "perturbed_logranks": perturbed_scores,
        }
        for key in ("origin", "phishing_label", "language", "source"):
            if key in record:
                result[key] = record[key]
        output.append(result)
        print(f"[{index}/{len(records)}] {result['sample_id']}: NPR={result['npr']:.6f}")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(output)} results to {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
