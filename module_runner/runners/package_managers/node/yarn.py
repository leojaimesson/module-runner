import json
import logging
import shutil
from pathlib import Path
from typing import Optional

from .base import NodePackageManager


class YarnPackageManager(NodePackageManager):
    """Manages Node.js dependencies and scripts using Yarn."""

    def __init__(self) -> None:
        self._bin = shutil.which("yarn")
        if self._bin is None:
            raise RuntimeError("yarn executable not found in PATH")

    def install(self, module_path: Path, module_name: str) -> None:
        if self._needs_install(module_path):
            self._run_install([self._bin, "install"], module_path, module_name)
        elif self._reusing(module_path):
            logging.getLogger("module_runner").info("[%s] reusing existing node_modules", module_name)

    def run_script(self, script: str, payload: Optional[dict]) -> list[str]:
        cmd = [self._bin, script]
        if payload is not None:
            cmd.append(json.dumps(payload))
        return cmd
