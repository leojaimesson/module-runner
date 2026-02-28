from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class PythonPackageManager(ABC):
    """Strategy that manages the Python environment and builds the execution command."""

    @abstractmethod
    def build(self, module_path: Path, script_path: Path, payload: Optional[dict]) -> list[str]: ...
