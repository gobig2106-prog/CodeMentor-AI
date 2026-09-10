"""Start CodeMentor AI with: python app.py"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.gui import launch  # noqa: E402


if __name__ == "__main__":
    launch(ROOT / "dataset" / "programming_qa.csv")