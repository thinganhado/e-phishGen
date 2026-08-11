"""Run the HWT/MGT metrics for e-phishGen's matched_pool_44 dataset.

The runner treats every ``samples[*]`` entry as an independent input and
records both metric values and per-metric errors. It uses only local model
paths and writes JSON/Markdown output under ``results/``.
"""

from __future__ import annotations

import gc
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer, RobertaModel, RobertaTokenizer


ROOT = Path(__file__).resolve().parents[2]
PREPROCESS = Path(__file__).resolve().parent / "preprocess"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from average_log_probability import average_log_probability
from detectgpt_curvature import detectgpt_discrepancy
from dna_gpt_score import dna_gpt_score
from fast_detectgpt_criterion import analytic_sampling_discrepancy, sampling_discrepancy
from lrr import lrr
from mean_log_rank import mean_log_rank
from mean_token_rank import mean_token_rank
from mle_intrinsic_dimension import mle_intrinsic_dimension
from ngram_overlap_ratio import ngram_overlap_ratio
from npr import npr
from negative_mean_log_rank import negative_mean_log_rank
from negative_mean_token_rank import negative_mean_token_rank
from perplexity import perplexity_from_log_probs
from phd_intrinsic_dimension import phd_intrinsic_dimension
from predictive_entropy import predictive_entropy
from probability_fraction import probability_fraction
from rank_100_1000_ratio import rank_100_1000_ratio
from rank_10_100_ratio import rank_10_100_ratio
from rank_gt1000_ratio import rank_gt1000_ratio
from top10_entropy import top10_entropy
from top10_rank_ratio import top10_rank_ratio
from total_surprisal import total_surprisal
from uid_diff import uid_diff
from uid_diff2 import uid_diff2
from uid_max_span import uid_max_span
from uid_mean import uid_mean
from uid_min_span import uid_min_span
from uid_variance import uid_variance
from weighted_ngram_score import weighted_ngram_score

# The calculation directory and preprocessing directory both contain a
# module named ``common``. Load the calculation helpers first, then replace
# the import binding for the preprocessing adapters.
_calculation_common = sys.modules.get("common")
sys.path.insert(0, str(PREPROCESS))
sys.modules.pop("common", None)
import common as _preprocess_common  # noqa: F401,E402
from preprocess import detectgpt, dna_gpt, fast_dna_gpt, gpt_who, gptid


DATASET = ROOT / "matched_pool_44.json"
MODEL_ROOT = Path(r"E:\AI\models")
OUTPUT_DIR = Path(__file__).resolve().parent / "results"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODELS = {
    "causal": MODEL_ROOT / "gpt2-medium",
    "perplexity": MODEL_ROOT / "gpt2-large",
    "uid": MODEL_ROOT / "gpt2-xl",
    "mask": MODEL_ROOT / "t5-large",
    "embedding": MODEL_ROOT / "roberta-base-cased",
}
PERTURBATIONS = 5
REGENERATIONS = 10


def load_causal(path: Path):
    tokenizer = AutoTokenizer.from_pretrained(str(path), local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(str(path), local_files_only=True).to(DEVICE)
    model.eval()
    return model, tokenizer


def scalarize(value):
    if isinstance(value, torch.Tensor):
        if value.ndim == 0:
            return float(value.detach().cpu().item())
        return [scalarize(item) for item in value.detach().cpu().flatten()]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def put(result, name, value):
    result["metrics"][name] = scalarize(value)


def fail(result, name, exc):
    result["errors"][name] = f"{type(exc).__name__}: {exc}"


def score_text(text, model, tokenizer, max_length=1024):
    encoded = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length)
    encoded = {key: value.to(DEVICE) for key, value in encoded.items()}
    with torch.no_grad():
        logits = model(**encoded).logits[:, :-1]
    labels = encoded["input_ids"][:, 1:]
    return logits[0].detach(), labels[0].detach()


