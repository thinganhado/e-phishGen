"""Resumable stage runner for run_matched_pool_44.py."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, RobertaModel, RobertaTokenizer

import run_matched_pool_44 as run


PARTIAL = run.OUTPUT_DIR / "matched_pool_44_metrics.partial.json"


def load_state():
    data = json.loads(run.DATASET.read_text(encoding="utf-8"))
    samples = data["samples"]
    if PARTIAL.exists():
        payload = json.loads(PARTIAL.read_text(encoding="utf-8"))
        results = payload["results"]
        if len(results) == len(samples):
            return data, results, payload.get("metadata", {})
    results = [
        {"sample_id": sample["sample_id"], "group": sample["group"],
         "match_stratum": sample["match_stratum"], "metrics": {}, "errors": {}}
        for sample in samples
    ]
    metadata = {
        "dataset": str(run.DATASET), "sample_count": len(samples),
        "device": run.DEVICE, "torch": torch.__version__,
        "cuda": torch.version.cuda,
        "models": {key: str(value) for key, value in run.MODELS.items()},
        "perturbations": run.PERTURBATIONS, "regenerations": run.REGENERATIONS,
        "started_utc": datetime.now(timezone.utc).isoformat(),
    }
    return data, results, metadata


def save(data, results, metadata):
    metadata["updated_utc"] = datetime.now(timezone.utc).isoformat()
    run.write_outputs(results, metadata)
    PARTIAL.write_text(json.dumps({"metadata": metadata, "results": results}, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["causal", "perplexity", "uid", "embedding", "perturb", "dna"])
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=None)
    args = parser.parse_args()
    data, results, metadata = load_state()
    samples = data["samples"]
    end = len(samples) if args.end is None else min(args.end, len(samples))
    start = max(0, args.start)
    texts = [sample["text"] for sample in samples]

    if args.stage == "causal":
        model, tokenizer = run.load_causal(run.MODELS["causal"])
        for i in range(start, end):
            print(f"causal {i + 1}/{len(samples)} {results[i]['sample_id']}", flush=True)
            results[i]["errors"].pop("causal_metrics", None)
            try:
                logits, labels = run.score_text(texts[i], model, tokenizer)
                run.calculate_causal_metrics(results[i], logits, labels)
                run.calculate_fast_detect(results[i], texts[i], model, tokenizer)
            except Exception as exc:
                run.fail(results[i], "causal_metrics", exc)
        run.release(model, tokenizer)
    elif args.stage == "perplexity":
        model, tokenizer = run.load_causal(run.MODELS["perplexity"])
        for i in range(start, end):
            print(f"perplexity {i + 1}/{len(samples)} {results[i]['sample_id']}", flush=True)
            try:
                run.calculate_ppl(results[i], texts[i], model, tokenizer)
            except Exception as exc:
                run.fail(results[i], "perplexity_gpt2_large", exc)
        run.release(model, tokenizer)
    elif args.stage == "uid":
        model, tokenizer = run.load_causal(run.MODELS["uid"])
        for i in range(start, end):
            print(f"uid {i + 1}/{len(samples)} {results[i]['sample_id']}", flush=True)
            try:
                run.calculate_uid(results[i], texts[i], model, tokenizer)
            except Exception as exc:
                run.fail(results[i], "uid_metrics", exc)
        run.release(model, tokenizer)
    elif args.stage == "embedding":
        tokenizer = RobertaTokenizer.from_pretrained(str(run.MODELS["embedding"]), local_files_only=True)
        model = RobertaModel.from_pretrained(str(run.MODELS["embedding"]), local_files_only=True).to(run.DEVICE)
        model.eval()
        for i in range(start, end):
            print(f"embedding {i + 1}/{len(samples)} {results[i]['sample_id']}", flush=True)
            results[i]["errors"].pop("phd_intrinsic_dimension", None)
            results[i]["errors"].pop("mle_intrinsic_dimension", None)
            results[i]["errors"].pop("embedding_metrics", None)
            try:
                run.calculate_embeddings(results[i], texts[i], model, tokenizer)
            except Exception as exc:
                run.fail(results[i], "embedding_metrics", exc)
        run.release(model, tokenizer)
    elif args.stage == "perturb":
        base_model, base_tokenizer = run.load_causal(run.MODELS["causal"])
        mask_tokenizer = AutoTokenizer.from_pretrained(str(run.MODELS["mask"]), local_files_only=True)
        mask_model = AutoModelForSeq2SeqLM.from_pretrained(str(run.MODELS["mask"]), local_files_only=True).to(run.DEVICE)
        mask_model.eval()
        for i in range(start, end):
            print(f"perturbation {i + 1}/{len(samples)} {results[i]['sample_id']}", flush=True)
            results[i]["errors"].pop("perturbation_metrics", None)
            try:
                run.calculate_perturbation(results[i], texts[i], base_model, base_tokenizer, mask_model, mask_tokenizer)
            except Exception as exc:
                run.fail(results[i], "perturbation_metrics", exc)
        run.release(base_model, base_tokenizer, mask_model, mask_tokenizer)
    elif args.stage == "dna":
        model, tokenizer = run.load_causal(run.MODELS["causal"])
        for i in range(start, end):
            print(f"generation {i + 1}/{len(samples)} {results[i]['sample_id']}", flush=True)
            try:
                run.calculate_dna(results[i], texts[i], model, tokenizer)
            except Exception as exc:
                run.fail(results[i], "dna_metrics", exc)
        run.release(model, tokenizer)

    save(data, results, metadata)
    print(f"COMPLETED {args.stage} {start}:{end}", flush=True)


if __name__ == "__main__":
    main()
