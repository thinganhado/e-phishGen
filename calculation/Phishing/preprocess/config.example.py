"""Secret-free configuration template for the copied preprocessing scripts."""

from pathlib import Path

# Set this to the directory containing the corpus inputs and outputs.
PROJECT_ROOT = Path(r"C:\path\to\cross-model-phishing")
DATA_DIR = PROJECT_ROOT / "data"
HUMAN_DIR = DATA_DIR / "human"
LLM_DIR = DATA_DIR / "llm"
LOGS_DIR = PROJECT_ROOT / "logs"

