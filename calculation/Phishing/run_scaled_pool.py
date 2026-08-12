from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import run_matched_pool_44 as runner

runner.DATASET = ROOT / "scaled_stratified_pool_8980.json"
runner.JSON_OUT = HERE / "results" / "scaled_stratified_pool_8980_phishing_metrics.json"
runner.MD_OUT = HERE / "results" / "scaled_stratified_pool_8980_phishing_metrics.md"

if __name__ == "__main__":
    runner.main()
