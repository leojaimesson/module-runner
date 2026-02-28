import json
from pathlib import Path
from typing import Optional

from ....environment.uv_env import ensure_uv_environment
from .base import PythonPackageManager


class UvPackageManager(PythonPackageManager):
    """Manages the environment via uv — supports both pyproject.toml (uv run) and requirements.txt (venv)."""

    def build(self, module_path: Path, script_path: Path, payload: Optional[dict]) -> list[str]:
        executor = ensure_uv_environment(module_path, module_path.name)
        if str(executor) == "uv":
            cmd = ["uv", "run", "--project", str(module_path), "python", str(script_path)]
        else:
            cmd = [str(executor), str(script_path)]
        if payload is not None:
            cmd.append(json.dumps(payload))
        return cmd
