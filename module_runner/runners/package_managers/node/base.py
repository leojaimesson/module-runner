import json
import logging
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from ....environment.constants import NODE_MODULES_DIR, PACKAGE_JSON

logger = logging.getLogger("module_runner")


class NodePackageManager(ABC):
    """Manages Node.js dependencies and builds script execution commands."""

    @abstractmethod
    def install(self, module_path: Path, module_name: str) -> None:
        """Install dependencies if needed."""
        ...

    @abstractmethod
    def run_script(self, script: str, payload: Optional[dict]) -> list[str]:
        """Build the command to run a package.json script."""
        ...

    def _needs_install(self, module_path: Path) -> bool:
        return (module_path / PACKAGE_JSON).exists() and not (module_path / NODE_MODULES_DIR).exists()

    def _reusing(self, module_path: Path) -> bool:
        return (module_path / NODE_MODULES_DIR).exists()

    def _run_install(self, cmd: list[str], module_path: Path, module_name: str) -> None:
        logger.info("[%s] installing deps: %s", module_name, " ".join(cmd))
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=str(module_path))
        except subprocess.CalledProcessError as exc:
            stderr = exc.stderr.strip() if exc.stderr else str(exc)
            raise RuntimeError(
                f"Environment 'node' failed to install dependencies for module '{module_name}': {stderr}"
            ) from exc
