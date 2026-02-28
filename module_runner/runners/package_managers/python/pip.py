import json
from pathlib import Path
from typing import Optional

from ....environment.pip_env import ensure_pip_environment
from .base import PythonPackageManager


class PipPackageManager(PythonPackageManager):
    """Manages the environment via a venv provisioned by pip."""

    def build(self, module_path: Path, script_path: Path, payload: Optional[dict]) -> list[str]:
        executor = ensure_pip_environment(module_path, module_path.name)
        cmd = [str(executor), str(script_path)]
        if payload is not None:
            cmd.append(json.dumps(payload))
        return cmd
