"""Resumable HWT/MGT run for scaled_stratified_pool_8980.

The original 44-sample runner writes only after all model stages finish.  This
runner checkpoints after each sample and stage, so a GPU/runtime failure does
not discard completed work.
"""

from __future__ import annotations

import gc
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer, RobertaModel, RobertaTokenizer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import run_matched_pool_44 as runner

runner.DATASET = ROOT / os.environ.get("HWT_MGT_DATASET", "scaled_stratified_pool_8980.json")
runner.OUTPUT_DIR = HERE / "results"
DATASET_STEM = runner.DATASET.stem
CHECKPOINT = runner.OUTPUT_DIR / f"{DATASET_STEM}_metrics.partial.json"
FINAL_JSON = runner.OUTPUT_DIR / f"{DATASET_STEM}_metrics.json"
FINAL_MD = runner.OUTPUT_DIR / f"{DATASET_STEM}_metrics.md"


def save_checkpoint(results, metadata):
    # Write beside the checkpoint and replace it only after the complete JSON
    # has been flushed.  This also recovers cleanly from an interrupted write
    # or a transient Windows file-handle error.
    payload = json.dumps(
        {"metadata": metadata, "results": results},
        indent=2,
        ensure_ascii=False,
        default=runner.scalarize,
    )
    temporary = CHECKPOINT.with_name(CHECKPOINT.name + ".tmp")
    temporary.write_text(payload, encoding="utf-8")
    os.replace(temporary, CHECKPOINT)


def release_safe(*models):
    for model in models:
        del model
    gc.collect()
    if torch.cuda.is_available():
        try:
            torch.cuda.empty_cache()
        except Exception as exc:
            print(f"WARNING cleanup failed: {type(exc).__name__}: {exc}", flush=True)


def load_checkpoint(samples):
    if not CHECKPOINT.exists():
        return [{"sample_id": s["sample_id"], "group": s["group"], "match_stratum": s.get("match_stratum"), "metrics": {}, "errors": {}} for s in samples]
    payload = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    rows = payload.get("results", [])
    if [row.get("sample_id") for row in rows] != [s["sample_id"] for s in samples]:
        raise ValueError("Existing checkpoint does not match the current dataset order")
    print(f"Resuming checkpoint: {CHECKPOINT}", flush=True)
    return rows


def run_stage(results, texts, name, fn, required_keys):
    pending = [
        i for i, row in enumerate(results)
        if not all(key in row["metrics"] for key in required_keys)
        or any(key == name or key.startswith(name + "_") for key in row["errors"])
    ]
    print(f"Stage {name}: {len(pending)} samples pending", flush=True)
    for done, index in enumerate(pending, 1):
        result = results[index]
        print(f"{name} {done}/{len(pending)} {result['sample_id']}", flush=True)
        try:
            fn(result, texts[index])
            for key in list(result["errors"]):
                if key == name or key.startswith(name + "_"):
                    result["errors"].pop(key, None)
        except Exception as exc:
            runner.fail(result, name, exc)
            print(f"ERROR {name} {result['sample_id']}: {type(exc).__name__}: {exc}", flush=True)
        if done % 10 == 0 or done == len(pending):
            save_checkpoint(results, metadata)


def main():
    global metadata
    data = json.loads(runner.DATASET.read_text(encoding="utf-8"))
    samples = data["samples"]
    texts = [sample["text"] for sample in samples]
    results = load_checkpoint(samples)
    metadata = {
        "dataset": str(runner.DATASET),
        "sample_count": len(samples),
        "device": runner.DEVICE,
        "torch": torch.__version__,
        "cuda": torch.version.cuda,
        "models": {key: str(value) for key, value in runner.MODELS.items()},
        "perturbations": runner.PERTURBATIONS,
        "regenerations": runner.REGENERATIONS,
        "resumable": True,
        "started_utc": datetime.now(timezone.utc).isoformat(),
    }
    print(f"Running {len(samples)} samples on {runner.DEVICE}", flush=True)

    causal_model, causal_tokenizer = runner.load_causal(runner.MODELS["causal"])
    def causal(result, text):
        logits, labels = runner.score_text(text, causal_model, causal_tokenizer)
        runner.calculate_causal_metrics(result, logits, labels)
        runner.calculate_fast_detect(result, text, causal_model, causal_tokenizer)
    run_stage(results, texts, "causal_metrics", causal, ["predictive_entropy", "fast_detectgpt_sampling"])
    release_safe(causal_model, causal_tokenizer)

    ppl_model, ppl_tokenizer = runner.load_causal(runner.MODELS["perplexity"])
    run_stage(results, texts, "perplexity", lambda result, text: runner.calculate_ppl(result, text, ppl_model, ppl_tokenizer), ["perplexity_gpt2_large"])
    release_safe(ppl_model, ppl_tokenizer)

    uid_model, uid_tokenizer = runner.load_causal(runner.MODELS["uid"])
    run_stage(results, texts, "uid", lambda result, text: runner.calculate_uid(result, text, uid_model, uid_tokenizer), ["uid_mean", "total_surprisal"])
    release_safe(uid_model, uid_tokenizer)

    embedding_tokenizer = RobertaTokenizer.from_pretrained(str(runner.MODELS["embedding"]), local_files_only=True)
    embedding_model = RobertaModel.from_pretrained(str(runner.MODELS["embedding"]), local_files_only=True).to(runner.DEVICE)
    embedding_model.eval()
    run_stage(results, texts, "embedding", lambda result, text: runner.calculate_embeddings(result, text, embedding_model, embedding_tokenizer), ["phd_intrinsic_dimension", "mle_intrinsic_dimension"])
    release_safe(embedding_model, embedding_tokenizer)

    base_model, base_tokenizer = runner.load_causal(runner.MODELS["causal"])
    mask_tokenizer = AutoTokenizer.from_pretrained(str(runner.MODELS["mask"]), local_files_only=True)
    mask_model = AutoModelForSeq2SeqLM.from_pretrained(str(runner.MODELS["mask"]), local_files_only=True).to(runner.DEVICE)
    mask_model.eval()
    run_stage(results, texts, "perturbation", lambda result, text: runner.calculate_perturbation(result, text, base_model, base_tokenizer, mask_model, mask_tokenizer), ["detectgpt_discrepancy", "npr"])
    release_safe(base_model, base_tokenizer, mask_model, mask_tokenizer)

    dna_model, dna_tokenizer = runner.load_causal(runner.MODELS["causal"])
    run_stage(results, texts, "dna", lambda result, text: runner.calculate_dna(result, text, dna_model, dna_tokenizer), ["ngram_overlap_ratio", "weighted_ngram_score", "dna_gpt_regeneration_log_probability_difference"])
    release_safe(dna_model, dna_tokenizer)

    metadata["finished_utc"] = datetime.now(timezone.utc).isoformat()
    FINAL_JSON.write_text(json.dumps({"metadata": metadata, "results": results}, indent=2, ensure_ascii=False, default=runner.scalarize), encoding="utf-8")
    runner.write_outputs(results, metadata)
    FINAL_MD.write_text(FINAL_MD.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"WROTE {FINAL_JSON}", flush=True)
    print(f"WROTE {FINAL_MD}", flush=True)


if __name__ == "__main__":
    main()
