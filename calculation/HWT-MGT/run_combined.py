import os
os.environ["HWT_MGT_DATASET"] = "combined_calculation.json"
import run_scaled_pool_resumable

if __name__ == "__main__":
    run_scaled_pool_resumable.main()
