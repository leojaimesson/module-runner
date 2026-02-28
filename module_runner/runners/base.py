import logging
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from subprocess import CompletedProcess
from typing import Optional

from ..exceptions import RunnerExecutionError

logger = logging.getLogger("module_runner")


class BaseRunner(ABC):

    def __init__(self, module_path: str | Path, entrypoint: Optional[str] = None) -> None:
        self.module_path = Path(module_path).resolve()
        self.module_name = self.module_path.name
        self.entrypoint = entrypoint

    def run(self, payload: Optional[dict] = None) -> CompletedProcess[str]:
        cmd = self._build_command(payload)

        logger.info("[%s] executing: %s", self.module_name, " ".join(cmd))

        process: CompletedProcess[str] = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.module_path),
        )

        if process.returncode != 0:
            raise RunnerExecutionError(
                module=self.module_name,
                exit_code=process.returncode,
                stderr=process.stderr,
                stdout=process.stdout,
                cmd=cmd,
            )

        return process

    @abstractmethod
    def _build_command(self, payload: Optional[dict]) -> list[str]: ...

    def _entrypoint_path(self, default: str) -> Path:
        entry_point = self.entrypoint or default
        script_path = self.module_path / entry_point
        if not script_path.exists():
            raise FileNotFoundError(f"Module '{self.module_name}' does not contain {entry_point}")
        return script_path
