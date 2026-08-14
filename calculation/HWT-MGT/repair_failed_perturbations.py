"""Repair only samples with failed perturbation metrics in the checkpoint."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import run_matched_pool_44 as runner

DATASET = ROOT / "scaled_stratified_pool_8980.json"
CHECKPOINT = HERE / "results" / "scaled_stratified_pool_8980_metrics.partial.json"
LOG = HERE / "results" / "scaled_stratified_pool_8980_targeted_perturbation.log"
ERROR_LOG = HERE / "results" / "scaled_stratified_pool_8980_targeted_perturbation.err.log"


def main():
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    rows = checkpoint["results"]
    samples = {sample["sample_id"]: sample for sample in data["samples"]}
    targets = [row for row in rows if "perturbation" in row.get("errors", {})]
    print(f"Targeted perturbation repairs: {len(targets)}", flush=True)

    base_model, base_tokenizer = runner.load_causal(runner.MODELS["causal"])
    mask_tokenizer = AutoTokenizer.from_pretrained(str(runner.MODELS["mask"]), local_files_only=True)
    mask_model = AutoModelForSeq2SeqLM.from_pretrained(str(runner.MODELS["mask"]), local_files_only=True).to(runner.DEVICE)
    mask_model.eval()

    for index, row in enumerate(targets, 1):
        sample = samples[row["sample_id"]]
        print(f"repair {index}/{len(targets)} {row['sample_id']}", flush=True)
        try:
            runner.calculate_perturbation(row, sample["text"], base_model, base_tokenizer, mask_model, mask_tokenizer)
            row["errors"].pop("perturbation", None)
        except Exception as exc:
            row["errors"]["perturbation"] = f"{type(exc).__name__}: {exc}"
            print(f"ERROR {row['sample_id']}: {type(exc).__name__}: {exc}", flush=True)
        if index % 10 == 0 or index == len(targets):
            CHECKPOINT.write_text(json.dumps(checkpoint, indent=2, ensure_ascii=False, default=runner.scalarize), encoding="utf-8")

    runner.release(base_model, base_tokenizer, mask_model, mask_tokenizer)
    checkpoint.setdefault("metadata", {})["last_targeted_repair_utc"] = datetime.now(timezone.utc).isoformat()
    CHECKPOINT.write_text(json.dumps(checkpoint, indent=2, ensure_ascii=False, default=runner.scalarize), encoding="utf-8")
    remaining = sum("perturbation" in row.get("errors", {}) for row in rows)
    print(f"Targeted repair complete; remaining perturbation errors: {remaining}", flush=True)


if __name__ == "__main__":
    main()
