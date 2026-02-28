import json
import sys
from pathlib import Path
from typing import Optional

from .base import PythonPackageManager


class SystemPackageManager(PythonPackageManager):
    """Uses the current system interpreter — no environment setup."""

    def build(self, module_path: Path, script_path: Path, payload: Optional[dict]) -> list[str]:
        cmd = [sys.executable, str(script_path)]
        if payload is not None:
            cmd.append(json.dumps(payload))
        return cmd