def score_continuation(text, prefix, model, tokenizer):
    encoded = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
    prefix_ids = tokenizer(prefix, add_special_tokens=False).input_ids
    encoded = {key: value.to(DEVICE) for key, value in encoded.items()}
    with torch.no_grad():
        logits = model(**encoded).logits[0]
    labels = encoded["input_ids"][0]
    start = max(1, min(len(prefix_ids), labels.numel() - 1))
    log_probs = torch.log_softmax(logits[start - 1:-1], dim=-1)
    target = labels[start:]
    if target.numel() == 0:
        raise ValueError("generated text has no continuation tokens")
    return float(log_probs.gather(1, target[:, None]).squeeze(1).mean().cpu().item())


def calculate_causal_metrics(result, logits, labels):
    values = {
        "predictive_entropy": predictive_entropy(logits),
        "top10_entropy": top10_entropy(logits),
        "average_log_probability": average_log_probability(logits, labels),
        "perplexity_from_causal_log_probs": perplexity_from_log_probs(
            torch.log_softmax(logits, -1).gather(1, labels[:, None]).squeeze(1)
        ),
        "mean_token_rank": mean_token_rank(logits, labels),
        "mean_log_rank": mean_log_rank(logits, labels),
        "negative_mean_token_rank": negative_mean_token_rank(logits, labels),
        "negative_mean_log_rank": negative_mean_log_rank(logits, labels),
        "top10_rank_ratio": top10_rank_ratio(logits, labels),
        "rank_10_100_ratio": rank_10_100_ratio(logits, labels),
        "rank_100_1000_ratio": rank_100_1000_ratio(logits, labels),
        "rank_gt1000_ratio": rank_gt1000_ratio(logits, labels),
        "probability_fraction": probability_fraction(logits, labels),
        "lrr": lrr(average_log_probability(logits, labels), mean_log_rank(logits, labels)),
    }
    for name, value in values.items():
        put(result, name, value)


def calculate_ppl(result, text, model, tokenizer):
    logits, labels = score_text(text, model, tokenizer, max_length=1024)
    log_probs = torch.log_softmax(logits, -1).gather(1, labels[:, None]).squeeze(1)
    put(result, "perplexity_gpt2_large", perplexity_from_log_probs(log_probs))


def calculate_uid(result, text, model, tokenizer):
    values = gpt_who.token_surprisals(text, model, tokenizer, device=DEVICE)
    for name, fn in {
        "uid_mean": uid_mean,
        "total_surprisal": total_surprisal,
        "uid_variance": uid_variance,
        "uid_diff": uid_diff,
        "uid_diff2": uid_diff2,
        "uid_min_span": uid_min_span,
        "uid_max_span": uid_max_span,
    }.items():
        try:
            put(result, name, fn(values))
        except Exception as exc:
            fail(result, name, exc)


