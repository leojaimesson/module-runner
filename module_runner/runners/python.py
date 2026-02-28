from pathlib import Path
from typing import Optional

from ..environment.constants import MAIN_PY
from .base import BaseRunner
from .package_managers import PythonPackageManager, UvPackageManager


class PythonRunner(BaseRunner):
    """Runs a Python module using the provided package manager strategy."""

    def __init__(
        self,
        module_path: str | Path,
        package_manager: PythonPackageManager = None,
        entrypoint: Optional[str] = None,
    ) -> None:
        super().__init__(module_path, entrypoint)
        self.package_manager = package_manager or UvPackageManager()

    def _build_command(self, payload: Optional[dict]) -> list[str]:
        script_path = self._entrypoint_path(MAIN_PY)
        return self.package_manager.build(self.module_path, script_path, payload)

