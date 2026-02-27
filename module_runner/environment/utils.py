import sys
from pathlib import Path


def venv_python(venv_path: Path) -> Path:
    """Return the Python interpreter path inside a virtual environment."""
    if sys.platform.startswith("win"):
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"