def calculate_embeddings(result, text, model, tokenizer):
    embeddings = gptid.contextual_embeddings(text, model, tokenizer, device=DEVICE).numpy()
    try:
        phd_value = phd_intrinsic_dimension(embeddings, seed=0)
    except ValueError as exc:
        # The original PHD defaults need at least two subsample sizes.
        # Short samples use smaller sizes with the same estimator.
        if "at least two subsample sizes" not in str(exc):
            raise
        min_points = max(2, min(40, embeddings.shape[0] // 3))
        phd_value = phd_intrinsic_dimension(
            embeddings,
            min_points=min_points,
            max_points=embeddings.shape[0],
            point_jump=min_points,
            seed=0,
        )
    for name, value in {
        "phd_intrinsic_dimension": phd_value,
        "mle_intrinsic_dimension": mle_intrinsic_dimension(embeddings),
    }.items():
        try:
            put(result, name, value)
        except Exception as exc:
            fail(result, name, exc)


def calculate_perturbation(result, text, base_model, base_tokenizer, mask_model, mask_tokenizer):
    original_logits, original_labels = score_text(text, base_model, base_tokenizer)
    original_ll = average_log_probability(original_logits, original_labels)
    original_lr = mean_log_rank(original_logits, original_labels)
    perturbed = detectgpt.perturb_texts(
        [text] * PERTURBATIONS, mask_model, mask_tokenizer,
        device=DEVICE, max_length=150,
    )
    perturbed_ll = []
    perturbed_lr = []
    for item in perturbed:
        logits, labels = score_text(item, base_model, base_tokenizer)
        perturbed_ll.append(average_log_probability(logits, labels))
        perturbed_lr.append(mean_log_rank(logits, labels))
    put(result, "detectgpt_discrepancy", detectgpt_discrepancy(original_ll, perturbed_ll))
    put(result, "detectgpt_normalized_discrepancy", detectgpt_discrepancy(original_ll, perturbed_ll, normalized=True))
    put(result, "npr", npr(original_lr, perturbed_lr))
    put(result, "perturbation_count", len(perturbed))


def calculate_fast_detect(result, text, model, tokenizer):
    logits, labels = score_text(text, model, tokenizer)
    samples = torch.multinomial(torch.softmax(logits, -1), num_samples=10)
    put(result, "fast_detectgpt_analytic", analytic_sampling_discrepancy(logits, logits, labels))
    put(result, "fast_detectgpt_sampling", sampling_discrepancy(logits, logits, labels, samples))


def calculate_dna(result, text, model, tokenizer):
    prompt = dna_gpt.build_prompt(text)
    encoded = tokenizer(prompt["prefix"], return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        generated = model.generate(
            **encoded, do_sample=True, temperature=1.0, top_k=40,
            max_new_tokens=120, num_return_sequences=REGENERATIONS,
            pad_token_id=tokenizer.eos_token_id,
        )
    decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
    target_tokens = dna_gpt.tokenize_for_ngrams(prompt["continuation"])
    overlap = []
    weighted = []
    regenerated_scores = []
    for item in decoded:
        suffix = item[len(prompt["prefix"]):] if item.startswith(prompt["prefix"]) else item
        generated_tokens = dna_gpt.tokenize_for_ngrams(suffix)
        overlap.append(ngram_overlap_ratio(target_tokens, generated_tokens, 1))
        weighted.append(weighted_ngram_score(target_tokens, generated_tokens))
        regenerated_scores.append(score_continuation(item, prompt["prefix"], model, tokenizer))
    original_score = score_continuation(prompt["text"], prompt["prefix"], model, tokenizer)
    put(result, "ngram_overlap_ratio", float(np.mean(overlap)))
    put(result, "weighted_ngram_score", float(np.mean(weighted)))
    put(result, "dna_gpt_regeneration_log_probability_difference", dna_gpt_score(original_score, regenerated_scores))
    put(result, "regeneration_count", len(decoded))


def write_outputs(results, metadata):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"metadata": metadata, "results": results}
    json_path = OUTPUT_DIR / "matched_pool_44_metrics.json"
    md_path = OUTPUT_DIR / "matched_pool_44_metrics.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=scalarize), encoding="utf-8")

    metric_names = sorted({name for row in results for name in row["metrics"]})
    lines = ["# HWT/MGT metrics: matched_pool_44", "", "## Metadata", "", "```json", json.dumps(metadata, indent=2), "```", ""]
    for metric in metric_names:
        lines.extend([f"## {metric}", "", "| sample_id | group | value |", "|---|---|---:|"])
        for row in results:
            if metric in row["metrics"]:
                value = json.dumps(row["metrics"][metric], ensure_ascii=False)
                lines.append(f"| {row['sample_id']} | {row['group']} | `{value}` |")
        lines.append("")
    lines.extend(["## Errors", "", "| sample_id | metric | error |", "|---|---|---|"])
    for row in results:
        for metric, error in row["errors"].items():
            lines.append(f"| {row['sample_id']} | {metric} | `{error}` |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE {json_path}")
    print(f"WROTE {md_path}")


def release(*models):
    for model in models:
        del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def main():
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    samples = data["samples"]
    results = [
        {"sample_id": sample["sample_id"], "group": sample["group"],
         "match_stratum": sample["match_stratum"], "metrics": {}, "errors": {}}
        for sample in samples
    ]
    texts = [sample["text"] for sample in samples]
    metadata = {
        "dataset": str(DATASET), "sample_count": len(samples), "device": DEVICE,
        "torch": torch.__version__, "cuda": torch.version.cuda,
        "models": {key: str(value) for key, value in MODELS.items()},
        "perturbations": PERTURBATIONS, "regenerations": REGENERATIONS,
        "started_utc": datetime.now(timezone.utc).isoformat(),
    }

    print(f"Running {len(samples)} samples on {DEVICE}")
    causal_model, causal_tokenizer = load_causal(MODELS["causal"])
    for index, (result, text) in enumerate(zip(results, texts), 1):
        print(f"causal {index}/{len(results)} {result['sample_id']}")
        try:
            logits, labels = score_text(text, causal_model, causal_tokenizer)
            calculate_causal_metrics(result, logits, labels)
            calculate_fast_detect(result, text, causal_model, causal_tokenizer)
        except Exception as exc:
            fail(result, "causal_metrics", exc)
    release(causal_model, causal_tokenizer)

    ppl_model, ppl_tokenizer = load_causal(MODELS["perplexity"])
    for index, (result, text) in enumerate(zip(results, texts), 1):
        print(f"perplexity {index}/{len(results)} {result['sample_id']}")
        try:
            calculate_ppl(result, text, ppl_model, ppl_tokenizer)
        except Exception as exc:
            fail(result, "perplexity_gpt2_large", exc)
    release(ppl_model, ppl_tokenizer)

    uid_model, uid_tokenizer = load_causal(MODELS["uid"])
    for index, (result, text) in enumerate(zip(results, texts), 1):
        print(f"uid {index}/{len(results)} {result['sample_id']}")
        try:
            calculate_uid(result, text, uid_model, uid_tokenizer)
        except Exception as exc:
            fail(result, "uid_metrics", exc)
    release(uid_model, uid_tokenizer)

    embedding_tokenizer = RobertaTokenizer.from_pretrained(str(MODELS["embedding"]), local_files_only=True)
    embedding_model = RobertaModel.from_pretrained(str(MODELS["embedding"]), local_files_only=True).to(DEVICE)
    embedding_model.eval()
    for index, (result, text) in enumerate(zip(results, texts), 1):
        print(f"embedding {index}/{len(results)} {result['sample_id']}")
        try:
            calculate_embeddings(result, text, embedding_model, embedding_tokenizer)
        except Exception as exc:
            fail(result, "embedding_metrics", exc)
    release(embedding_model, embedding_tokenizer)

    base_model, base_tokenizer = load_causal(MODELS["causal"])
    mask_tokenizer = AutoTokenizer.from_pretrained(str(MODELS["mask"]), local_files_only=True)
    mask_model = AutoModelForSeq2SeqLM.from_pretrained(str(MODELS["mask"]), local_files_only=True).to(DEVICE)
    mask_model.eval()
    for index, (result, text) in enumerate(zip(results, texts), 1):
        print(f"perturbation {index}/{len(results)} {result['sample_id']}")
        try:
            calculate_perturbation(result, text, base_model, base_tokenizer, mask_model, mask_tokenizer)
        except Exception as exc:
            fail(result, "perturbation_metrics", exc)
    release(base_model, base_tokenizer, mask_model, mask_tokenizer)

    dna_model, dna_tokenizer = load_causal(MODELS["causal"])
    for index, (result, text) in enumerate(zip(results, texts), 1):
        print(f"generation {index}/{len(results)} {result['sample_id']}")
        try:
            calculate_dna(result, text, dna_model, dna_tokenizer)
        except Exception as exc:
            fail(result, "dna_metrics", exc)
    release(dna_model, dna_tokenizer)

    metadata["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_outputs(results, metadata)


if __name__ == "__main__":
    main()
