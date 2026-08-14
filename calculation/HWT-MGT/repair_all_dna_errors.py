"""Rerun only DNA-GPT failures and append a complete audit to completion.log."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import run_matched_pool_44 as runner

runner.DATASET = ROOT / "scaled_stratified_pool_8980.json"
runner.OUTPUT_DIR = HERE / "results"
CHECKPOINT = HERE / "results" / "scaled_stratified_pool_8980_metrics.partial.json"
FINAL_JSON = HERE / "results" / "scaled_stratified_pool_8980_metrics.json"
LOG = HERE / "results" / "scaled_stratified_pool_8980_completion.log"


class Tee:
    def __init__(self, original, path):
        self.original = original
        self.stream = path.open("a", encoding="utf-8", buffering=1)

    def write(self, value):
        self.original.write(value)
        self.original.flush()
        self.stream.write(value)
        self.stream.flush()

    def flush(self):
        self.original.flush()
        self.stream.flush()


sys.stdout = Tee(sys.stdout, LOG)
sys.stderr = Tee(sys.stderr, LOG)


def save(payload):
    CHECKPOINT.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=runner.scalarize), encoding="utf-8")


def main():
    payload = json.loads(FINAL_JSON.read_text(encoding="utf-8"))
    data = json.loads(runner.DATASET.read_text(encoding="utf-8"))
    samples = {sample["sample_id"]: sample for sample in data["samples"]}
    rows = payload["results"]
    targets = [row for row in rows if "dna" in row.get("errors", {})]
    limit = int(os.environ.get("DNA_REPAIR_LIMIT", "0"))
    if limit:
        targets = targets[:limit]
    print("\n=== CONSOLIDATED DNA ERROR REPAIR ===", flush=True)
    print(f"started_utc={datetime.now(timezone.utc).isoformat()}", flush=True)
    print(f"target_count={len(targets)} limit={limit or 'none'}", flush=True)
    print("repair_scope=dna only; all other completed metrics preserved", flush=True)

    model, tokenizer = runner.load_causal(runner.MODELS["causal"])
    for index, row in enumerate(targets, 1):
        sample_id = row["sample_id"]
        print(f"DNA_REPAIR {index}/{len(targets)} {sample_id}", flush=True)
        try:
            runner.calculate_dna(row, samples[sample_id]["text"], model, tokenizer)
            row["errors"].pop("dna", None)
        except Exception as exc:
            row["errors"]["dna"] = f"{type(exc).__name__}: {exc}"
            print(f"ERROR DNA_REPAIR {sample_id}: {type(exc).__name__}: {exc}", flush=True)
        if index % 10 == 0 or index == len(targets):
            save(payload)

    runner.release(model, tokenizer)
    payload.setdefault("metadata", {})["dna_error_repair_utc"] = datetime.now(timezone.utc).isoformat()
    payload["metadata"]["dna_prompt_token_safe"] = True
    save(payload)
    runner.write_outputs(rows, payload["metadata"])
    remaining = [(row["sample_id"], key) for row in rows for key in row.get("errors", {})]
    print(f"DNA_REPAIR_COMPLETE remaining_errors={len(remaining)}", flush=True)
    if remaining:
        print(f"remaining_error_types={sorted(set(key for _, key in remaining))}", flush=True)
    else:
        print("ALL_HWT_MGT_METRICS_ERROR_FREE", flush=True)


if __name__ == "__main__":
    main()
