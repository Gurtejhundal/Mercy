"""Run the bundled toolkit from any learner repository without installation."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mercy.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
