from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import run_matched_pool_44 as runner

runner.DATASET = ROOT / "scaled_stratified_pool_8980.json"
runner.OUTPUT_DIR = HERE / "results"

if __name__ == "__main__":
    runner.main()
